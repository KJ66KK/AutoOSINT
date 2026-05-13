import typer
from rich.console import Console
from rich.table import Table
from core.models import ModuleResult
from modules.email.breach_check import EmailBreachModule
from modules.domain.dns_recon import DNSReconModule
from modules.phone.carrier_lookup import CarrierLookupModule
from modules.username.social_scan import SocialScanModule

app = typer.Typer(help="AutoOSINT: A professional OSINT investigation tool.")
console = Console()

def display_results(result: ModuleResult):
    if result.success:
        table = Table(title=f"Results for {result.target}")
        table.add_column("Module", style="cyan")
        table.add_column("Confidence", style="magenta")
        table.add_column("Findings", style="green")
        
        # Displaying data as a string for now; you can make this prettier!
        findings = str(result.data)
        
        table.add_row(
            result.module_name, 
            result.confidence, 
            findings
        )
        console.print(table)
    else:
        console.print(f"[red]Error in {result.module_name}:[/red] {result.error}")

@app.command()
def email(target: str):
    """
    Scan an email address for breaches and leaks.
    """
    console.print(f"[bold blue]Searching OSINT data for email:[/bold blue] {target}...")
    checker = EmailBreachModule()
    display_results(checker.scan(target))

@app.command()
def domain(target: str):
    """
    Perform DNS reconnaissance and sub-domain enumeration.
    """
    console.print(f"[bold blue]Analyzing domain:[/bold blue] {target}...")
    checker = DNSReconModule()
    display_results(checker.scan(target))

@app.command()
def phone(target: str):
    """
    Lookup carrier and location info for a phone number.
    """
    console.print(f"[bold blue]Looking up phone number:[/bold blue] {target}...")
    checker = CarrierLookupModule()
    display_results(checker.scan(target))

@app.command()
def username(target: str):
    """
    Search for a username across social media platforms.
    """
    console.print(f"[bold blue]Scanning for username:[/bold blue] {target}...")
    checker = SocialScanModule()
    display_results(checker.scan(target))

if __name__ == "__main__":
    app()
