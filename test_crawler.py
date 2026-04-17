"""
Cypher Crawler - Unit Tests
Run with: pytest tests/
"""

import pytest
from unittest.mock import patch, MagicMock
from cypher_crawler.crawler import CypherCrawler, PageResult


SAMPLE_HTML = """
<html>
<head><title>Test Page</title></head>
<body>
  <a href="/about">About</a>
  <a href="/contact">Contact</a>
  <a href="https://external.com">External</a>
  <form action="/login" method="POST">
    <input type="text" name="username">
    <input type="password" name="password">
  </form>
  <p>Contact us at admin@example.com or info@example.com</p>
  <script src="/static/app.js"></script>
  <link rel="stylesheet" href="/static/style.css">
  <img src="/images/logo.png">
</body>
</html>
"""

DEFAULT_CONFIG = {
    "max_pages": 5,
    "max_depth": 2,
    "delay": 0,
    "timeout": 5,
    "user_agent": "TestAgent",
    "respect_robots": False,
    "same_domain_only": True,
    "verify_ssl": True,
    "extract_links": True,
    "extract_emails": True,
    "detect_forms": True,
    "capture_headers": True,
}


def make_mock_response(html=SAMPLE_HTML, status=200, content_type="text/html"):
    mock = MagicMock()
    mock.status_code = status
    mock.text = html
    mock.ok = status < 400
    mock.headers = {"Content-Type": content_type, "Server": "nginx"}
    return mock


class TestPageResult:
    def test_defaults(self):
        r = PageResult(url="https://example.com")
        assert r.url == "https://example.com"
        assert r.status_code is None
        assert r.links == []
        assert r.emails == []
        assert r.forms == []
        assert r.error is None


class TestCrawlerFetch:
    def setup_method(self):
        self.crawler = CypherCrawler(DEFAULT_CONFIG)

    @patch("cypher_crawler.crawler.requests.Session.get")
    def test_fetch_ok(self, mock_get):
        mock_get.return_value = make_mock_response()
        result = self.crawler.fetch("https://example.com")
        assert result.status_code == 200
        assert result.title == "Test Page"
        assert result.error is None

    @patch("cypher_crawler.crawler.requests.Session.get")
    def test_extracts_links(self, mock_get):
        mock_get.return_value = make_mock_response()
        result = self.crawler.fetch("https://example.com")
        assert any("about" in l for l in result.links)
        assert any("contact" in l for l in result.links)

    @patch("cypher_crawler.crawler.requests.Session.get")
    def test_extracts_emails(self, mock_get):
        mock_get.return_value = make_mock_response()
        result = self.crawler.fetch("https://example.com")
        assert "admin@example.com" in result.emails
        assert "info@example.com" in result.emails

    @patch("cypher_crawler.crawler.requests.Session.get")
    def test_detects_forms(self, mock_get):
        mock_get.return_value = make_mock_response()
        result = self.crawler.fetch("https://example.com")
        assert len(result.forms) == 1
        assert result.forms[0]["method"] == "POST"
        assert result.forms[0]["action"] == "/login"

    @patch("cypher_crawler.crawler.requests.Session.get")
    def test_extracts_assets(self, mock_get):
        mock_get.return_value = make_mock_response()
        result = self.crawler.fetch("https://example.com")
        assert any("app.js" in s for s in result.scripts)
        assert any("style.css" in s for s in result.stylesheets)
        assert any("logo.png" in s for s in result.images)

    @patch("cypher_crawler.crawler.requests.Session.get")
    def test_handles_timeout(self, mock_get):
        import requests
        mock_get.side_effect = requests.exceptions.Timeout()
        result = self.crawler.fetch("https://example.com")
        assert result.error == "Timeout"
        assert result.status_code is None

    @patch("cypher_crawler.crawler.requests.Session.get")
    def test_handles_connection_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError("refused")
        result = self.crawler.fetch("https://example.com")
        assert result.error is not None
        assert "Connection" in result.error


class TestRobots:
    def test_can_fetch_without_robots(self):
        config = {**DEFAULT_CONFIG, "respect_robots": False}
        c = CypherCrawler(config)
        assert c.can_fetch("https://example.com/admin") is True

    def test_can_fetch_with_no_parser(self):
        config = {**DEFAULT_CONFIG, "respect_robots": True}
        c = CypherCrawler(config)
        c.robots_parser = None
        assert c.can_fetch("https://example.com/anything") is True
