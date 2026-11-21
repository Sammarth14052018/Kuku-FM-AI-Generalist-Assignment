"""Download the public Indian legal PDFs used by the LexAI notebook."""

from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.error import URLError
from urllib.request import Request, urlopen


CORPUS_DIR = Path(__file__).resolve().parent / "data" / "legal"
SOURCES = {
    "Bharatiya Nyaya Sanhita, 2023.pdf":
        "https://www.mha.gov.in/files/documents/250883_english_01042024.pdf",
    "Sexual Harassment of Women at Workplace Act, 2013.pdf":
        "https://lpai.mha.gov.in/media/icc/sexual-harassment-Act-2013.pdf",
    "Criminal Law (Amendment) Act, 2013.pdf":
        "https://www.mha.gov.in/files/acts_rules_documets/TheCrimnalLaw030413.pdf",
    "Commission of Sati (Prevention) Act, 1987.pdf":
        "https://cdn.ncw.gov.in/wp-content/uploads/2023/06/TheCommissionofSatiPreventionAct1987-of1988_0.pdf",
    "Dowry Prohibition Act, 1961.pdf":
        "https://www.uppolice.gov.in/site/writereaddata/siteContent/acts/202202171231581300TheDowryProhibitionAct1961.pdf",
    "Immoral Traffic (Prevention) Act, 1956.pdf":
        "https://cdnbbsr.s3waas.gov.in/s3a012869311d64a44b5a0d567cd20de04/uploads/2023/07/2023070639-1.pdf",
    "Indecent Representation of Women (Prohibition) Act, 1986.pdf":
        "https://cdn.ncw.gov.in/wp-content/uploads/2023/06/TheIndecentRepresentationofWomenProhibitionAct1986_2.pdf",
    "Protection of Women from Domestic Violence Act, 2005.pdf":
        "https://cdn.ncw.gov.in/wp-content/uploads/2023/06/TheProtectionofWomenfromDomesticViolenceAct2005_0.pdf",
}


def download_sources(directory: Path = CORPUS_DIR) -> list[Path]:
    directory.mkdir(parents=True, exist_ok=True)
    paths = []
    errors = []
    for filename, url in SOURCES.items():
        path = directory / filename
        if path.is_file():
            with path.open("rb") as cached:
                if cached.read(5) == b"%PDF-":
                    paths.append(path)
                    continue

        try:
            request = Request(url, headers={"User-Agent": "LexAI corpus downloader/1.0"})
            with urlopen(request, timeout=20) as response:
                content = response.read(25_000_001)
            if not content.startswith(b"%PDF-") or len(content) > 25_000_000:
                raise ValueError("The source did not return a supported PDF.")
            with NamedTemporaryFile(dir=directory, delete=False) as temporary:
                temp_path = Path(temporary.name)
                try:
                    temporary.write(content)
                    temporary.flush()
                    temp_path.replace(path)
                finally:
                    temp_path.unlink(missing_ok=True)
        except (URLError, OSError, ValueError) as exc:
            errors.append(f"{filename}: {exc} ({url})")
        else:
            paths.append(path)

    if errors:
        raise RuntimeError("Could not download all legal PDFs. Retry to fetch the missing files.\n" + "\n".join(errors))
    return paths


if __name__ == "__main__":
    try:
        for pdf in download_sources():
            print(pdf.name)
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from None
