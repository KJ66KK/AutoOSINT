from typing import List, Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from core.models import ModuleResult
from core.engine import ScannerEngine
from core.correlator import DataCorrelator
from core.formatter import export_to_json, export_to_csv

# Initialize Typer with a simpler structure
app = typer.Typer(
    help="""
    [bold cyan]AutoOSINT[/bold cyan] - A professional OSINT investigation tool.
    
    [bold underline]Usage Examples:[/bold underline]
    
    [yellow]1. Forced Target Flags (Mandatory):[/yellow]
    $ autoosint [bold]-e[/bold] admin@example.com   (Email)
    $ autoosint [bold]-d[/bold] target.com          (Domain)
    $ autoosint [bold]-u[/bold] username            (Username)
    $ autoosint [bold]-p[/bold] "(966)50XXXXXXX"    (Phone)
    
    [yellow]2. Deep Scanning (Pivoting):[/yellow]
    $ autoosint [bold]-u[/bold] johndoe [bold]-D[/bold] (or --deep)
    
    [yellow]3. Exporting Results:[/yellow]
    $ autoosint [bold]-d[/bold] google.com [bold]--export json[/bold]
    """,
    rich_markup_mode="rich"
)

console = Console()
engine = ScannerEngine()
correlator = DataCorrelator()

def display_results(results: List[ModuleResult], target: str):
    if not results:
        console.print(f"[yellow]No modules ran for target: {target}[/yellow]")
        return

    table = Table(title=f"Results for {target}", show_header=True, header_style="bold magenta")
    table.add_column("Module", style="cyan")
    table.add_column("Target", style="white")
    table.add_column("Status", style="bold")
    table.add_column("Confidence", style="magenta")
    table.add_column("Findings", style="green")
    
    for result in results:
        status_str = "[green]OK[/green]" if result.success else f"[red]FAIL: {result.error}[/red]"
        
        # Format findings for better readability
        if isinstance(result.data, dict):
            findings = "\n".join([f"[bold cyan]{k}:[/bold cyan] {v}" for k, v in result.data.items()])
        else:
            findings = str(result.data)
        
        if not result.success:
            findings = "N/A"
        
        table.add_row(
            result.module_name, 
            result.target,
            status_str,
            result.confidence, 
            findings
        )
    
    console.print(table)
    
    # Run Correlator
    analysis = correlator.analyze(results)
    if analysis["insights"]:
        insights_text = "\n".join([f"- {insight}" for insight in analysis["insights"]])
        console.print(Panel(insights_text, title="🧠 Correlator Insights", border_style="blue"))

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    email: Optional[str] = typer.Option(None, "-e", "--email", help="Scan an [bold]email[/bold] address"),
    domain: Optional[str] = typer.Option(None, "-d", "--domain", help="Scan a [bold]domain[/bold]"),
    username: Optional[str] = typer.Option(None, "-u", "--username", help="Scan a [bold]username[/bold]"),
    phone: Optional[str] = typer.Option(None, "-p", "--phone", help="Scan a [bold]phone number[/bold] (e.g. '(966)50XXXXXXX')"),
    deep: bool = typer.Option(False, "--deep", "-D", help="Deep scan: automatically follow linked data (e.g. input = email output = email + username,phone,domain)"),
    export: Optional[str] = typer.Option(None, "--export", help="Export format: [bold]json[/bold] or [bold]csv[/bold]"),
    version: bool = typer.Option(False, "--version", "-v", help="Show version info")
):
    """
    [bold cyan]AutoOSINT[/bold cyan]: Professional OSINT Investigation Tool.
    """
    if version:
        console.print("[bold cyan]AutoOSINT v0.1.0[/bold cyan]")
        raise typer.Exit()

    # If no flags are provided and no subcommand was called, show help
    if ctx.invoked_subcommand is None and not any([email, domain, username, phone]):
        console.print(Panel("[bold cyan]Welcome to AutoOSINT![/bold cyan]\n\nPlease specify a target type using a flag (e.g., [bold]-d google.com[/bold]).", border_style="cyan"))
        console.print(ctx.get_help())
        raise typer.Exit()

    if ctx.invoked_subcommand:
        return

    final_target = None
    target_type = None

    if email:
        final_target, target_type = email, "email"
    elif domain:
        final_target, target_type = domain, "domain"
    elif username:
        final_target, target_type = username, "username"
    elif phone:
        final_target, target_type = phone, "phone"

    if final_target:
        console.print(f"[bold blue]Target:[/bold blue] {final_target} ({target_type.upper()})")
        if deep:
            console.print("[bold yellow]Deep Scanning Enabled:[/bold yellow] Following linked data...")
        console.print(f"[bold blue]Initiating scan...[/bold blue]")
        
        results = engine.run_all(final_target, target_type, recursive=deep)
        display_results(results, final_target)

        if export:
            fmt = export.lower()
            if fmt == 'json':
                saved_to = export_to_json(results)
                console.print(f"[bold green]Results exported to {saved_to}[/bold green]")
            elif fmt == 'csv':
                saved_to = export_to_csv(results)
                console.print(f"[bold green]Results exported to {saved_to}[/bold green]")

if __name__ == "__main__":
    app()
