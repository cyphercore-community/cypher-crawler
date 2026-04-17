# 🕷️ Cypher Crawler

> Web reconnaissance tool for authorized security testing — built for Kali Linux

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?logo=kalilinux)](https://kali.org)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen)](CONTRIBUTING.md)

---

## ⚠️ Disclaimer

**Cypher Crawler is intended for authorized security testing, penetration testing, and educational purposes only.**  
Scanning systems without explicit permission is **illegal** and may violate laws such as the Computer Fraud and Abuse Act (CFAA) or the Computer Misuse Act.  
The developers are **not responsible** for any misuse.

---

## 📖 What is Cypher Crawler?

Cypher Crawler is a fast, extensible Python-based web crawler designed for cybersecurity professionals and students. It maps a target website's structure, extracts useful reconnaissance data, and exports it in multiple formats — all from your terminal on Kali Linux.

### What it collects:
- All internal and external links
- HTML forms (method, action, inputs)
- Email addresses
- JavaScript, CSS, and image assets
- HTTP response headers (Server, X-Powered-By, CSP, etc.)
- Status codes and page titles

---

## 🚀 Installation

### Kali Linux (recommended)

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/cypher-crawler.git
cd cypher-crawler

# Install dependencies
pip install -r requirements.txt

# Install as a CLI tool
pip install -e .
```

### Quick run (no install)

```bash
git clone https://github.com/YOUR_USERNAME/cypher-crawler.git
cd cypher-crawler
pip install -r requirements.txt
python -m cypher_crawler.main -u https://example.com
```

---

## 🧪 Usage

```
cypher-crawler -u <TARGET_URL> [OPTIONS]
```

### Basic crawl

```bash
cypher-crawler -u https://example.com
```

### Full recon with all extractors

```bash
cypher-crawler -u https://target.com -p 50 -d 3 --emails --forms --headers
```

### Save reports in all formats

```bash
cypher-crawler -u https://target.com -o my_report --format json csv txt --output-dir ./reports
```

### Ignore robots.txt (use responsibly)

```bash
cypher-crawler -u https://target.com --no-robots --delay 1.0
```

---

## ⚙️ Options Reference

| Flag | Description | Default |
|------|-------------|---------|
| `-u`, `--url` | Target URL (**required**) | — |
| `-p`, `--pages` | Max pages to crawl | `20` |
| `-d`, `--depth` | Crawl depth | `2` |
| `--delay` | Delay between requests (seconds) | `0.5` |
| `--timeout` | Request timeout (seconds) | `10` |
| `--user-agent` | Custom User-Agent string | `CypherCrawler/1.0` |
| `--emails` | Extract email addresses | off |
| `--forms` | Detect HTML forms | off |
| `--headers` | Capture HTTP response headers | off |
| `--no-robots` | Ignore robots.txt | off |
| `--all-domains` | Follow external links too | off |
| `--no-ssl-verify` | Skip SSL verification | off |
| `-o`, `--output` | Output filename base | — |
| `--format` | Output format(s): `json` `csv` `txt` | `json` |
| `--output-dir` | Directory for output files | `.` |

---

## 📁 Project Structure

```
cypher-crawler/
├── cypher_crawler/
│   ├── __init__.py       # Version info
│   ├── main.py           # CLI entry point + banner
│   ├── crawler.py        # Core crawl engine
│   └── reporter.py       # JSON / CSV / TXT report generator
├── tests/
│   └── test_crawler.py   # Unit tests
├── requirements.txt
├── setup.py
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

## 📊 Output Example

```
  Target: https://example.com
  Max pages: 20  Depth: 2  Delay: 0.5s

  [1] Crawling: https://example.com
    ✓ 200 — Example Domain (0.43s)
  [2] Crawling: https://example.com/about
    ✓ 200 — About Us (0.38s)
    Emails: contact@example.com
    Forms: 1 found
  ...

  Crawl complete. 12 pages crawled.

  ┌─────────────────────────────────────────────┐
  │ URL          Status  Title    Links  Forms   │
  ├─────────────────────────────────────────────┤
  │ /            200     Example  14     0       │
  │ /about       200     About    7      1       │
  └─────────────────────────────────────────────┘
```

---

## 🤝 Contributing

We welcome contributions from the security community! See [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

**Ways to contribute:**
- 🐛 Bug reports and fixes
- ✨ New features (e.g. subdomain finder, header analyzer, JS parser)
- 📖 Documentation improvements
- 🧪 Tests and CI

---

## 🗺️ Roadmap

- [ ] Subdomain enumeration module
- [ ] HTTP header security analyzer (missing CSP, HSTS, etc.)
- [ ] JavaScript endpoint extractor
- [ ] WordPress/CMS fingerprinting
- [ ] Multi-threading support
- [ ] Proxy/Tor support
- [ ] HTML report output
- [ ] Integration with Shodan API

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

Built with:
- [Requests](https://requests.readthedocs.io/) — HTTP library
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — HTML parsing
- [Rich](https://github.com/Textualize/rich) — Terminal formatting

---

<p align="center">Made with 🔐 by the Cypher Crawler Contributors</p>
