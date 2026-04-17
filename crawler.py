"""
Cypher Crawler - Core Crawling Engine
"""

import re
import time
import urllib.robotparser
from urllib.parse import urljoin, urlparse
from collections import deque
from dataclasses import dataclass, field
from typing import Optional

import requests
from bs4 import BeautifulSoup
from rich.console import Console

console = Console()


@dataclass
class PageResult:
    url: str
    status_code: Optional[int] = None
    title: str = ""
    links: list = field(default_factory=list)
    emails: list = field(default_factory=list)
    forms: list = field(default_factory=list)
    scripts: list = field(default_factory=list)
    stylesheets: list = field(default_factory=list)
    images: list = field(default_factory=list)
    headers: dict = field(default_factory=dict)
    content_type: str = ""
    error: Optional[str] = None
    depth: int = 0
    crawl_time: float = 0.0


class CypherCrawler:
    def __init__(self, config: dict):
        self.config = config
        self.visited = set()
        self.queue = deque()
        self.results: list[PageResult] = []
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": config.get("user_agent", "CypherCrawler/1.0 (Security Research)")
        })
        self.robots_parser = None
        self.base_domain = ""

    def can_fetch(self, url: str) -> bool:
        if not self.config.get("respect_robots", True):
            return True
        if self.robots_parser:
            return self.robots_parser.can_fetch("*", url)
        return True

    def load_robots(self, base_url: str):
        robots_url = urljoin(base_url, "/robots.txt")
        try:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            self.robots_parser = rp
            console.print(f"  [dim]robots.txt loaded from {robots_url}[/dim]")
        except Exception:
            console.print(f"  [dim]No robots.txt found[/dim]")

    def fetch(self, url: str) -> PageResult:
        result = PageResult(url=url)
        start = time.time()
        try:
            resp = self.session.get(
                url,
                timeout=self.config.get("timeout", 10),
                allow_redirects=True,
                verify=self.config.get("verify_ssl", True)
            )
            result.status_code = resp.status_code
            result.headers = dict(resp.headers)
            result.content_type = resp.headers.get("Content-Type", "")

            if "text/html" in result.content_type:
                soup = BeautifulSoup(resp.text, "html.parser")

                # Title
                title_tag = soup.find("title")
                result.title = title_tag.get_text(strip=True)[:120] if title_tag else ""

                # Links
                if self.config.get("extract_links", True):
                    for tag in soup.find_all("a", href=True):
                        href = tag["href"].strip()
                        if href and not href.startswith(("#", "javascript:", "mailto:")):
                            full = urljoin(url, href)
                            result.links.append(full)

                # Emails
                if self.config.get("extract_emails", False):
                    emails = re.findall(
                        r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
                        resp.text
                    )
                    result.emails = list(set(emails))

                # Forms
                if self.config.get("detect_forms", False):
                    for form in soup.find_all("form"):
                        result.forms.append({
                            "action": form.get("action", ""),
                            "method": form.get("method", "GET").upper(),
                            "inputs": [
                                {"name": i.get("name", ""), "type": i.get("type", "text")}
                                for i in form.find_all("input")
                            ]
                        })

                # Assets
                result.scripts = [
                    urljoin(url, s["src"])
                    for s in soup.find_all("script", src=True)
                ]
                result.stylesheets = [
                    urljoin(url, l["href"])
                    for l in soup.find_all("link", rel=True)
                    if "stylesheet" in l.get("rel", [])
                ]
                result.images = [
                    urljoin(url, i["src"])
                    for i in soup.find_all("img", src=True)
                ]

        except requests.exceptions.SSLError as e:
            result.error = f"SSL Error: {e}"
        except requests.exceptions.ConnectionError as e:
            result.error = f"Connection Error: {e}"
        except requests.exceptions.Timeout:
            result.error = "Timeout"
        except Exception as e:
            result.error = str(e)

        result.crawl_time = round(time.time() - start, 2)
        return result

    def crawl(self, start_url: str):
        parsed = urlparse(start_url)
        self.base_domain = parsed.netloc
        max_pages = self.config.get("max_pages", 20)
        max_depth = self.config.get("max_depth", 2)
        delay = self.config.get("delay", 0.5)
        same_domain_only = self.config.get("same_domain_only", True)

        if self.config.get("respect_robots", True):
            self.load_robots(start_url)

        self.queue.append((start_url, 1))

        while self.queue and len(self.results) < max_pages:
            url, depth = self.queue.popleft()

            if url in self.visited:
                continue
            if not self.can_fetch(url):
                console.print(f"  [yellow]Blocked by robots.txt:[/yellow] {url}")
                continue

            self.visited.add(url)
            console.print(f"  [cyan][{depth}][/cyan] Crawling: [bold]{url[:80]}[/bold]")

            result = self.fetch(url)
            result.depth = depth
            self.results.append(result)

            if result.error:
                console.print(f"    [red]✗[/red] {result.error}")
            else:
                info = f"    [green]✓[/green] {result.status_code}"
                if result.title:
                    info += f" — {result.title[:50]}"
                info += f" ({result.crawl_time}s)"
                console.print(info)

                if result.emails:
                    console.print(f"    [yellow]Emails:[/yellow] {', '.join(result.emails[:5])}")
                if result.forms:
                    console.print(f"    [magenta]Forms:[/magenta] {len(result.forms)} found")

            # Queue discovered links
            if depth < max_depth:
                for link in result.links:
                    if link not in self.visited:
                        lp = urlparse(link)
                        if same_domain_only and lp.netloc != self.base_domain:
                            continue
                        self.queue.append((link, depth + 1))

            if delay > 0:
                time.sleep(delay)

        console.print(f"\n[bold green]Crawl complete.[/bold green] {len(self.results)} pages crawled.")
        return self.results
