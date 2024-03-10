# VPN-подключение к labs.academy.ru для MacOS
## Требования
- Python3
- sstp-client
## Установка
Установите python3 и sstp-client при помощи Homebrew:
1) Откройте терминал
2) Установите Homebrew, выполнив команду: `/bin/bash -c “$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)”` и дождитесь завершения
3) Установите необходимые пакеты: для этого выполните последовательно три команды:
   - `brew update`
   - `brew install wget`
   - `brew install python3`
   - `brew install sstp-client`
## Подключение
Запустите файл скрипта с правами администратора, для этого:
1) Откройте терминал в папке, где расположен файл `vpn_labs_academy_ru.py`
2) Добавьте право на выполнение: `chmod +x vpn_labs_academy_ru.py`
3) Запустите скрипт командой: `sudo ./vpn_labs_academy_ru.py`, потребуется ввести пароль от учетной записи
4) Введите логин и пароль для подключения
5) ***Подключение будет работать пока открыто данное окно терминала***
6) Чтобы отключиться, нажмите комбинацию клавиш `Ctrl+C`