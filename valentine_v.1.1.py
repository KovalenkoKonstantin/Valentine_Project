import tkinter as tk
import random
import time
import threading
import os
import sys
import winreg as reg
import pygetwindow as gw
import math
import screeninfo
from datetime import datetime, timedelta

# 📌 Константы
screen = screeninfo.get_monitors()[0]  # Берём первый монитор
SCREEN_WIDTH = screen.width
SCREEN_HEIGHT = screen.height

BG_COLOR = "white"  # Цвет фона
EXIT_BUTTON = ('q', 'й')    # Кнопки выхода из программы

HEART_NUMBER = 7    # Количество единовременно создаваемых сердец
MAX_HEART_SIZE = 170    # Максимальный размер сердечек
HEART_COLORS = ["#FF1493", "#FF69B4", "#DB7093", "#FF00FF", "#FF007F"]  # Цвета сердец
SHADOW_COLOR = "#FFC0CB"  # Цвет тени сердец

TEXT_COLORS = ["#FFD700", "#FFFFFF", "#8B0000", "#191970"]  # Цвета текста
TEXT_SHADOW_COLOR = "black"  # Цвет тени текста
TEXT_SPEED = 0.05   # Скорость движения текста
TEXT = f"С днём Валентина, {os.getlogin()}!"    # Надпись
TEXT_FONT = "Arial"  # Шрифт
TEXT_SIZE = 50  # Размер шрифта
TEXT_WEIGHT = "bold"  # Толщина текста

# 📌 Словарь с программами
programs = {
    "Outlook": {"window_keyword": "Outlook", "process_name": "OUTLOOK.EXE"},
    "Telegram": {"window_keyword": "Telegram", "process_name": "Telegram.exe"},
}

# 🔄 Выбранная программа
selected_program = "Outlook"

# 📅 Дата запуска анимации
launch_date = datetime(datetime.now().year, 2, 14)  # Можно изменить на другую дату

# 📅 Время закрытия программы
close_time = {"hour": 23, "minute": 0}

# 📌 Максимальное одновременное количество сердечек на экране
max_hearts = 50

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

# 💖 Функция анимации сердечек и текста
def create_hearts_and_text():
    root = tk.Tk()  # Инициализируем главное окно
    root.title(TEXT)  # Устанавливаем заголовок окна
    root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")  # Устанавливаем размер окна
    root.configure(bg=BG_COLOR)  # Устанавливаем фон
    root.wm_attributes("-transparentcolor", BG_COLOR)  # Указываем выбранный цвет как прозрачный
    root.attributes("-topmost", True)  # Делаем окно всегда поверх других окон
    root.overrideredirect(True)  # Удаляет стандартные кнопки закрытия, сворачивания и рамку окна

    # Создаем холст для рисования
    canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg=BG_COLOR, highlightthickness=0)
    canvas.pack()

    hearts = []

    def create_heart():
        """
            Создает новое сердце на случайной позиции с случайным размером и цветом,
            добавляет его в список для анимации.
            """
        x = random.randint(50, SCREEN_WIDTH - 50)    # Случайная координата X в пределах окна
        y = random.randint(50, SCREEN_HEIGHT - 50)    # Случайная координата Y в пределах окна
        color = random.choice(HEART_COLORS)
        heart_size = random.randint(30, MAX_HEART_SIZE)  # Случайный размер сердца

        # Создаем тень для сердца, немного смещенную вниз и вправо
        shadow = canvas.create_text(x + 2, y + 2, text="❤️", font=(TEXT_FONT, heart_size), fill=SHADOW_COLOR)
        # Создаем основное сердце
        heart = canvas.create_text(x, y, text="❤️", font=(TEXT_FONT, heart_size), fill=color)
        # Добавляем сердце в список для последующей анимации
        # x, y - текущие координаты
        # dx, dy - случайные значения скорости по осям X и Y
        hearts.append((heart, shadow, x, y, random.uniform(-3, 3), random.uniform(-1, -3)))

    def animate_hearts():
        """
            Анимирует движение сердец вверх и немного в стороны.
            Если сердце выходит за границы экрана, оно удаляется из списка.
            """
        for i, (heart, shadow, x, y, dx, dy) in enumerate(hearts):
            y += dy # Смещаем сердце вверх (dy < 0)
            x += dx # Смещаем сердце в случайную сторону (dx может быть как +, так и -)

            # Обновляем координаты сердца и его тени
            canvas.coords(heart, x, y)
            canvas.coords(shadow, x + 2, y + 2)

            # Удаляем сердце, если оно вышло за границы экрана
            if y < -50 or x < -50 or x > SCREEN_WIDTH + 50:
                canvas.delete(heart)
                canvas.delete(shadow)
                hearts.pop(i)   # Удаляем элемент из списка

        # Повторяем анимацию каждые 50 миллисекунд
        root.after(50, animate_hearts)

    def adjust_hearts():
        """
            Управляет количеством сердец на экране:
            1. Удаляет старые сердца, если их больше 100.
            2. Создает новые сердца.
            3. Запускает эту же функцию снова через 200 мс.
            """
        while len(hearts) > max_hearts:
            heart, shadow, *_ = hearts.pop(0)   # Удаляем самое старое сердце
            canvas.delete(heart)
            canvas.delete(shadow)

        for _ in range(HEART_NUMBER):  # Создаем HEART_NUMBER новых сердец за раз
            create_heart()

        root.after(200, adjust_hearts)  # Запускаем функцию снова через 200 мс

    # Начальный угол движения текста (используется для синусоидального эффекта)
    angle = 0
    amplitude_x = 150   # Амплитуда колебаний по оси X
    amplitude_y = 50    # Амплитуда колебаний по оси Y
    speed = TEXT_SPEED  # Скорость движения текста (изменение угла)
    color_index = 0     # Индекс текущего цвета

    # Создаем тень для текста (слегка смещенную вниз и вправо)
    shadow_text = canvas.create_text(962, 542, text=TEXT,
                                     font=(TEXT_FONT, TEXT_SIZE, TEXT_WEIGHT),
                                     fill=TEXT_SHADOW_COLOR)

    # Создаем основной текст с поздравлением
    valentine_text = canvas.create_text(960, 540, text=TEXT,
                                        font=(TEXT_FONT, TEXT_SIZE, TEXT_WEIGHT),
                                        fill=TEXT_COLORS[color_index])

    def animate_text():
        """
            Анимирует поздравительный текст:
            - Изменяет цвет по кругу из списка `text_colors`
            - Двигает текст по синусоиде, создавая эффект "плавного колебания"
            """
        nonlocal color_index, angle # Используем переменные из внешнего скоупа

        # Меняем цвет текста, переключая цвет по списку
        canvas.itemconfig(valentine_text, fill=TEXT_COLORS[color_index])

        # Вычисляем новые координаты на основе синусоидального движения
        # 960 и 540 начальные координаты (центр экрана)
        x = 960 + amplitude_x * math.sin(angle)
        y = 540 + amplitude_y * math.cos(angle)

        # Устанавливаем новые координаты текста и его тени
        canvas.coords(valentine_text, x, y)
        canvas.coords(shadow_text, x + 2, y + 2)    # Тень чуть смещена

        # Увеличиваем угол для создания плавного движения
        angle += speed
        # Повторяем анимацию каждые 100 миллисекунд
        root.after(100, animate_text)

    # Получаем фокус на окно сразу после его создания
    root.focus_set()  # Это должно помочь программе получать клавиши

    # 📌 Функция выхода из программы при нажатии "q"/"й"
    def on_key(event):
        if event.char.lower() in EXIT_BUTTON:
            # print("Выход из программы...")
            # root.destroy()
            root.quit()     # Завершаем главный цикл tkinter
            sys.exit(0)  # Корректное завершение программы
        # time.sleep(0.1)  # Небольшая задержка для снижения нагрузки на процессор

    # Привязываем обработчик к окну
    root.bind("<Key>", on_key)

    # Запускаем анимацию текста
    animate_text()
    # Запускаем анимацию сердец
    adjust_hearts()
    animate_hearts()
    # Запускаем главный цикл приложения
    root.mainloop()

# 🔥 Функция старта программы
def start_valentine():
    program_keyword = programs[selected_program]["window_keyword"]

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
            print(f"Сегодня {launch_date.strftime('%d %B')}. Запускаю сердечки!")
            create_hearts_and_text()
            break  # Останавливаем цикл после запуска анимации

        time.sleep(5)  # Проверяем каждые 5 секунд

# 📌 Проверяем автозапуск
check_autostart()

# 📌 Запускаем программу
start_valentine()

# 📌 Запускаем отслеживание программы в фоновом потоке
threading.Thread(target=start_valentine, daemon=True).start()

# close_selected_program()