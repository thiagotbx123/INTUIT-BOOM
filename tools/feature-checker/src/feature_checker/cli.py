"""Command-line interface for Feature Checker."""

import sys

import click
from rich.console import Console
from rich.table import Table

from .core.checker import FeatureChecker
from .utils.config import load_config

console = Console()


def print_banner():
    """Print CLI banner."""
    console.print()
    console.print("=" * 60, style="cyan")
    console.print("         FEATURE CHECKER - Health Check Framework", style="cyan bold")
    console.print("=" * 60, style="cyan")
    console.print()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Feature Checker - Automated health checks for demo environments."""
    pass


@cli.command()
@click.option("--product", "-p", required=True, help="Product to check (e.g., qbo)")
@click.option("--project", "-j", default=None, help="Specific project/environment")
@click.option("--check", "-c", default=None, help="Run specific check by ID")
@click.option("--dry-run", is_flag=True, help="Preview without taking screenshots")
@click.option("--format", "-f", default="excel", type=click.Choice(["excel", "json", "markdown"]))
def run(product: str, project: str, check: str, dry_run: bool, format: str):
    """Run health checks for a product."""
    print_banner()

    try:
        checker = FeatureChecker(product, project)
        console.print(f"Product: [bold]{product}[/bold]")
        console.print(f"Project: [bold]{project or 'all'}[/bold]")
        console.print()

        # Connect to browser
        console.print("Connecting to browser...", style="dim")
        checker.connect()
        console.print("[green]✓[/green] Browser connected")

        # Login
        console.print("Logging in...", style="dim")
        if checker.login():
            console.print("[green]✓[/green] Login successful")
        else:
            console.print("[red]✗[/red] Login failed", style="red")
            return

        # Run checks
        if check:
            # Run single check
            checks = [c for c in checker.product.checks if c.id == check]
            if not checks:
                console.print(f"[red]Check not found: {check}[/red]")
                return
            checker.run_all_checks(checks)
        else:
            # Run all checks
            checker.run_all_checks()

        # Print summary
        checker.print_summary()

        # Generate report
        if not dry_run:
            report_path = checker.generate_report(format)
            console.print(f"\n[green]Report saved:[/green] {report_path}")

        # Disconnect
        checker.disconnect()

    except FileNotFoundError as e:
        console.print(f"[red]Configuration not found: {e}[/red]")
        sys.exit(1)
    except ConnectionError as e:
        console.print(f"[red]Browser connection failed: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option("--product", "-p", required=True, help="Product to list checks for")
def list(product: str):
    """List available checks for a product."""
    print_banner()

    try:
        config = load_config()
        product_config = config.load_product(product)

        table = Table(title=f"Health Checks for {product}")
        table.add_column("#", style="dim")
        table.add_column("ID", style="cyan")
        table.add_column("Name")
        table.add_column("Type")
        table.add_column("Priority")

        for i, check in enumerate(product_config.checks, 1):
            priority_style = {
                "critical": "red",
                "high": "yellow",
                "medium": "",
                "low": "dim",
            }.get(check.priority, "")

            table.add_row(
                str(i),
                check.id,
                check.name,
                check.type,
                f"[{priority_style}]{check.priority}[/{priority_style}]"
                if priority_style
                else check.priority,
            )

        console.print(table)
        console.print(f"\nTotal: {len(product_config.checks)} checks")

    except FileNotFoundError:
        console.print(f"[red]Product not found: {product}[/red]")
        sys.exit(1)


@cli.command()
@click.option("--product", "-p", required=True, help="Product to generate report for")
@click.option("--format", "-f", default="excel", type=click.Choice(["excel", "json", "markdown"]))
def report(product: str, format: str):
    """Generate report from last run."""
    print_banner()
    console.print(f"Generating {format} report for {product}...")
    # Would load cached results and generate report


@cli.command()
def status():
    """Show configuration status."""
    print_banner()

    config = load_config()

    table = Table(title="Configuration Status")
    table.add_column("Setting")
    table.add_column("Value")
    table.add_column("Status")

    # Check paths
    table.add_row(
        "Evidence Directory",
        str(config.evidence_dir),
        "[green]✓[/green]" if config.evidence_dir.exists() else "[red]✗[/red]",
    )
    table.add_row(
        "Reports Directory",
        str(config.reports_dir),
        "[green]✓[/green]" if config.reports_dir.exists() else "[red]✗[/red]",
    )
    table.add_row(
        "Config Directory",
        str(config.config_dir),
        "[green]✓[/green]" if config.config_dir.exists() else "[red]✗[/red]",
    )

    # Check Chrome
    import os

    chrome_exists = os.path.exists(config.chrome_path)
    table.add_row(
        "Chrome Path",
        config.chrome_path[:50] + "...",
        "[green]✓[/green]" if chrome_exists else "[red]✗[/red]",
    )

    # Check alerting
    table.add_row(
        "Slack Alerts",
        "Configured" if config.slack_webhook_url else "Not configured",
        "[green]✓[/green]" if config.slack_webhook_url else "[dim]○[/dim]",
    )
    table.add_row(
        "Email Alerts",
        "Configured" if config.alert_email else "Not configured",
        "[green]✓[/green]" if config.alert_email else "[dim]○[/dim]",
    )

    console.print(table)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
