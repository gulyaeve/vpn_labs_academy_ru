#!/usr/local/bin/python3
from getpass import getpass, getuser
from os import path
from subprocess import call, run
from threading import Thread, Event, Timer
from urllib.request import Request, urlopen


# Если ваш путь к sstpc отличается, то замените его здесь:
sstpc_path = "/usr/local/sbin/sstpc"

vpn_host = "labs.academy.ru"
routes_path = "http://10.26.81.1/labs/access.txt"


assert getuser() == "root", "Запустите скрипт при помощи sudo"
assert path.exists(sstpc_path), "Не установлен sstp-client"


# Переменные vpn_login и vpn_pass можно заменить своими значениями, например:
# vpn_login = "my_login"
# vpn_pass = "my_pass"
vpn_login = input("Введите логин для vpn-соединения: ")
vpn_pass = getpass("Введите пароль для vpn-соединения (вводимые символы скрыты): ")

# Экранирование символов в пароле
vpn_pass = fr"{vpn_pass}"


vpn_sstp_command = (
    f"{sstpc_path} "
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
