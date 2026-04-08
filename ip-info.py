import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def run_command(tool_name, command):
    console.print(f"\n[bold yellow][*] Launching {tool_name}...[/bold yellow]")
    console.print(f"[dim]Executing: {command}[/dim]\n")
    # Command ကို မောင်းနှင်ခြင်း
    os.system(command)
    console.print(f"\n[bold green][+] {tool_name} completed.[/bold green]")
    console.print("-" * 60)

def main():
    os.system('clear')
    
    # Header
    console.print(Panel.fit(
        "[bold red]🔱 MYANMAR TECH-AI: ULTIMATE RECON 🔱[/bold red]\n"
        "[white]Integrated Scanner: Subfinder | Nmap | Nikto | Nuclei[/white]",
        border_style="bold blue"
    ))

    # Target Input
    target = input("\n[?] Enter Domain or IP (e.g., google.com): ").strip()
    
    if not target:
        console.print("[bold red][!] Target is required![/bold red]")
        return

    # Workflow Table
    table = Table(title="Scan Strategy")
    table.add_column("Order", style="cyan")
    table.add_column("Tool", style="magenta")
    table.add_column("Task", style="green")
    
    table.add_row("1", "Subfinder", "Find Subdomains")
    table.add_row("2", "Nmap", "Service Fingerprinting")
    table.add_row("3", "Nikto", "Web Misconfiguration")
    table.add_row("4", "Nuclei", "Vulnerability Scanning")
    
    console.print(table)
    
    confirm = input("\n[!] Start automated scan? (y/n): ").lower()
    if confirm != 'y':
        return

    start_time = time.time()

    # --- Phase 1: Subfinder ---
    run_command("SUBFINDER", f"subfinder -d {target} -silent")

    # --- Phase 2: Nmap ---
    run_command("NMAP", f"nmap -sV -T4 {target}")

    # --- Phase 3: Nikto ---
    # သင်လက်ရှိရောက်နေတဲ့ folder အတိုင်း လမ်းကြောင်းပေးထားပါတယ်
    run_command("NIKTO", f"perl ~/nikto/program/nikto.pl -h {target}")

    # --- Phase 4: Nuclei ---
    run_command("NUCLEI", f"nuclei -u {target}")

    total_time = round(time.time() - start_time, 2)
    console.print(f"\n[bold green]✅ Scan Complete in {total_time}s.[/bold green]")

if __name__ == "__main__":
    main()