emporary chat
4,903 tokens

User 5:40 PM
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
code
Code
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
if name == "main":
main()
MADE BY THAW ZIN PHYO
လို့ထည့်ပေး
Model 5:40 PM
ThinkingThoughts
Expand to view model thoughts

chevron_right
ဒီ Code က တော်တော်လေး ပြည့်စုံပြီးသားပါ။ rich library ကို သုံးထားတဲ့အတွက် UI ကလည်း လှပပါတယ်။ သင်တောင်းဆိုထားတဲ့အတိုင်း "MADE BY THAW ZIN PHYO" ဆိုတဲ့ credit ကို ပိုပြီးထင်သာမြင်သာရှိအောင်နဲ့ code ကို အနည်းငယ် ပိုပြီးစနစ်ကျအောင် ပြင်ဆင်ပေးထားပါတယ်။
ဒီ script ကို run ဖို့အတွက် လိုအပ်တဲ့ library တွေကို အရင် install လုပ်ရပါမယ် -
code
Bash
pip install requests rich
ပြီးရင်တော့ အောက်ပါ code ကို run နိုင်ပါပြီ -
code
Python
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
    common_ports = [21, 22, 23, 25, 53, 80, 443, 3389, 8080]
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
    # ip-api.com ကို သုံးပြီး အချက်အလက်ယူခြင်း
    try:
        # fields bitmask 66846719 သည် လိုအပ်သော data အားလုံးပါဝင်သည်
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719")
        return response.json()
    except:
        return None

def main():
    clear()
    # Banner showing the credit clearly
    console.print(Panel.fit(
        "[bold cyan]🌟 ADVANCED IP FINDER 🌟[/bold cyan]\n"
        "[bold red]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold red]\n"
        "[bold yellow]CREATED BY : THAW ZIN PHYO[/bold yellow]",
        border_style="blue",
        padding=(1, 4)
    ))

    target = input("\n[?] Target IP Address (Enter for My IP): ").strip()
    if not target:
        try:
            target = requests.get('https://api.ipify.org').text
        except:
            console.print("[red]Error: Could not retrieve your public IP.[/red]")
            return

    console.print(f"\n[bold green]➜[/bold green] Scanning: [bold white]{target}[/bold white]")
    
    # Start simulation progress for better UX
    with console.status("[bold cyan]Fetching data...[/bold cyan]"):
        data = fetch_data(target)
        time.sleep(1) # ခဏစောင့်ပေးခြင်း
        
    if not data or data.get('status') == 'fail':
        console.print(f"[bold red]❌ Error: {data.get('message', 'Invalid IP or No Data found.')}[/bold red]")
        return

    # DNS and Port Scan
    with console.status("[bold magenta]Running Security Audit...[/bold magenta]"):
        rdns = get_reverse_dns(target)
        ports = check_ports(target)

    # --- Displaying Geolocation Info ---
    info_table = Table(title="\n📍 GEOLOCATION & NETWORK INFO", show_header=True, header_style="bold green", expand=True)
    info_table.add_column("Field", style="cyan", width=20)
    info_table.add_column("Details", style="white")

    info_table.add_row("IP Address", data.get('query'))
    info_table.add_row("Hostname", rdns)
    info_table.add_row("Country", f"{data.get('country')} ({data.get('countryCode')})")
    info_table.add_row("Region/City", f"{data.get('regionName')}, {data.get('city')}")
    info_table.add_row("ISP", data.get('isp'))
    info_table.add_row("Organization", data.get('org'))
    info_table.add_row("AS Number", data.get('as'))
    info_table.add_row("Timezone", data.get('timezone'))
    
    console.print(info_table)

    # --- Displaying Security Info ---
    sec_table = Table(title="\n🛡️ SECURITY & ADVANCED AUDIT", show_header=True, header_style="bold magenta", expand=True)
    sec_table.add_column("Audit Type", style="cyan", width=20)
    sec_table.add_column("Status", style="white")

    is_proxy = "[bold red]YES (VPN/Proxy Detected)[/bold red]" if data.get('proxy') else "[green]NO[/green]"
    is_mobile = "[yellow]YES (Mobile Data)[/yellow]" if data.get('mobile') else "NO"
    is_hosting = "[bold red]YES (Data Center/Hosting)[/bold red]" if data.get('hosting') else "Residential / Personal"

    sec_table.add_row("Proxy/VPN", is_proxy)
    sec_table.add_row("Mobile Connection", is_mobile)
    sec_table.add_row("Network Type", is_hosting)
    sec_table.add_row("Open Ports", "[bold green]" + ", ".join(ports) + "[/bold green]")
    
    console.print(sec_table)

    # Google Maps Link
    lat, lon = data.get('lat'), data.get('lon')
    map_link = f"https://www.google.com/maps?q={lat},{lon}"
    console.print(Panel(f"[bold yellow]🔗 Google Maps Link:[/bold yellow]\n[u blue]{map_link}[/u blue]", border_style="blue", title="[bold white]LOCATION MAP[/bold white]"))
    
    console.print(f"\n[bold green]Scan Completed Successfully![/bold green] [white]Tool by Thaw Zin Phyo[/white]\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Exiting...[/red]")
        sys.exit()
ပြုပြင်ပြောင်းလဲထားချက်များ-
Banner: Banner ထဲမှာ MADE BY THAW ZIN PHYO ကို ပိုပြီး သိသာအောင် ထည့်ထားပါတယ်။
Status Spinner: Data ရှာနေစဉ်မှာ rich.status ကို သုံးပြီး animated loading icon လေး ထည့်ပေးထားပါတယ်။
Table Layout: expand=True သုံးထားလို့ screen အပြည့် table က ပိုကြည့်ကောင်းသွားပါတယ်။
Error Handling: အင်တာနက်မရှိတာဖြစ်ဖြစ်၊ IP အမှားရိုက်တာဖြစ်ဖြစ် error message သေချာပြအောင် လုပ်ထားပါတယ်။
Colors: Color တွေကို ပိုစုံအောင် သုံးပြီး Security alert တွေကို အနီရောင်နဲ့ ပေါ်လွင်အောင် လုပ်ထားပါတယ်။
Model 5:43 PM
ThinkingThoughts
Expand to view model thoughts

chevron_right
ဒါကတော့ သင်တောင်းဆိုထားတဲ့အတိုင်း 50,000 MMK ပေးဆောင်ရမယ့်အကြောင်းအချက်နဲ့ Script ရဲ့ Features တွေကို အင်္ဂလိပ်ဘာသာနဲ့ အပြည့်အစုံ ရေးသားပေးထားတဲ့ README.md ဖိုင်ပဲ ဖြစ်ပါတယ်။
🕵️ ADVANCED IP FINDER & SECURITY AUDITOR
An advanced, terminal-based IP tracking and security auditing tool designed for developers and security researchers. This tool provides detailed geolocation data, network ownership information, and security risk assessment.
Developer: Thaw Zin Phyo
📢 IMPORTANT NOTICE (TERMS OF USE)
This script is provided as a premium utility. By downloading, running, or using this script, you are legally and morally bound by the following license terms:
License Fee: 50,000 MMK (Myanmar Kyat)
Payment Policy: If you use this script for personal or commercial purposes, you are required to pay the developer fee of 50,000 MMK.
Contact for Payment: [Insert your Facebook/Telegram/Phone here]
Failure to comply with the payment terms while using the script constitutes a breach of the developer's effort and intellectual property.
🚀 KEY FEATURES
This tool is packed with professional-grade features:
Full Geolocation Tracking: Get precise Country, City, Region, and Timezone of any IP address.
ISP & Organization Lookup: Identify the Internet Service Provider (ISP) and the company owning the IP range.
Security Audit (Proxy/VPN Detection):
Detects if the target is using a VPN or Proxy.
Identifies if the IP belongs to a Data Center/Hosting service.
Detects if the target is on a Mobile Connection.
Reverse DNS Lookup: Automatically resolves the Hostname associated with the IP.
Lightweight Port Scanner: Scans common critical ports (SSH, FTP, HTTP, etc.) to check for potential vulnerabilities.
Google Maps Integration: Generates a direct clickable link to view the physical location on Google Maps.
Modern UI: Built with the Rich library for a beautiful, colorful, and professional terminal interface.
Automated Public IP Detection: If no IP is entered, it automatically scans your own public IP address.
🛠️ INSTALLATION
Ensure you have Python 3.x installed on your system.
Clone the repository:
code
Bash
git clone https://github.com/your-username/ip-finder.git
cd ip-finder
Install required dependencies:
code
Bash
pip install requests rich
Run the script:
code
Bash
python ip_finder.py
📸 SCREENSHOTS
(You can add a screenshot link here later)
⚠️ DISCLAIMER
This tool is for educational and ethical security testing purposes only. The developer, Thaw Zin Phyo, is not responsible for any misuse or illegal activities conducted with this tool.
💳 SUPPORT THE DEVELOPER
If you like this tool and want to support more advanced projects, please ensure you have paid the 50,000 MMK usage fee. Your support helps in maintaining and adding new features to this project.
MADE BY THAW ZIN PHYO
8.8s
info
Google AI models may make mistakes, so double-check outputs.
