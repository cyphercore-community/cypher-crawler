#!/usr/bin/env python3
"""
  ██████╗██╗   ██╗██████╗ ██╗  ██╗███████╗██████╗
 ██╔════╝╚██╗ ██╔╝██╔══██╗██║  ██║██╔════╝██╔══██╗
 ██║      ╚████╔╝ ██████╔╝███████║█████╗  ██████╔╝
 ██║       ╚██╔╝  ██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗
 ╚██████╗   ██║   ██║     ██║  ██║███████╗██║  ██║
  ╚═════╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

 ██████╗██████╗  █████╗ ██╗    ██╗██╗     ███████╗██████╗
██╔════╝██╔══██╗██╔══██╗██║    ██║██║     ██╔════╝██╔══██╗
██║     ██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝
██║     ██╔══██╗██╔══██║██║███╗██║██║     ██╔══╝  ██╔══██╗
╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗███████╗██║  ██║
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝

  Web Reconnaissance Tool | For authorized testing only
  GitHub: https://github.com/YOUR_USERNAME/cypher-crawler
"""

import argparse
import sys
import os
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich import print as rprint

from cypher_crawler.crawler import CypherCrawler
from cypher_crawler.reporter import save_json, save_csv, save_txt, print_summary_table
from cypher_crawler import __version__

console = Console()

BANNER = """[bold cyan]
  ██████╗██╗   ██╗██████╗ ██╗  ██╗███████╗██████╗     ██████╗██████╗  █████╗ ██╗    ██╗██╗     ███████╗██████╗
 ██╔════╝╚██╗ ██╔╝██╔══██╗██║  ██║██╔════╝██╔══██╗   ██╔════╝██╔══██╗██╔══██╗██║    ██║██║     ██╔════╝██╔══██╗
 ██║      ╚████╔╝ ██████╔╝███████║█████╗  ██████╔╝   ██║     ██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝
 ██║       ╚██╔╝  ██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗   ██║     ██╔══██╗██╔══██║██║███╗██║██║     ██╔══╝  ██╔══██╗
 ╚██████╗   ██║   ██║     ██║  ██║███████╗██║  ██║   ╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗███████╗██║  ██║
  ╚═════╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝
[/bold cyan]"""


def print_banner():
    console.print(BANNER)
    console.print(f"  [bold]Version:[/bold] {__version__}   [bold]Author:[/bold] Cypher Crawler Contributors")
    console.print(f"  [dim]⚠  Use only on systems you own or have explicit permission to test.[/dim]\n")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="cypher-crawler",
        description="Cypher Crawler — Web reconnaissance tool for authorized security testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cypher-crawler -u https://example.com
  cypher-crawler -u https://target.com -p 30 -d 3 --emails --forms --headers
  cypher-crawler -u https://target.com -o report --format json csv txt
  cypher-crawler -u https://target.com --no-robots --delay 1.0 --timeout 15
        """
    )

    # Target
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g. https://example.com)")

    # Crawl options
    crawl = parser.add_argument_group("Crawl options")
    crawl.add_argument("-p", "--pages", type=int, default=20, metavar="N", help="Max pages to crawl (default: 20)")
    crawl.add_argument("-d", "--depth", type=int, default=2, metavar="N", help="Crawl depth (default: 2)")
    crawl.add_argument("--delay", type=float, default=0.5, metavar="SEC", help="Delay between requests in seconds (default: 0.5)")
    crawl.add_argument("--timeout", type=int, default=10, metavar="SEC", help="Request timeout in seconds (default: 10)")
    crawl.add_argument("--user-agent", default="CypherCrawler/1.0 (Security Research)", help="Custom User-Agent string")
    crawl.add_argument("--no-robots", action="store_true", help="Ignore robots.txt (use responsibly)")
    crawl.add_argument("--all-domains", action="store_true", help="Crawl external domains too (off by default)")
    crawl.add_argument("--no-ssl-verify", action="store_true", help="Disable SSL certificate verification")

    # Extraction options
    extract = parser.add_argument_group("Extraction options")
    extract.add_argument("--emails", action="store_true", help="Extract email addresses")
    extract.add_argument("--forms", action="store_true", help="Detect and analyze HTML forms")
    extract.add_argument("--headers", action="store_true", help="Capture HTTP response headers")
    extract.add_argument("--no-links", action="store_true", help="Disable link extraction")

    # Output options
    output = parser.add_argument_group("Output options")
    output.add_argument("-o", "--output", metavar="NAME", help="Output filename base (without extension)")
    output.add_argument("--format", nargs="+", choices=["json", "csv", "txt"], default=["json"],
                        metavar="FORMAT", help="Output format(s): json csv txt (default: json)")
    output.add_argument("--output-dir", default=".", metavar="DIR", help="Output directory (default: current dir)")
    output.add_argument("--no-table", action="store_true", help="Skip printing summary table")

    parser.add_argument("-v", "--version", action="version", version=f"Cypher Crawler {__version__}")
    return parser


def main():
    print_banner()
    parser = build_parser()
    args = parser.parse_args()

    # Build config
    config = {
        "max_pages": args.pages,
        "max_depth": args.depth,
        "delay": args.delay,
        "timeout": args.timeout,
        "user_agent": args.user_agent,
        "respect_robots": not args.no_robots,
        "same_domain_only": not args.all_domains,
        "verify_ssl": not args.no_ssl_verify,
        "extract_links": not args.no_links,
        "extract_emails": args.emails,
        "detect_forms": args.forms,
        "capture_headers": args.headers,
    }

    console.print(Panel(
        f"[bold]Target:[/bold] {args.url}\n"
        f"[bold]Max pages:[/bold] {config['max_pages']}  "
        f"[bold]Depth:[/bold] {config['max_depth']}  "
        f"[bold]Delay:[/bold] {config['delay']}s\n"
        f"[bold]Emails:[/bold] {config['extract_emails']}  "
        f"[bold]Forms:[/bold] {config['detect_forms']}  "
        f"[bold]Robots.txt:[/bold] {config['respect_robots']}",
        title="[bold cyan]Cypher Crawler[/bold cyan]",
        border_style="cyan"
    ))

    crawler = CypherCrawler(config)
    results = crawler.crawl(args.url)

    if not results:
        console.print("[red]No results collected.[/red]")
        sys.exit(1)

    if not args.no_table:
        print_summary_table(results)

    # Save reports
    if args.output:
        os.makedirs(args.output_dir, exist_ok=True)
        base = os.path.join(args.output_dir, args.output)
        for fmt in args.format:
            path = f"{base}.{fmt}"
            if fmt == "json":
                save_json(results, path)
            elif fmt == "csv":
                save_csv(results, path)
            elif fmt == "txt":
                save_txt(results, path)
    else:
        console.print("\n[dim]Tip: Use -o <name> to save a report. E.g. -o report --format json csv txt[/dim]")

    console.print("\n[bold cyan]Cypher Crawler done.[/bold cyan] Stay ethical. 🔐")


if __name__ == "__main__":
    main()
