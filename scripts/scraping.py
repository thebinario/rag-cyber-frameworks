from __future__ import annotations

import json
import re
import ssl
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "data" / "raw"
MANIFEST_PATH = REPO_ROOT / "data" / "processed" / "manifests" / "documents_manifest.json"

REQUEST_HEADERS = {
    "User-Agent": "rag-cyber-frameworks/1.0 (educational project)",
}
REQUEST_TIMEOUT = 60
DELAY_BETWEEN_REQUESTS = 1.0

_SSL_CONTEXT = ssl.create_default_context()
_SSL_CONTEXT.check_hostname = False
_SSL_CONTEXT.verify_mode = ssl.CERT_NONE


def _urlopen(req: request.Request, timeout: int = REQUEST_TIMEOUT):
    return request.urlopen(req, timeout=timeout, context=_SSL_CONTEXT)


def _download(url: str, dest: Path, binary: bool = False) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = request.Request(url, headers=REQUEST_HEADERS)
    try:
        with _urlopen(req) as resp:
            raw = resp.read()
        if binary:
            dest.write_bytes(raw)
        else:
            text = raw.decode("utf-8", errors="replace")
            clean = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
            dest.write_bytes(clean.encode("utf-8"))
        return True
    except (error.URLError, error.HTTPError, OSError) as exc:
        print(f"  FAILED: {exc}")
        return False


def _fetch_html(url: str) -> str:
    req = request.Request(url, headers=REQUEST_HEADERS)
    with _urlopen(req) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _html_to_text(html: str) -> str:
    content_match = re.search(
        r'<div id="mw-content-text"[^>]*>(.*?)</div>\s*<!--',
        html,
        re.DOTALL,
    )
    if content_match:
        html = content_match.group(1)

    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</(p|div|li|tr|h[1-6])>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)

    from html import unescape
    text = unescape(text)

    lines = [line.rstrip() for line in text.splitlines()]
    cleaned: list[str] = []
    blank_count = 0
    for line in lines:
        if not line.strip():
            blank_count += 1
            if blank_count <= 2:
                cleaned.append("")
        else:
            blank_count = 0
            cleaned.append(line)

    return "\n".join(cleaned).strip()


PTES_PAGES = {
    "Pre-engagement": "http://www.pentest-standard.org/index.php/Pre-engagement",
    "Intelligence Gathering": "http://www.pentest-standard.org/index.php/Intelligence_Gathering",
    "Threat Modeling": "http://www.pentest-standard.org/index.php/Threat_Modeling",
    "Vulnerability Analysis": "http://www.pentest-standard.org/index.php/Vulnerability_Analysis",
    "Exploitation": "http://www.pentest-standard.org/index.php/Exploitation",
    "Post Exploitation": "http://www.pentest-standard.org/index.php/Post_Exploitation",
    "Reporting": "http://www.pentest-standard.org/index.php/Reporting",
    "PTES Technical Guidelines": "http://www.pentest-standard.org/index.php/PTES_Technical_Guidelines",
}


def scrape_ptes() -> list[dict[str, str]]:
    print("\n[PTES] Scraping pentest-standard.org...")
    dest_dir = RAW_DIR / "ptes"
    dest_dir.mkdir(parents=True, exist_ok=True)
    documents: list[dict[str, str]] = []

    for title, url in PTES_PAGES.items():
        filename = f"{title}.md"
        dest = dest_dir / filename
        print(f"  {title} <- {url}")

        try:
            html = _fetch_html(url)
            text = _html_to_text(html)
            if len(text) < 200:
                raise ValueError(f"page content too short ({len(text)} chars)")
            dest.write_text(text, encoding="utf-8")
            print(f"  OK ({len(text)} chars)")
        except Exception as exc:
            if dest.exists() and dest.stat().st_size > 200:
                print(f"  FAILED to scrape ({exc}), using existing local file")
            else:
                print(f"  FAILED: {exc}, no local file available")
                continue

        documents.append({
            "id": f"ptes-{title.lower().replace(' ', '-')}",
            "title": title,
            "framework": "ptes",
            "source_type": "markdown",
            "language": "en",
            "path": f"data/raw/ptes/{filename}",
            "origin": url,
        })

        time.sleep(DELAY_BETWEEN_REQUESTS)

    return documents


NIST_PDFS = {
    "NIST.CSWP.29": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "nistspecialpublication800-115": "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf",
    "nistspecialpublication800-53r5": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf",
}


def download_nist() -> list[dict[str, str]]:
    print("\n[NIST] Downloading PDFs...")
    dest_dir = RAW_DIR / "nist"
    documents: list[dict[str, str]] = []

    for name, url in NIST_PDFS.items():
        filename = f"{name}.pdf"
        dest = dest_dir / filename
        print(f"  {name} <- {url}")

        if _download(url, dest, binary=True):
            documents.append({
                "id": f"nist-{name.lower()}",
                "title": name,
                "framework": "nist",
                "source_type": "pdf",
                "language": "en",
                "path": f"data/raw/nist/{filename}",
                "origin": url,
            })
            print(f"  OK ({dest.stat().st_size // 1024} KB)")
        time.sleep(DELAY_BETWEEN_REQUESTS)

    return documents


OSSTMM_URL = "https://www.isecom.org/OSSTMM.3.pdf"


def download_osstmm() -> list[dict[str, str]]:
    print("\n[OSSTMM] Downloading PDF...")
    dest = RAW_DIR / "osstmm" / "OSSTMM.3.pdf"
    print(f"  OSSTMM.3 <- {OSSTMM_URL}")

    if _download(OSSTMM_URL, dest, binary=True):
        print(f"  OK ({dest.stat().st_size // 1024} KB)")
        return [{
            "id": "osstmm-osstmm-3",
            "title": "OSSTMM.3",
            "framework": "osstmm",
            "source_type": "pdf",
            "language": "en",
            "path": "data/raw/osstmm/OSSTMM.3.pdf",
            "origin": OSSTMM_URL,
        }]
    return []


OWASP_WSTG_SECTIONS = {
    "WSTG-INFO": "https://raw.githubusercontent.com/OWASP/wstg/master/document/4-Web_Application_Security_Testing/01-Information_Gathering/README.md",
    "WSTG-CONF": "https://raw.githubusercontent.com/OWASP/wstg/master/document/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/README.md",
    "WSTG-IDNT": "https://raw.githubusercontent.com/OWASP/wstg/master/document/4-Web_Application_Security_Testing/03-Identity_Management_Testing/README.md",
    "WSTG-ATHN": "https://raw.githubusercontent.com/OWASP/wstg/master/document/4-Web_Application_Security_Testing/04-Authentication_Testing/README.md",
    "WSTG-ATHZ": "https://raw.githubusercontent.com/OWASP/wstg/master/document/4-Web_Application_Security_Testing/05-Authorization_Testing/README.md",
    "WSTG-SESS": "https://raw.githubusercontent.com/OWASP/wstg/master/document/4-Web_Application_Security_Testing/06-Session_Management_Testing/README.md",
    "WSTG-INPV": "https://raw.githubusercontent.com/OWASP/wstg/master/document/4-Web_Application_Security_Testing/07-Input_Validation_Testing/README.md",
    "WSTG-ERRH": "https://raw.githubusercontent.com/OWASP/wstg/master/document/4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/README.md",
    "WSTG-CRYP": "https://raw.githubusercontent.com/OWASP/wstg/master/document/4-Web_Application_Security_Testing/09-Testing_for_Weak_Cryptography/README.md",
    "WSTG-BUSL": "https://raw.githubusercontent.com/OWASP/wstg/master/document/4-Web_Application_Security_Testing/10-Business_Logic_Testing/README.md",
    "WSTG-CLNT": "https://raw.githubusercontent.com/OWASP/wstg/master/document/4-Web_Application_Security_Testing/11-Client-side_Testing/README.md",
    "WSTG-APIT": "https://raw.githubusercontent.com/OWASP/wstg/master/document/4-Web_Application_Security_Testing/12-API_Testing/README.md",
}


def download_owasp_wstg() -> list[dict[str, str]]:
    print("\n[OWASP WSTG] Downloading sections from GitHub...")
    dest_dir = RAW_DIR / "owasp-wstg"
    dest_dir.mkdir(parents=True, exist_ok=True)
    documents: list[dict[str, str]] = []

    for section_id, url in OWASP_WSTG_SECTIONS.items():
        filename = f"{section_id}.md"
        dest = dest_dir / filename
        print(f"  {section_id} <- {url}")

        if _download(url, dest):
            content = dest.read_text(encoding="utf-8", errors="replace")
            if len(content) < 100:
                print(f"  WARNING: content too short ({len(content)} chars), skipping")
                continue
            documents.append({
                "id": f"owasp-wstg-{section_id.lower()}",
                "title": f"OWASP WSTG {section_id}",
                "framework": "owasp",
                "source_type": "markdown",
                "language": "en",
                "path": f"data/raw/owasp-wstg/{filename}",
                "origin": url,
            })
            print(f"  OK ({len(content)} chars)")

        time.sleep(DELAY_BETWEEN_REQUESTS)

    return documents


KALI_TOOLS = [
    "hydra", "nmap", "sqlmap", "aircrack-ng", "nikto", "gobuster",
    "john", "hashcat", "metasploit-framework", "burpsuite",
    "wfuzz", "dirb", "enum4linux", "smbclient", "netcat",
    "wireshark", "tcpdump", "responder", "crackmapexec",
    "wpscan", "sublist3r", "amass", "fierce", "dnsrecon",
    "whatweb", "wafw00f", "skipfish", "medusa", "ncrack",
    "reaver", "bettercap", "ettercap", "mitmproxy",
    "searchsploit", "exploitdb",
]

KALI_TOOLS_URL = "https://www.kali.org/tools/{tool}/"


def scrape_kali_tools() -> list[dict[str, str]]:
    print("\n[KALI TOOLS] Scraping kali.org/tools...")
    dest_dir = RAW_DIR / "kali-tools"
    dest_dir.mkdir(parents=True, exist_ok=True)
    documents: list[dict[str, str]] = []

    for tool in KALI_TOOLS:
        url = KALI_TOOLS_URL.format(tool=tool)
        filename = f"{tool}.md"
        dest = dest_dir / filename
        print(f"  {tool} <- {url}")

        try:
            html = _fetch_html(url)
            text = _html_to_text(html)
            if len(text) < 100:
                print(f"  WARNING: content too short ({len(text)} chars), skipping")
                time.sleep(DELAY_BETWEEN_REQUESTS)
                continue
            dest.write_text(text, encoding="utf-8")
            documents.append({
                "id": f"kali-{tool}",
                "title": f"Kali Tools - {tool}",
                "framework": "kali",
                "source_type": "markdown",
                "language": "en",
                "path": f"data/raw/kali-tools/{filename}",
                "origin": url,
            })
            print(f"  OK ({len(text)} chars)")
        except error.HTTPError as exc:
            if exc.code == 404:
                print(f"  NOT FOUND (404), skipping")
            else:
                print(f"  FAILED: HTTP {exc.code}")
        except Exception as exc:
            print(f"  FAILED: {exc}")

        time.sleep(DELAY_BETWEEN_REQUESTS)

    return documents


_HT_BASE = "https://raw.githubusercontent.com/HackTricks-wiki/hacktricks/master/src"
_HT_LINUX_BASE = "https://raw.githubusercontent.com/HackTricks-wiki/hacktricks-linux/master/src"

HACKTRICKS_SECTIONS = {
    "pentesting-network": f"{_HT_BASE}/generic-methodologies-and-resources/pentesting-network/README.md",
    "pentesting-wifi": f"{_HT_BASE}/generic-methodologies-and-resources/pentesting-wifi/README.md",
    "pentesting-methodology": f"{_HT_BASE}/generic-methodologies-and-resources/pentesting-methodology.md",
    "sql-injection": f"{_HT_BASE}/pentesting-web/sql-injection/README.md",
    "xss": f"{_HT_BASE}/pentesting-web/xss-cross-site-scripting/README.md",
    "file-inclusion": f"{_HT_BASE}/pentesting-web/file-inclusion/README.md",
    "command-injection": f"{_HT_BASE}/pentesting-web/command-injection.md",
    "ssrf": f"{_HT_BASE}/pentesting-web/ssrf-server-side-request-forgery/README.md",
    "deserialization": f"{_HT_BASE}/pentesting-web/deserialization/README.md",
    "ssti": f"{_HT_BASE}/pentesting-web/ssti-server-side-template-injection/README.md",
    "xxe": f"{_HT_BASE}/pentesting-web/xxe-xee-xml-external-entity.md",
    "csrf": f"{_HT_BASE}/pentesting-web/csrf-cross-site-request-forgery.md",
    "privilege-escalation-linux": f"{_HT_BASE}/linux-hardening/privilege-escalation/README.md",
    "privilege-escalation-windows": f"{_HT_BASE}/windows-hardening/windows-local-privilege-escalation/README.md",
    "active-directory": f"{_HT_BASE}/windows-hardening/active-directory-methodology/README.md",
    "pentesting-ftp": f"{_HT_BASE}/network-services-pentesting/pentesting-ftp/README.md",
    "pentesting-ssh": f"{_HT_BASE}/network-services-pentesting/pentesting-ssh.md",
    "pentesting-smb": f"{_HT_BASE}/network-services-pentesting/pentesting-smb/README.md",
    "pentesting-rdp": f"{_HT_BASE}/network-services-pentesting/pentesting-rdp.md",
    "pentesting-web": f"{_HT_BASE}/network-services-pentesting/pentesting-web/README.md",
    "pentesting-mysql": f"{_HT_BASE}/network-services-pentesting/pentesting-mysql.md",
    "pentesting-smtp": f"{_HT_BASE}/network-services-pentesting/pentesting-smtp/README.md",
    "pentesting-mssql": f"{_HT_BASE}/network-services-pentesting/pentesting-mssql-microsoft-sql-server/README.md",
}


def download_hacktricks() -> list[dict[str, str]]:
    print("\n[HACKTRICKS] Downloading sections from GitHub...")
    dest_dir = RAW_DIR / "hacktricks"
    dest_dir.mkdir(parents=True, exist_ok=True)
    documents: list[dict[str, str]] = []

    for section_id, url in HACKTRICKS_SECTIONS.items():
        filename = f"{section_id}.md"
        dest = dest_dir / filename
        print(f"  {section_id} <- {url}")

        try:
            if not _download(url, dest):
                continue
            content = dest.read_text(encoding="utf-8")
            if len(content) < 100:
                print(f"  WARNING: content too short ({len(content)} chars), skipping")
                continue
            documents.append({
                "id": f"hacktricks-{section_id}",
                "title": f"HackTricks - {section_id.replace('-', ' ').title()}",
                "framework": "hacktricks",
                "source_type": "markdown",
                "language": "en",
                "path": f"data/raw/hacktricks/{filename}",
                "origin": url,
            })
            print(f"  OK ({len(content)} chars)")
        except Exception as exc:
            print(f"  FAILED: {exc}")
        time.sleep(DELAY_BETWEEN_REQUESTS)

    return documents


def build_manifest(all_documents: list[dict[str, str]]) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "document_count": len(all_documents),
        "documents": [
            {
                **doc,
                "ingestion_status": "discovered",
            }
            for doc in all_documents
        ],
    }

    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nManifest written: {MANIFEST_PATH} ({len(all_documents)} documents)")


def main() -> None:
    print("=" * 60)
    print("RAG Cyber Frameworks - Source Scraper")
    print("=" * 60)

    all_documents: list[dict[str, str]] = []

    all_documents.extend(scrape_ptes())
    all_documents.extend(download_nist())
    all_documents.extend(download_osstmm())
    all_documents.extend(download_owasp_wstg())
    all_documents.extend(scrape_kali_tools())
    all_documents.extend(download_hacktricks())

    build_manifest(all_documents)

    print("\n" + "=" * 60)
    print("Summary:")
    frameworks: dict[str, int] = {}
    for doc in all_documents:
        fw = doc["framework"]
        frameworks[fw] = frameworks.get(fw, 0) + 1
    for fw, count in sorted(frameworks.items()):
        print(f"  {fw}: {count} documents")
    print(f"  TOTAL: {len(all_documents)} documents")
    print("=" * 60)

    print("\nNext steps:")
    print("  python scripts/clean_documents.py")
    print("  python scripts/build_chunks.py")
    print("  python scripts/build_embeddings.py")
    print("  python scripts/build_vector_index.py")


if __name__ == "__main__":
    main()
