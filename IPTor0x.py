import requests
from jinja2 import Template
from colorama import Fore, Style, init
import concurrent.futures

init(autoreset=True)

# Application logo
def print_logo():
    logo = r"""
██╗██████╗ ████████╗ ██████╗ ██████╗  ██████╗ ██╗  ██╗
██║██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗██╔═████╗╚██╗██╔╝
██║██████╔╝   ██║   ██║   ██║██████╔╝██║██╔██║ ╚███╔╝ 
██║██╔═══╝    ██║   ██║   ██║██╔══██╗████╔╝██║ ██╔██╗ 
██║██║        ██║   ╚██████╔╝██║  ██║╚██████╔╝██╔╝ ██╗
╚═╝╚═╝        ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═                                             
    by corvus0x
    
    """
    print(Fore.CYAN + logo + Style.RESET_ALL)

def get_tor_exit_nodes():
    """Downloads the list of TOR exit nodes from the official site."""
    url = "https://check.torproject.org/torbulkexitlist"
    try:
        response = requests.get(url, timeout=5)
        return set(response.text.splitlines())
    except requests.RequestException:
        return set()

def load_ip_list(file_path):
    """Loads the list of IPs from a file."""
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def check_ip(ip, tor_exit_nodes):
    """Checks if an IP is in the TOR exit node list."""
    return ip if ip in tor_exit_nodes else None

def generate_html_report(tor_ips, non_tor_ips, total_ips):
    """Generates an HTML report with the results."""
    tor_count = len(tor_ips)
    tor_percentage = round((tor_count / total_ips) * 100, 2) if total_ips > 0 else 0

    template = Template(""" 
    <html>
    <head>
        <title>IPTor0x Report</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px;
                background-color: #f4f4f9; 
                color: #333;
            }
            h1 {
                color: #444;
                text-align: center;
                margin-top: 20px;
                font-size: 48px;
                font-weight: 900;
            }
            h1::after {
                content: '';
                display: block;
                width: 50px;
                margin: 10px auto;
                border-bottom: 3px solid #444;
            }
            h2 { 
                color: #333; 
                margin-top: 30px; 
                font-size: 24px;
                padding: 10px;
            }
            .info-section, .tor-section, .non-tor-section {
                width: 90%;
                margin: 30px auto;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                background-color: white;
            }
            .info-section {
                background-color: #f8f9fa;
                border-left: 5px solid #007bff;
            }
            .tor-section {
                border-left: 5px solid #dc3545;
            }
            .non-tor-section {
                border-left: 5px solid #28a745;
            }
            table { 
                width: 100%; 
                border-collapse: collapse; 
                margin-top: 20px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            th, td { 
                border: 1px solid #ddd; 
                padding: 7px; 
                text-align: center; 
            }
            .tor-table th { 
                background-color: rgba(220, 53, 69, 0.2); 
                color: #000;
                font-size: 18px;
            }
            .non-tor-table th { 
                background-color: rgba(40, 167, 69, 0.2); 
                color: #000;
                font-size: 18px;
            }
            td { 
                font-size: 16px; 
                color: #000; 
            }
            .tor-node { 
                background-color: transparent; 
                font-weight: bold; 
            }
            .tor-node a {
                background: linear-gradient(45deg, #AEC6CF, #b0b0b0); /* Pastel gray gradient */
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                text-decoration: none;
                font-size: 14px;
                display: inline-block;
                transition: background 0.3s ease-in-out;
            }

            .tor-node a:hover {
                background: linear-gradient(45deg, #b0b0b0, #8c8c8c); /* Darker pastel gray on hover */
            }

            footer {
                text-align: center;
                padding: 20px;
                margin-top: 30px;
                font-size: 14px;
                background-color: #333;
                color: white;
            }

        </style>
    </head>
    <body>
        <h1>IPTor0x Report</h1>

        <div class="info-section">
            <h2>General Information</h2>
            <p><strong>Total IPs analyzed:</strong> {{ total_ips }}</p>
            <p><strong>Total IPs that are TOR nodes:</strong> {{ tor_count }}</p>
            <p><strong>Percentage of IPs that are TOR nodes:</strong> {{ tor_percentage }}%</p>
        </div>

        <div class="tor-section">
            <h2>IPs detected as TOR nodes</h2>
            <table class="tor-table">
                <tr><th>IP</th><th>AbuseIPDB</th></tr>
                {% for ip in tor_ips %}
                    <tr class="tor-node">
                        <td>{{ ip }}</td>
                        <td><a href="https://www.abuseipdb.com/check/{{ ip }}" target="_blank">View Info</a></td>
                    </tr>
                {% endfor %}
            </table>
        </div>

        <div class="non-tor-section">
            <h2>IPs that are not TOR nodes</h2>
            <table class="non-tor-table">
                <tr><th>IP</th></tr>
                {% for ip in non_tor_ips %}
                    <tr>
                        <td>{{ ip }}</td>
                    </tr>
                {% endfor %}
            </table>
        </div>

    </body>
    </html>
    """)


    # Generate the HTML and save it to a file
    html_content = template.render(tor_ips=tor_ips, non_tor_ips=non_tor_ips, tor_count=tor_count, tor_percentage=tor_percentage, total_ips=total_ips)
    with open("report_IPTor0x.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def main():
    print_logo()
    tor_exit_nodes = get_tor_exit_nodes()
    ip_list = load_ip_list("IPs.txt")
    tor_ips = []
    non_tor_ips = []
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda ip: check_ip(ip, tor_exit_nodes), ip_list))
    
    for ip, result in zip(ip_list, results):
        if result:
            tor_ips.append(ip)
        else:
            non_tor_ips.append(ip)
    
    if tor_ips:
        print(Fore.YELLOW + Style.BRIGHT + "The following IPs are TOR exit nodes:")
        for ip in tor_ips:
            print(Fore.RED + Style.BRIGHT + f"{ip}")
        print()
    else:
        print(Fore.GREEN + Style.BRIGHT + "No IPs found that are TOR exit nodes.")
    
    generate_html_report(tor_ips, non_tor_ips, len(ip_list))
    print(Fore.CYAN + Style.BRIGHT + "[INFO] Report generated: " + Fore.LIGHTBLUE_EX + "report_IPTor0x.html")

if __name__ == "__main__":
    main()
