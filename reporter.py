"""
Cypher Crawler - Report Generator
Outputs results as JSON, CSV, or plain text
"""

import json
import csv
import os
from datetime import datetime
from dataclasses import asdict
from rich.console import Console
from rich.table import Table

console = Console()


def save_json(results, output_path: str):
    data = {
        "generated": datetime.now().isoformat(),
        "tool": "Cypher Crawler v1.0.0",
        "total_pages": len(results),
        "pages": [asdict(r) for r in results],
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    console.print(f"[green]JSON report saved:[/green] {output_path}")


def save_csv(results, output_path: str):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["URL", "Status", "Title", "Links", "Emails", "Forms", "Scripts", "Depth", "Time(s)", "Error"])
        for r in results:
            writer.writerow([
                r.url, r.status_code, r.title,
                len(r.links), len(r.emails), len(r.forms),
                len(r.scripts), r.depth, r.crawl_time, r.error or ""
            ])
    console.print(f"[green]CSV report saved:[/green] {output_path}")


def save_txt(results, output_path: str):
    lines = [
        "=" * 70,
        "  CYPHER CRAWLER - CRAWL REPORT",
        f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"  Total pages: {len(results)}",
        "=" * 70,
        ""
    ]
    all_emails = set()
    all_forms = []

    for r in results:
        lines.append(f"[{'OK' if not r.error else 'ERR'}] {r.url}")
        lines.append(f"  Status : {r.status_code or 'N/A'}")
        lines.append(f"  Title  : {r.title or '(none)'}")
        lines.append(f"  Links  : {len(r.links)}  |  Forms: {len(r.forms)}  |  Scripts: {len(r.scripts)}")
        if r.emails:
            lines.append(f"  Emails : {', '.join(r.emails)}")
            all_emails.update(r.emails)
        if r.error:
            lines.append(f"  Error  : {r.error}")
        lines.append("")
        all_forms.extend(r.forms)

    lines += [
        "=" * 70,
        "  SUMMARY",
        "=" * 70,
        f"  Emails found    : {len(all_emails)}",
        f"  Forms found     : {len(all_forms)}",
    ]
    if all_emails:
        lines.append(f"  Email list      : {', '.join(all_emails)}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    console.print(f"[green]Text report saved:[/green] {output_path}")


def print_summary_table(results):
    table = Table(title="Cypher Crawler — Results Summary", show_lines=True)
    table.add_column("URL", style="cyan", max_width=50, no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Title", max_width=30)
    table.add_column("Links", justify="right")
    table.add_column("Forms", justify="right")
    table.add_column("Emails", justify="right")

    for r in results:
        status_style = "green" if r.status_code and 200 <= r.status_code < 300 else "red"
        table.add_row(
            r.url[:50],
            f"[{status_style}]{r.status_code or 'ERR'}[/{status_style}]",
            r.title[:30] if r.title else "[dim]—[/dim]",
            str(len(r.links)),
            str(len(r.forms)),
            str(len(r.emails)),
        )
    console.print(table)
