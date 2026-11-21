"""Index text PDFs for LexAI with document and page provenance."""

import argparse
from hashlib import sha256
import os
from pathlib import Path

from download_sources import SOURCES
from providers import EMBEDDING_DIMENSIONS, EMBEDDING_MODEL, index_settings


def pdf_chunks(path: Path, tessdata: str | None = None):
    import pymupdf

    version = sha256(path.read_bytes()).hexdigest()
    with pymupdf.open(path) as document:
        for page_number, page in enumerate(document, 1):
            text = page.get_text()
            scanned = not text.strip() and tessdata is not None
            if scanned:
                text_page = page.get_textpage_ocr(language="eng", dpi=200, full=True, tessdata=tessdata)
                text = page.get_text(textpage=text_page)
            words = text.split()
            for start in range(0, len(words), 110):
                excerpt = " ".join(words[start:start + 140])
                record_id = sha256(f"{path.name}:{version}:{page_number}:{start}".encode()).hexdigest()
                metadata = {"source": path.name, "page": page_number, "text": excerpt, "ocr": scanned}
                if path.name in SOURCES:
                    metadata["url"] = f"{SOURCES[path.name]}#page={page_number}"
                yield record_id, metadata
                if start + 140 >= len(words):
                    break


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Directory containing public legal PDFs")
    parser.add_argument("--ocr", action="store_true", help="Read scanned pages using English Tesseract data")
    args = parser.parse_args()

    files = sorted(path for path in args.directory.glob("*") if path.is_file() and path.suffix.lower() == ".pdf")
    if not files:
        parser.error("No PDFs found. Pass a directory containing public, text-searchable legal PDFs.")

    from dotenv import load_dotenv

    load_dotenv()
    if not os.getenv("PINECONE_API_KEY"):
        parser.error("Set PINECONE_API_KEY in .env before indexing.")

    from pinecone import Pinecone, ServerlessSpec
    from sentence_transformers import SentenceTransformer

    tessdata = None
    if args.ocr:
        import pymupdf

        try:
            tessdata = pymupdf.get_tessdata()
        except RuntimeError:
            parser.error("Install Tesseract with English language data or set TESSDATA_PREFIX.")

    chunks = []
    for path in files:
        passages = list(pdf_chunks(path, tessdata))
        if not passages:
            print(f"Skipped {path.name} because it had no extractable text.")
        else:
            print(f"Prepared {len(passages)} passages from {path.name}.")
        chunks.extend(passages)
    if not chunks:
        parser.error("No extractable text found. Use searchable PDFs or run OCR first.")

    index_name, namespace = index_settings()
    pinecone = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    if not pinecone.indexes.exists(index_name):
        pinecone.indexes.create(
            name=index_name,
            dimension=EMBEDDING_DIMENSIONS,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=os.getenv("PINECONE_CLOUD", "aws"),
                region=os.getenv("PINECONE_REGION", "us-east-1"),
            ),
            timeout=120,
        )

    index_info = pinecone.indexes.describe(index_name)
    if index_info.dimension != EMBEDDING_DIMENSIONS or index_info.metric != "cosine":
        parser.error(f"Use a {EMBEDDING_DIMENSIONS}-dimension cosine index.")
    if not index_info.status.ready:
        parser.error("The Pinecone index is still preparing. Try again when it is ready.")

    index = pinecone.index(host=index_info.host)
    model = SentenceTransformer(EMBEDDING_MODEL)
    batch_size = 64
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        embeddings = model.encode([metadata["text"] for _, metadata in batch]).tolist()
        index.upsert(
            vectors=[
                {"id": record_id, "values": embedding, "metadata": metadata}
                for (record_id, metadata), embedding in zip(batch, embeddings, strict=True)
            ],
            namespace=namespace,
        )
    print(f"Uploaded {len(chunks)} passages to {index_name}/{namespace}.")


if __name__ == "__main__":
    main()
