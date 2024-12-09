import tkinter as tk
from tkinter import colorchooser, simpledialog

# Базовый класс для всех фигур
class Shape:
    def __init__(self, color='black', thickness=1):
        self.color = color  # Цвет фигуры
        self.thickness = thickness  # Толщина фигуры

# Класс для рисования точек
class Point(Shape):
    def __init__(self, x, y, color='black', thickness=1):
        super().__init__(color, thickness)  # Инициализация базового класса
        self.x = x  # Координата x точки
        self.y = y  # Координата y точки

    # Метод для рисования точки на холсте
    def draw(self, canvas):
        canvas.create_oval(
            self.x - self.thickness, self.y - self.thickness,
            self.x + self.thickness, self.y + self.thickness,
            fill=self.color, outline=self.color
        )

# Класс для рисования линий
class Line(Shape):
    def __init__(self, x1, y1, x2, y2, color='black', thickness=1):
        super().__init__(color, thickness)  # Инициализация базового класса
        self.x1 = x1  # Начальная координата x линии
        self.y1 = y1  # Начальная координата y линии
        self.x2 = x2  # Конечная координата x линии
        self.y2 = y2  # Конечная координата y линии

    # Метод для рисования линии на холсте
    def draw(self, canvas):
        canvas.create_line(
            self.x1, self.y1, self.x2, self.y2,
            fill=self.color, width=self.thickness
        )

# Основной класс приложения
class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Графический редактор")  # Заголовок окна

        # Создание холста для рисования
        self.canvas = tk.Canvas(root, bg='white', width=800, height=600)
        self.canvas.pack()

        self.color = 'black'  # Цвет по умолчанию
        self.thickness = 1  # Толщина по умолчанию
        self.mode = 'free'  # Режим рисования: 'free' или 'line'
        self.points = []  # Хранит точки для соединения линиями

        self.create_toolbar()  # Создание панели инструментов
        self.canvas.bind("<Button-1>", self.on_click)  # Обработка нажатия кнопки мыши
        self.canvas.bind("<B1-Motion>", self.on_drag)  # Обработка перемещения мыши с зажатой кнопкой

    # Метод для создания панели инструментов
    def create_toolbar(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка выбора цвета
        color_button = tk.Button(toolbar, text='Выбрать цвет', command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        # Кнопка выбора толщины
        thickness_button = tk.Button(toolbar, text='Выбрать толщину', command=self.choose_thickness)
        thickness_button.pack(side=tk.LEFT)

        # Кнопка для свободного рисования
        free_button = tk.Button(toolbar, text='Свободное рисование', command=self.set_free_mode)
        free_button.pack(side=tk.LEFT)

        # Кнопка для рисования линий
        line_button = tk.Button(toolbar, text='Рисовать линии', command=self.set_line_mode)
        line_button.pack(side=tk.LEFT)

        # Кнопка для очистки холста
        clear_button = tk.Button(toolbar, text='Очистить', command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

    # Метод для выбора цвета
    def choose_color(self):
        color = colorchooser.askcolor()[1]  # Открытие диалогового окна выбора цвета
        if color:
            self.color = color  # Установка выбранного цвета

    # Метод для выбора толщины линии
    def choose_thickness(self):
        thickness = simpledialog.askinteger("Толщина", "Введите толщину линии:", minvalue=1, maxvalue=10)
        if thickness:
            self.thickness = thickness  # Установка выбранной толщины

    # Метод для установки режима свободного рисования
    def set_free_mode(self):
        self.mode = 'free'  # Установка режима свободного рисования
        self.points = []  # Очистка списка точек

    # Метод для установки режима рисования линий
    def set_line_mode(self):
        self.mode = 'line'  # Установка режима рисования линий

    # Метод для очистки холста
    def clear_canvas(self):
        self.canvas.delete("all")  # Удаление всех объектов на холсте
        self.points = []  # Очистка списка точек

    # Метод для обработки нажатия кнопки мыши
    def on_click(self, event):
        if self.mode == 'line':
            self.points.append((event.x, event.y))  # Добавление точки в список
            if len(self.points) == 2:  # Если две точки выбраны
                line = Line(self.points[0][0], self.points[0][1], self.points[1][0], self.points[1][1],
                            color=self.color, thickness=self.thickness)
                line.draw(self.canvas)  # Рисование линии
                self.points = []  # Сброс списка точек после рисования

    # Метод для обработки перемещения мыши
    def on_drag(self, event):
        if self.mode == 'free':
            point = Point(event.x, event.y, color=self.color, thickness=self.thickness)
            point.draw(self.canvas)  # Рисование точки

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()