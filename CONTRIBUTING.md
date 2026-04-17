# Contributing to Cypher Crawler

Thank you for your interest in contributing! Cypher Crawler is an open-source security tool built by and for the cybersecurity community. All skill levels are welcome.

---

## 🧭 Before You Start

- **Only use this tool on systems you own or have explicit permission to test.**
- Contributions must not add features designed to facilitate unauthorized access.
- Be respectful. This is a welcoming, collaborative project.

---

## 🛠️ How to Contribute

### 1. Fork the repository

Click **Fork** on the top right of the GitHub page, then clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/cypher-crawler.git
cd cypher-crawler
```

### 2. Create a branch

Name your branch clearly:

```bash
git checkout -b feature/header-analyzer
# or
git checkout -b fix/timeout-bug
# or
git checkout -b docs/improve-readme
```

### 3. Set up your dev environment (Kali Linux)

```bash
pip install -r requirements.txt
pip install -e .
pip install pytest
```

### 4. Make your changes

- Follow the existing code style (PEP 8)
- Add comments where the logic isn't obvious
- Write or update tests in `tests/` if you add new functionality

### 5. Test your changes

```bash
pytest tests/
```

### 6. Commit with a clear message

```bash
git add .
git commit -m "feat: add HTTP header security analyzer"
```

Use prefixes: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`

### 7. Push and open a Pull Request

```bash
git push origin feature/header-analyzer
```

Then open a Pull Request on GitHub. Fill in the PR template explaining:
- What the change does
- Why it's useful
- How to test it

---

## 💡 Good First Issues

Look for issues tagged `good first issue` on GitHub. Some ideas:

| Area | Ideas |
|------|-------|
| **Features** | Subdomain enumeration, proxy/Tor support, CMS fingerprinting |
| **Output** | HTML report, color-coded terminal output |
| **Analysis** | Missing security header detector, JS endpoint parser |
| **Performance** | Multi-threading / async crawling |
| **Tests** | Add unit tests for `crawler.py`, mock HTTP responses |
| **Docs** | Better examples, wiki pages, video walkthrough |

---

## 📂 Project Structure

```
cypher-crawler/
├── cypher_crawler/
│   ├── __init__.py       # Version info
│   ├── main.py           # CLI + banner
│   ├── crawler.py        # Core engine — CypherCrawler class
│   └── reporter.py       # Report generators
├── tests/
│   └── test_crawler.py
├── requirements.txt
├── setup.py
├── CONTRIBUTING.md
└── README.md
```

**Where to add new things:**
- New extractor (e.g. subdomain finder) → new file `cypher_crawler/subdomain.py`, import in `main.py`
- New output format → add function in `reporter.py`
- New CLI flag → add in `build_parser()` in `main.py`, pass to `config` dict

---

## ✅ Code Standards

- Python 3.9+
- PEP 8 formatting (use `black` if you'd like: `pip install black && black .`)
- Type hints encouraged
- Docstrings for public classes and functions
- No hardcoded credentials, tokens, or IPs

---

## 🐛 Reporting Bugs

Open an issue with:
1. What you ran (command + flags)
2. What you expected
3. What actually happened (paste the error)
4. Your OS and Python version

---

## 📜 License

By contributing, you agree your code will be released under the [MIT License](LICENSE).

---

Thank you for making Cypher Crawler better! 🔐
