import os
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class UltimateRecon:
    def __init__(self, target):
        self.target = target
        # Folder name based on target to save results
        self.folder = f"results_{target.replace('.', '_')}"
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def run_command(self, tool_name, command):
        console.print(f"\n[bold yellow][*] Running {tool_name}...[/bold yellow]")
        try:
            # Run the system command
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            # Save output to file
            with open(f"{self.folder}/{tool_name}.txt", "w") as f:
                f.write(stdout.decode())
            
            console.print(f"[bold green][+] {tool_name} completed. Results saved in {self.folder}/{tool_name}.txt[/bold green]")
        except Exception as e:
            console.print(f"[bold red][!] Error running {tool_name}: {e}[/bold red]")

    def full_scan(self):
        # 1. Subfinder (Subdomain Discovery)
        self.run_command("Subfinder", f"subfinder -d {self.target} -silent")

        # 2. Nmap (Service Enumeration)
        # -sV: Version detection, -T4: Fast timing, -F: Top 100 ports
        self.run_command("Nmap", f"nmap -sV -T4 {self.target}")

        # 3. Nikto (Web Vulnerability Scan)
        self.run_command("Nikto", f"nikto -h {self.target} -Tuning 123")

        # 4. Nuclei (Advanced Template-based Scanning)
        self.run_command("Nuclei", f"nuclei -u {self.target} -severity low,medium,high,critical")

def main():
    os.system('clear')
    console.print(Panel.fit(
        "[bold red]🔱 ULTIMATE EXPLOIT AUTOMATION FRAMEWORK 🔱[/bold red]\n"
        "[white]Integrating: Nmap | Nikto | Subfinder | Nuclei[/white]",
        border_style="red"
    ))

    target = input("\n[?] Enter Target Domain (e.g., example.com): ").strip()
    
    if not target:
        console.print("[red]Target is required![/red]")
        return

    recon = UltimateRecon(target)
    
    table = Table(title="Scan Modules Activated")
    table.add_column("Tool", style="cyan")
    table.add_column("Purpose", style="magenta")
    table.add_row("Subfinder", "Finding hidden subdomains")
    table.add_row("Nmap", "Service & Port fingerprinting")
    table.add_row("Nikto", "Web server misconfiguration check")
    table.add_row("Nuclei", "Automated vulnerability detection")
    console.print(table)

    confirm = input("\n[!] Start full automation? (y/n): ")
    if confirm.lower() == 'y':
        recon.full_scan()
        console.print(f"\n[bold green]🔥 All scans complete. Check the '{recon.folder}' folder for details.[/bold green]")
    else:
        console.print("[yellow]Scan cancelled.[/yellow]")

if __name__ == "__main__":
    main()