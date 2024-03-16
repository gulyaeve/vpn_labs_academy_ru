#!/usr/local/bin/python3
from getpass import getpass, getuser
from os import path
from subprocess import call, run
from threading import Thread, Event, Timer
from urllib.request import Request, urlopen


assert getuser() == "root", "Запустите скрипт при помощи sudo"
assert path.exists("/usr/local/sbin/sstpc"), "Не установлен sstp-client"

vpn_host = "labs.academy.ru"
vpn_login = input("Введите логин для vpn-соединения: ")
vpn_pass = getpass("Введите пароль для vpn-соединения (вводимые символы скрыты): ")

routes_path = "http://10.26.81.1/labs/access.txt"
vpn_sstp_command = (
    "/usr/local/sbin/sstpc "
    "--cert-warn "
    "--tls-ext "
    f"--user {vpn_login} "
    f"--password {vpn_pass} "
    f"--uuid {vpn_host} "
    f"{vpn_host} "
    "usepeerdns "
    "require-mschap-v2 "
    "noauth "
    "noipdefault "
    "noccp "
    "refuse-eap "
    "refuse-pap "
    "refuse-mschap "
)


def setup_routes():
    request = urlopen(Request(routes_path))
    routes = request.read().decode('utf-8')
    for route in routes.split("\n"):
        action = route.split()[0]
        if action == "ADD":
            address = route.split()[1]
            mask = route.split()[3]
            call(
                f"route -v add -net {address} -netmask {mask} -interface ppp0 &>/dev/null",
                shell=True,
            )
    print("Routes setup completed")
    print(f"You are now connected to {vpn_host}")
    print("To disconnect press Ctrl+C")


def sstp_connect():
    run(f"{vpn_sstp_command}", shell=True)


if __name__ == '__main__':
    event = Event()

    t1 = Thread(target=sstp_connect)
    t2 = Timer(2, setup_routes)
    t1.start()
    t2.start()

    try:
        print(f"Starting connection to {vpn_host}")
        event.wait()
    except KeyboardInterrupt:
        call("killall sstpc", shell=True)
        print("Connection closed")
