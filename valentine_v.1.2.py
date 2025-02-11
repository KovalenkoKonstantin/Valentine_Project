import tkinter as tk
import random
import time
import threading
import os
import sys
import winreg as reg
import pygetwindow as gw
import screeninfo
import locale
from datetime import datetime, timedelta

# 📌 Устанавливаем русскую локаль
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

# 📌 Константы
screen = screeninfo.get_monitors()[0]  # Берём первый монитор
SCREEN_WIDTH = screen.width
SCREEN_HEIGHT = screen.height

BG_COLOR = "white"  # Цвет фона
EXIT_BUTTON = ('q', 'й')    # Кнопки выхода из программы

FLOWER_NUMBER = 12    # Количество единовременно создаваемых цветков
MAX_FLOWER_SIZE = 100    # Максимальный размер цветков
FLOWER_COLORS = [
    "#FFC0CB",  # светло-розовый
    "#8A2BE2",  # синий с фиолетовым оттенком
    "#9400D3",  # темно-фиолетовый
    "#FFD700",  # золотой
    "#00FFFF",  # бирюзовый
    "#FFB6C1",  # очень светлый розовый
    "#4B0082",  # индиго
    "#C71585",  # яркий пурпурный
    "#FF8C00",  # оранжевый
    "#9932CC",  # темный фиолетовый
    "#FF6347",  # томатный красный
    "#DA70D6",  # орхидея
    "#D2691E",  # шоколадный
    "#B22222",  # огненно-красный
    "#FFDAB9",  # персиковый
    "#ADFF2F",  # желто-зеленый (лаймовый)
    "#48D1CC",  # средний бирюзовый
    "#C0C0C0",  # серебристый
    "#800080",  # пурпурный
    "#FA8072",  # светло-томатовое
    "#2E8B57",  # морская волна
    "#993366",  # бордовый с фиолетовым оттенком
    "#20B2AA",  # светлый морской зеленый
    "#D3D3D3",  # светло-серый
    "#00BFFF",  # глубокий голубой
    "#FF1493",  # яркий розовый (изначальный цвет)
]  # Цвета цветков

TEXT_FONT = "Arial"  # Шрифт
TEXT = f"С {datetime.fromtimestamp(time.time()).strftime("%d %B")}, {os.getlogin()}!"    # Надпись

# 📌 Словарь с программами
programs = {
    "Outlook": {"window_keyword": "Outlook", "process_name": "OUTLOOK.EXE"},
    "Telegram": {"window_keyword": "Telegram", "process_name": "Telegram.exe"},
}

# 🔄 Выбранная программа
selected_program = "Outlook"

# 📅 Дата запуска анимации
launch_date = datetime(datetime.now().year, 3, 8)  # Можно изменить на другую дату

# 📅 Время закрытия программы
close_time = {"hour": 23, "minute": 0}

# 📌 Максимальное одновременное количество цветочков на экране
max_flowers = 80

# 🚀 Флаг для выхода из программы
exit_flag = False

# 📌 Функция добавления в автозагрузку
def add_to_autostart():
    script_path = os.path.abspath(sys.argv[0])
    script_name = os.path.basename(script_path)
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"

    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_WRITE) as reg_key:
            reg.SetValueEx(reg_key, script_name, 0, reg.REG_SZ, script_path)
            print(f"Программа {script_name} добавлена в автозагрузку.")
    except Exception as e:
        print(f"Ошибка при добавлении в автозагрузку: {e}")

# ✅ Функция проверки автозагрузки
def check_autostart():
    script_name = os.path.basename(sys.argv[0])
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"

    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_READ) as reg_key:
            try:
                reg.QueryValueEx(reg_key, script_name)
            except FileNotFoundError:
                add_to_autostart()
    except Exception as e:
        print(f"Ошибка при проверке автозагрузки: {e}")

# ✅ Функция проверки работы программы триггера
def is_program_running(process_name):
    """Проверяет, запущен ли процесс с указанным именем."""
    output = os.popen(f'tasklist | findstr /I "{process_name}"').read()
    return process_name.lower() in output.lower()  # True, если процесс найден

# 📌 Функция закрытия программы триггера
def close_selected_program():
    """Закрывает выбранную программу, если она найдена в списке открытых окон."""
    program_data = programs[selected_program]  # Получаем настройки программы
    program_keyword = program_data["window_keyword"]
    process_name = program_data["process_name"]

    # 📌 Функция силового закрытия программы триггера
    def force_close_program(process_name):
        """Принудительно завершает процесс через taskkill."""
        print(f"Принудительное закрытие {selected_program}...")
        os.system(f'wmic process where name="{process_name}" call terminate')

    # Получаем список всех заголовков открытых окон
    all_windows = gw.getAllTitles()
    target_windows = [win for win in all_windows if program_keyword.lower() in win.lower()]

    if target_windows:
        # print(f"{selected_program} найден. Закрываю...")

        for win in target_windows:
            try:
                # Получаем объект окна и закрываем его
                win_obj = gw.getWindowsWithTitle(win)[0]
                win_obj.close()
                print(f"Закрыто окно: {win}")
            except Exception as e:
                print(f"Ошибка при закрытии {win}: {e}")
    else:
        print(f"Окно {selected_program} не найдено.")

        # Если окна нет, но процесс работает, принудительно закрываем его
        if is_program_running(process_name):
            print(f"{selected_program} работает в фоне. Завершаю процесс...")
            force_close_program(process_name)
        else:
            print(f"{selected_program} не найден среди процессов.")

# 💐 Функция анимации цветочков и текста
def create_flowerst():
    root = tk.Tk()  # Инициализируем главное окно
    root.title(TEXT)  # Устанавливаем заголовок окна
    root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")  # Устанавливаем размер окна
    root.configure(bg=BG_COLOR)  # Устанавливаем фон
    root.wm_attributes("-transparentcolor", BG_COLOR)  # Указываем выбранный цвет как прозрачный
    root.attributes("-topmost", True)  # Делаем окно всегда поверх других окон
    # root.overrideredirect(True)  # Удаляет стандартные кнопки закрытия, сворачивания и рамку окна

    # Создаем холст для рисования
    canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg=BG_COLOR, highlightthickness=0)
    canvas.pack()

    flowers = []

    def create_flower():
        """
            Создает новый цветочек на случайной позиции с случайным размером и цветом,
            добавляет его в список для анимации.
            """
        # flower_symbols = ["🌸", "🌺", "🌻", "🌼", "🌷", "🌹"]  # Список цветочных символов
        flower_symbols = ["🌸", "🌷", "🌻"]  # Список цветочных символов
        x = random.randint(50, SCREEN_WIDTH - 50)    # Случайная координата X в пределах окна
        y = random.randint(50, SCREEN_HEIGHT - 50)    # Случайная координата Y в пределах окна
        color = random.choice(FLOWER_COLORS)
        flower_size = random.randint(30, MAX_FLOWER_SIZE)  # Случайный размер сердца

        # Создаем основной цветок
        flower = canvas.create_text(x, y, text=random.choice(flower_symbols), font=(TEXT_FONT, flower_size), fill=color)
        # Добавляем цветочек в список для отслеживания общего количества
        # x, y - текущие координаты
        flowers.append((flower, x, y, random.uniform(-3, 3), random.uniform(-1, -3)))

    def adjust_flowers():
        """
            Управляет количеством цветочков на экране:
            1. Удаляет старые цветочки, если их больше 50.
            2. Создает новые цветочки.
            3. Запускает эту же функцию снова через 500 мс.
            """
        while len(flowers) > max_flowers:
            flower, *_ = flowers.pop(0)   # Удаляем самое старое сердце
            canvas.delete(flower)

        for _ in range(FLOWER_NUMBER):  # Создаем FLOWER_NUMBER новых сердец за раз
            create_flower()

        root.after(2000, adjust_flowers)  # Запускаем функцию снова через 500 мс

    # Получаем фокус на окно сразу после его создания
    root.focus_set()  # Это должно помочь программе получать клавиши

    # 📌 Функция выхода из программы при нажатии "q"/"й"
    def on_key(event):
        if event.char.lower() in EXIT_BUTTON:
            root.quit()     # Завершаем главный цикл tkinter
            sys.exit(0)  # Корректное завершение программы

    # Привязываем обработчик к окну
    root.bind("<Key>", on_key)

    # Запускаем создание и отслеживание количества цветков
    adjust_flowers()
    # Запускаем главный цикл приложения
    root.mainloop()

# 🔥 Функция старта программы
def start_valentine():

    while not exit_flag:
        current_time = datetime.now()

        # Проверяем, если сейчас время закрытия (за день до события)
        one_day_before = launch_date - timedelta(days=1)
        if (current_time.date() == one_day_before.date()
                and current_time.hour == close_time["hour"]
                and current_time.minute == close_time["minute"]):
            print(f"{close_time['hour']}:{close_time['minute']}. Проверяю {selected_program}...")
            close_selected_program()

        # Проверяем, если сегодня день запуска анимации
        if (current_time.date() == launch_date.date()
                and is_program_running(programs[selected_program]['process_name'])):
            print(f"Сегодня {launch_date.strftime('%d %B')}. Запускаю цветочки!")
            create_flowerst()
            break  # Останавливаем цикл после запуска анимации

        time.sleep(5)  # Проверяем каждые 5 секунд

# 📌 Проверяем автозапуск
check_autostart()

# 📌 Запускаем программу
start_valentine()

# 📌 Запускаем отслеживание программы в фоновом потоке
threading.Thread(target=start_valentine, daemon=True).start()

# close_selected_program()