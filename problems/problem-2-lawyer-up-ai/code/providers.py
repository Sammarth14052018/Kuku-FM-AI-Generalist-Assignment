"""Live provider adapters and shared vector index settings."""

import os
import re

from download_sources import SOURCES
from research import Research, Source


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSIONS = 384


def index_settings() -> tuple[str, str]:
    return (
        os.getenv("PINECONE_INDEX", "law-suggestion-index"),
        os.getenv("PINECONE_NAMESPACE", "lexai-v1"),
    )


def live_research() -> Research:
    from dotenv import load_dotenv

    load_dotenv()
    required = ("GROQ_API_KEY", "PINECONE_API_KEY")
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise ValueError(f"Set {', '.join(missing)} to start live research.")

    from groq import Groq
    from pinecone import Pinecone
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(EMBEDDING_MODEL)
    index_name, namespace = index_settings()
    pinecone = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pinecone.index(index_name)
    client = Groq(timeout=25, max_retries=0)
    groq_model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    search_key = os.getenv("SERPAPI_API_KEY")

    def retrieve(question: str) -> list[Source]:
        def query(text: str, limit: int, **filters):
            return index.query(
                vector=model.encode(text).tolist(),
                namespace=namespace,
                top_k=limit,
                include_metadata=True,
                timeout=10,
                **filters,
            ).matches

        matches = query(question, 5)
        named_sources = []
        for filename in SOURCES:
            title = filename.removesuffix(".pdf").rsplit(",", 1)[0]
            pattern = re.compile(rf"\b{re.escape(title)}\b(?:,?\s+\d{{4}})?", re.IGNORECASE)
            if pattern.search(question):
                named_sources.append((filename, pattern))

        # Named acts can dominate a question's embedding and hide its subject.
        if len(named_sources) == 1:
            filename, pattern = named_sources[0]
            topic = pattern.sub("", question).strip(" ,?.")
            if topic:
                focused = query(topic, 8, filter={"source": {"$eq": filename}})
                matches = [*focused, *matches]

        sources = []
        seen = set()
        for match in matches:
            if match.id in seen:
                continue
            seen.add(match.id)
            metadata = match.metadata or {}
            if metadata.get("source") and metadata.get("page") and metadata.get("text"):
                sources.append(Source(
                    title=metadata["source"],
                    excerpt=metadata["text"],
                    page=int(metadata["page"]),
                    score=float(match.score),
                    url=metadata.get("url"),
                    ocr=bool(metadata.get("ocr")),
                ))
        return sources

    def search(question: str) -> list[Source]:
        if not search_key:
            return []

        from urllib.error import URLError
        from urllib.parse import urlencode, urlsplit
        from urllib.request import urlopen
        import json

        query = f"{question} India (site:gov.in OR site:nic.in)"
        params = urlencode({
            "engine": "google", "q": query, "api_key": search_key, "gl": "in", "hl": "en",
        })
        try:
            with urlopen(f"https://serpapi.com/search.json?{params}", timeout=8) as response:
                results = json.load(response).get("organic_results", [])
        except (URLError, TimeoutError, ValueError):
            return []

        leads = []
        for result in results:
            url = result.get("link", "")
            parsed = urlsplit(url)
            hostname = parsed.hostname or ""
            if parsed.scheme == "https" and hostname.endswith((".gov.in", ".nic.in")):
                leads.append(Source(result.get("title") or hostname, result.get("snippet", ""), url=url))
            if len(leads) == 3:
                break
        return leads

    def generate(prompt: str) -> str:
        response = client.chat.completions.create(
            model=groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_completion_tokens=1800,
        )
        return response.choices[0].message.content or ""

    return Research(retrieve, search, generate)
