import requests
import socket
import os
import sys
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track

console = Console()

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Not Found"

def check_ports(ip):
    # အရေးကြီးတဲ့ Port အချို့ကို စမ်းစစ်ခြင်း
    common_ports = [21, 22, 23, 25, 53, 80, 443, 3389]
    open_ports = []
    for port in common_ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))
        if result == 0:
            open_ports.append(str(port))
        s.close()
    return open_ports if open_ports else ["None Detected"]

def fetch_data(ip):
    # ပိုစုံတဲ့ API တစ်ခုကို ပြောင်းသုံးထားပါတယ် (ip-api.com)
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719")
        return response.json()
    except:
        return None

def main():
    clear()
    console.print(Panel.fit(
        "[bold red]🕵️ ADVANCED IP FIND [/bold red]\n"
        "[white] MADE BY THAW ZIN PHYO[/white]",
        border_style="red"
    ))

    target = input("\n[?] Target IP Address: ").strip()
    if not target:
        # ကိုယ့် IP ကိုယ်ကြည့်ရင်
        target = requests.get('https://api.ipify.org').text

    console.print(f"\n[bold yellow]🔍 Scanning {target}... Please wait.[/bold yellow]")

    # 1. Fetch IP Info
    data = fetch_data(target)
    if not data or data.get('status') == 'fail':
        console.print("[bold red]❌ Error: Invalid IP or No Data found.[/bold red]")
        return

    # 2. Reverse DNS
    rdns = get_reverse_dns(target)

    # 3. Port Scan (Lightweight)
    with console.status("[bold cyan]Scanning Common Ports...[/bold cyan]"):
        ports = check_ports(target)

    # --- Displaying Results ---
    
    # Basic Info Table
    info_table = Table(title="📍 GEOLOCATION & NETWORK INFO", show_header=True, header_style="bold green")
    info_table.add_column("Field", style="dim")
    info_table.add_column("Details")

    info_table.add_row("IP Address", data.get('query'))
    info_table.add_row("Hostname", rdns)
    info_table.add_row("Country", f"{data.get('country')} ({data.get('countryCode')})")
    info_table.add_row("Region/City", f"{data.get('regionName')}, {data.get('city')}")
    info_table.add_row("ISP", data.get('isp'))
    info_table.add_row("Organization", data.get('org'))
    info_table.add_row("AS Number", data.get('as'))
    info_table.add_row("Timezone", data.get('timezone'))
    
    console.print(info_table)

    # Security & Advanced Info
    sec_table = Table(title="🛡️ SECURITY & ADVANCED AUDIT", show_header=True, header_style="bold magenta")
    sec_table.add_column("Audit Type", style="dim")
    sec_table.add_column("Status")

    # VPN/Proxy Detection (Check by Hosting/Proxy flags)
    is_proxy = "YES [Alert]" if data.get('proxy') else "NO"
    is_mobile = "YES" if data.get('mobile') else "NO"
    is_hosting = "YES (Data Center)" if data.get('hosting') else "Residential / Personal"

    sec_table.add_row("Proxy/VPN Detected", f"[bold red]{is_proxy}[/bold red]" if data.get('proxy') else is_proxy)
    sec_table.add_row("Mobile Connection", is_mobile)
    sec_table.add_row("Network Type", is_hosting)
    sec_table.add_row("Open Ports", ", ".join(ports))
    
    console.print(sec_table)

    # Google Maps
    lat, lon = data.get('lat'), data.get('lon')
    console.print(Panel(f"[bold yellow]🔗 Google Maps Link:[/bold yellow] https://www.google.com/maps?q={lat},{lon}", border_style="blue"))

if __name__ == "__main__":
    main()
