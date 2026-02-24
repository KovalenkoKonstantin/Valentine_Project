import tkinter as tk    # Библиотека для создания графического интерфейса
import random
import time
import threading    # Для запуска отслеживания Outlook в фоновом потоке
import os   # Для получения имени пользователям
from datetime import datetime, timedelta
import sys  # Для работы с путями
import winreg as reg  # Для работы с реестром Windows
import pygetwindow as gw    # Библиотека для получения списка открытых окон
import math


# Функция для добавления программы в автозагрузку
def add_to_autostart():
    script_path = os.path.abspath(sys.argv[0])  # Получаем полный путь к текущему скрипту
    script_name = os.path.basename(script_path)  # Имя скрипта (без пути)

    key = r"Software\Microsoft\Windows\CurrentVersion\Run"

    try:
        # Открываем ключ реестра для записи
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_WRITE) as reg_key:
            # Добавляем запись, если её нет
            reg.SetValueEx(reg_key, script_name, 0, reg.REG_SZ, script_path)
            print(f"Программа {script_name} добавлена в автозагрузку.")
    except Exception as e:
        print(f"Ошибка при добавлении в автозагрузку: {e}")


# Функция для проверки наличия программы в автозагрузке
def check_autostart():
    script_name = os.path.basename(sys.argv[0])  # Получаем имя скрипта
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"

    try:
        # Открываем ключ реестра для чтения
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_READ) as reg_key:
            try:
                # Проверяем, есть ли наш скрипт в реестре
                reg_value = reg.QueryValueEx(reg_key, script_name)
                print(f"Программа {script_name} найдена в автозагрузке: {reg_value}")
            except FileNotFoundError:
                print(f"Программа {script_name} не найдена в автозагрузке.")
                # Если программы нет в автозагрузке, добавляем её
                add_to_autostart()
    except Exception as e:
        print(f"Ошибка при проверке автозагрузки: {e}")

# Функция для создания анимации сердечек
def show_hearts():
    # Получаем имя пользователя системы
    user_name = os.getlogin()

    root = tk.Tk()
    root.title(f"С днём Валентина, {user_name}!")
    root.geometry("1920x1080")
    root.configure(bg="white")  # Цвет фона окна
    # root.config(bg='black')     # Черный фон для контраста
    root.attributes("-topmost", True)   # Окно всегда сверху
    root.resizable(False, False)    # Отключаем изменение размера окна

    canvas = tk.Canvas(root, width=1920, height=1080, bg="white", highlightthickness=0)
    # canvas = tk.Canvas(root, width=1920, height=1080, bg="black", highlightthickness=0)
    canvas.pack()

    # Список для хранения всех сердечек
    hearts = []

    # 💖 Функция для создания нового сердечка
    def create_heart():
        x = random.randint(50, 1870)  # Рандомное появление по X
        y = random.randint(50, 1030)  # Рандомное появление по Y
        size = random.randint(30, 70)   # Размер сердечка
        # color = random.choice(["red", "pink", "purple"])
        color = random.choice(["#FF1493", "#FF69B4", "#DB7093", "#FF00FF", "#FF007F"])  # Яркие цвета

        shadow_color = "#FFC0CB"  # Цвет тени
        # Создаем тень для сердечка
        shadow = canvas.create_text(x + 2, y + 2, text="❤️", font=("Arial", size), fill=shadow_color)

        # Создаем сердечко в виде эмодзи "❤️"
        heart = canvas.create_text(x, y, text="❤️", font=("Arial", size), fill=color)
        # Добавляем сердечко и тень в список с случайными скоростями по X и Y
        # hearts.append((heart, x, y, random.uniform(-3, 3), random.uniform(-1, -3)))  # Добавили скорость по X и Y
        hearts.append((heart, shadow, x, y, random.uniform(-3, 3), random.uniform(-1, -3)))

    # 🎬 Функция для анимации сердечек
    def animate_hearts():
        # for i, (heart, x, y, dx, dy) in enumerate(hearts):
        for i, (heart, shadow, x, y, dx, dy) in enumerate(hearts):
            y += dy  # Двигаем вверх (dy отрицательный)
            x += dx  # Добавляем немного движения в стороны

            # Обновляем позицию сердечка на холсте
            canvas.coords(heart, x, y)
            canvas.coords(shadow, x + 2, y + 2)

            # Если сердечко ушло за границы - удаляем
            if y < -50 or x < -50 or x > 1970:
                canvas.delete(heart)
                canvas.delete(shadow)
                hearts.pop(i)

            # **Опускаем сердечки на задний план**
            for heart, shadow, *_ in hearts:
                canvas.tag_lower(heart)
                canvas.tag_lower(shadow)

        # Повторяем анимацию каждые 50 мс
        root.after(50, animate_hearts)

    MAX_HEARTS = 100  # Ограничение количества сердечек

    # ⏳ Функция для постоянного создания новых сердечек
    def create_hearts():
        # Удаляем старые сердечки, если их стало слишком много
        while len(hearts) > MAX_HEARTS:
            heart, shadow, *_ = hearts.pop(0)  # Удаляем самое старое сердечко
            canvas.delete(heart)
            canvas.delete(shadow)

        # Добавляем новые сердечки
        for _ in range(7):
            create_heart()

        root.after(200, create_hearts)  # Повторяем каждые 200 мс

    # 🌟 Функция создания звезд на фоне
    # def create_stars():
    #     for _ in range(100):
    #         x = random.randint(0, 1920)
    #         y = random.randint(0, 1080)
    #         size = random.randint(1, 3)
    #         star = canvas.create_oval(x, y, x + size, y + size, fill="white", outline="")
    #
    #         # Отправляем звезды на задний план, чтобы они не перекрывались сердечками
    #         canvas.tag_lower(star)

        # Повторяем анимацию каждые 50 мс
        # root.after(50, create_stars)

    # Перемещение текста без выхода за границы экрана
    angle = 0  # Угол для вычисления колебаний
    amplitude_x = 100  # Амплитуда движения по X
    amplitude_y = 50  # Амплитуда движения по Y
    speed = 0.05  # Скорость изменения угла

    # Цвета для переливания текста
    colors = ["#FF1493", "#FF69B4", "#DB7093", "#FF00FF", "#FF007F", "#FF4500", "#FFD700"]
    # Цвета для переливания текста (контрастные с сердечками)
    text_colors = ["#FFD700", "#FFFFFF", "#8B0000", "#191970"]
    color_index = 0

    # Создаем надпись и её тень
    shadow_text = canvas.create_text(
        962, 542,  # Чуть сдвигаем для тени
        text=f"С днём Валентина, {user_name}!",
        font=("Arial", 50, "bold"),
        fill="black"
    )

    valentine_text = canvas.create_text(
        960, 540,  # Начальные координаты (центр экрана)
        text=f"С днём Валентина, {user_name}!",
        font=("Arial", 50, "bold"),
        fill=text_colors[color_index]
    )

    # 🎨 Функция для анимации текста
    def animate_text():
        nonlocal color_index, angle

        # Переливание цветов
        canvas.itemconfig(valentine_text, fill=text_colors[color_index])
        color_index = (color_index + 1) % len(text_colors)

        # Движение текста по синусоиде вокруг центра
        x = 960 + amplitude_x * math.sin(angle)
        y = 540 + amplitude_y * math.cos(angle)

        canvas.coords(valentine_text, x, y)
        canvas.coords(shadow_text, x + 2, y + 2)

        # Увеличиваем угол для следующего кадра
        angle += speed

        # Повторяем анимацию каждые 50 мс
        root.after(100, animate_text)

    animate_text()  # Запускаем анимацию текста
    create_hearts()  # Запускаем создание сердечек
    animate_hearts()  # Запускаем анимацию сердечек
    # create_stars()  # Создаем звезды на фоне
    root.mainloop()  # Запускаем главный цикл окна


# Функция для закрытия Outlook
def close_outlook():
    # Получаем список всех окон
    all_windows = gw.getAllTitles()

    # Ищем окна Outlook
    outlook_windows = [win for win in all_windows if "Outlook" in win]

    # Если окно Outlook найдено, закрываем его
    if outlook_windows:
        print("Outlook найден. Закрываю...")
        # Закрытие всех окон Outlook
        for win in outlook_windows:
            win_obj = gw.getWindowsWithTitle(win)[0]
            win_obj.close()
            print(f"Закрыто окно: {win}")
    else:
        print("Outlook не найден, ничего не закрываю.")


# Переменная для даты запуска программы
launch_date = datetime(datetime.now().year, 2, 14)


# 📧 Функция для отслеживания Outlook
def check_outlook():
    while True:
        # Выводим дату, когда должна быть запущена программа
        # print(f"Программа будет запущена: {launch_date.strftime('%d-%m-%Y')}")

        # Получаем текущее время
        current_time = datetime.now()

        # Рассчитываем дату за день до launch_date
        one_day_before = launch_date - timedelta(days=1)

        # Проверяем, совпадает ли текущая дата и время с 23:00 за день до
        if current_time.date() == one_day_before.date() and current_time.hour == 23 and current_time.minute == 0:
            print(f"Сегодня {one_day_before.strftime('%d %B')}, 23:00. Проверяю Outlook...")

            # Если Outlook открыт, закрываем его
            close_outlook()

        # Проверяем дату
        if current_time.date() == launch_date.date():
            print('Сегодня подходящая дата для запуска программы')

            # Получаем список всех окон
            all_windows = gw.getAllTitles()
            # Выводим в консоль список всех окон
            print("Все открытые окна:", all_windows)

            # Ищем окно Outlook в списке (проверяем, есть ли "Outlook" в названии)
            outlook_windows = [win for win in all_windows if "Outlook" in win]
            print("Найденные окна Outlook:", outlook_windows)

            # Если Outlook найден
            if outlook_windows:
                print('Outlook запущен')
                print('Запускаю сердечки')
                show_hearts()  # Запускаем анимацию сердечек
                break  # Останавливаем проверку после запуска анимации
            else:
                print('Outlook не найден, жду...')

        time.sleep(5)  # Проверяем каждые 60 секунд

# Запуск функции проверки автозагрузки
# check_autostart()

# Запуск функции проверки Outlook
close_outlook()


# 🚀 Запуск проверки Outlook в фоновом потоке
# threading.Thread(target=check_outlook, daemon=True).start()
