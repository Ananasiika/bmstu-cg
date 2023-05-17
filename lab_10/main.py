import tkinter as tk
from math import pi, cos, sin
from tkinter import colorchooser
from tkinter import ttk
from numpy import arange
from math import sin, cos, pi
from functions import funcs

MAIN_COLOUR = "#C0C0C0"
ADD_COLOUR = "#202020"
BUTTON_COLOUR = "#FFFFFF"
DEFAULT_COLOUR = "#000000"

WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 810

# Frame sizes (relative).
BORDERS_PART = 0.03
BORDERS_WIDTH = int(WINDOW_WIDTH * BORDERS_PART)
BORDERS_HEIGHT = int(WINDOW_HEIGHT * BORDERS_PART)

# Number of rows (some kind of grid) for data.
ROWS = 20

DATA_PART_WIDTH = 0.28 - 2 * BORDERS_PART
DATA_PART_HEIGHT = 1 - 2 * BORDERS_PART
DATA_WIDTH = int(DATA_PART_WIDTH * WINDOW_WIDTH)
DATA_HEIGHT = int(DATA_PART_HEIGHT * WINDOW_HEIGHT)
SLOT_HEIGHT = DATA_HEIGHT // ROWS

FIELD_PART_WIDTH = (1 - DATA_PART_WIDTH) - 4 * BORDERS_PART
FIELD_PART_HEIGHT = 1 - 2 * BORDERS_PART
FIELD_WIDTH = int(FIELD_PART_WIDTH * WINDOW_WIDTH)
FIELD_HEIGHT = int(FIELD_PART_HEIGHT * WINDOW_HEIGHT)
CANVAS_CENTER = (FIELD_WIDTH // 2, FIELD_HEIGHT // 2)

FIELD_BORDER_PART = 0.03

FUNCS = ["sin(x) * cos(z)", "sin(cos(x)) * sin(z)", "cos(x) * z / 3"]

color = DEFAULT_COLOUR

sf = 48
x_from = -10
x_to = 10
x_step = 0.1

z_from = -10
z_to = 10
z_step = 0.1

trans_matrix = [[int(i == j) for i in range(4)] for j in range(4)]


def clear_all():
    clear_canvas()


def clear_canvas():
    canvas.delete('all')


def change_color():
    global color, color_btn
    color = colorchooser.askcolor(title="select color")[1]
    color_btn.configure(background=color)


def draw_section(xb, yb, xe, ye, color):
    canvas.create_line(xb, yb, xe, ye, fill=color)


def rotate_trans_matrix(rotate_matrix):
    global trans_matrix
    res_matrix = [[0 for i in range(4)] for j in range(4)]

    for i in range(4):
        for j in range(4):
            for k in range(4):
                res_matrix[i][j] += trans_matrix[i][k] * rotate_matrix[k][j]

    trans_matrix = res_matrix


def trans_point(point):
    # point = (x, y, z)
    point.append(1) # (x, y, z, 1)
    res_point = [0, 0, 0, 0]
    for i in range(4):
        for j in range(4):
            res_point[i] += point[j] * trans_matrix[j][i]

    for i in range(3):
        res_point[i] *= sf # x, y, z ==> SF * x, SF * y, SF * z

    res_point[0] += FIELD_WIDTH / 2
    res_point[1] += FIELD_HEIGHT / 2

    return res_point[:3]


def rotate_x():
    value = float(x_entry.get()) / 180 * pi
    rotate_matrix = [ [ 1, 0, 0, 0 ],
                       [ 0, cos(value), sin(value), 0 ],
                       [ 0, -sin(value), cos(value), 0 ],
                       [ 0, 0, 0, 1 ] ]
    rotate_trans_matrix(rotate_matrix)
    solve()


def rotate_y():
    value = float(y_entry.get()) / 180 * pi
    rotate_matrix = [ [ cos(value), 0, -sin(value), 0 ],
                       [ 0, 1, 0, 0 ],
                       [ sin(value), 0, cos(value), 0 ],
                       [ 0, 0, 0, 1 ] ]
    rotate_trans_matrix(rotate_matrix)
    solve()


def rotate_z():
    value = float(z_entry.get()) / 180 * pi
    rotate_matrix = [ [ cos(value), sin(value), 0, 0 ],
                       [ -sin(value), cos(value), 0, 0 ],
                       [ 0, 0, 1, 0 ],
                       [ 0, 0, 0, 1 ] ]
    rotate_trans_matrix(rotate_matrix)
    solve()


def set_sf():
    global sf
    sf = float(scale_entry.get())
    solve()

def set_meta():
    global x_from, x_step, x_to, z_from, z_step, z_to
    x_from = float(xfrom_entry.get())
    x_to = float(xto_entry.get())
    x_step = float(xstep_entry.get())
    z_from = float(zfrom_entry.get())
    z_to = float(zto_entry.get())
    z_step = float(zstep_entry.get())
    solve()


def draw_pixel(x, y):
    canvas.create_line(x, y, x + 1, y + 1, fill=color)


def is_visible(point):
    return 0 <= point[0] < FIELD_WIDTH and 0 <= point[1] < FIELD_HEIGHT


def draw_point(x, y, hh, lh):
    if not is_visible([x, y]):
        return False

    if y > hh[x]:
        hh[x] = y
        draw_pixel(x, y)

    elif y < lh[x]:
        lh[x] = y
        draw_pixel(x, y)

    return True


def draw_horizon_part(p1, p2, hh, lh):
    if p1[0] > p2[0]: # хочу, чтобы x2 > x1
        p1, p2 = p2, p1

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    l = dx if dx > dy else dy
    dx /= l
    dy /= l

    x, y = p1[0], p1[1]

    for _ in range(int(l) + 1):
        if not draw_point(int(round(x)), y, hh, lh):
            return
        x += dx
        y += dy


def draw_horizon(func, hh, lh, fr, to, step, z):
    f = lambda x: func(x, z) # f = f(x, z=const)
    prev = None
    for x in arange(fr, to + step, step):
        # x, z, f(x, z=const)
        current = trans_point([x, f(x), z]) # transformed: Повернуть, масштабировать и сдвинуть в центр экрана
        if prev: # Если это не первая точка (то есть если есть предыдущая)
            draw_horizon_part(prev, current, hh, lh)
        prev = current


def solve():
    clear_canvas()
    f = funcs[func_var.get()]
    high_horizon = [0 for i in range(FIELD_WIDTH)]
    low_horizon = [FIELD_HEIGHT for i in range(FIELD_WIDTH)]

    for z in arange(z_from, z_to + z_step, z_step):
        draw_horizon(f, high_horizon, low_horizon, x_from, x_to, x_step, z)

    for z in arange(z_from, z_to, z_step):
        p1 = trans_point([x_from, f(x_from, z), z])
        p2 = trans_point([x_from, f(x_from, z + z_step), z + z_step])
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color)
        p1 = trans_point([x_to, f(x_to, z), z])
        p2 = trans_point([x_to, f(x_to, z + z_step), z + z_step])
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color)
        



root = tk.Tk()
root.title("Лабораторная работа №10")
root["bg"] = MAIN_COLOUR
root.minsize(1100, 800)
root.geometry('1300x800+250+50')

style = ttk.Style(root)
style.configure('default.TButton', font='"Segoe UI Variable" 12')
style.configure('black.TButton', background='#000000')
style.configure('white.TButton', background='#ffffff')
style.configure('red.TButton', background='#ff0000')
style.configure('green.TButton', background='#00ff00')
style.configure('blue.TButton', background='#0000ff')

data_frame = tk.Frame(root)
data_frame["bg"] = MAIN_COLOUR

data_frame.place(x=int(BORDERS_WIDTH), y=int(BORDERS_HEIGHT),
                 width=DATA_WIDTH,
                 height=DATA_HEIGHT
                 )

func_var = tk.IntVar()
func_var.set(0)
func_radios = list()
for i in range(len(FUNCS)):
    func_radios.append(tk.Radiobutton(data_frame, text=FUNCS[i], bg='#ffffff',
                                      fg="#000000", variable=func_var, value=i))

color_label = tk.Label(data_frame, text="Цвет", font='"Segoe UI Variable" 12', bg=MAIN_COLOUR,
                       fg=ADD_COLOUR, relief=tk.GROOVE)
rotate_label = tk.Label(data_frame, text="Вращение", font='"Segoe UI Variable" 12',
                        bg=MAIN_COLOUR, fg=ADD_COLOUR, relief=tk.GROOVE)
meta_label = tk.Label(data_frame, text="Пределы и шаг", font='"Segoe UI Variable" 12',
                      bg=MAIN_COLOUR, fg=ADD_COLOUR, relief=tk.GROOVE)
x_label = tk.Label(data_frame, text="x", font='"Segoe UI Variable" 12', bg=MAIN_COLOUR,
                   fg=ADD_COLOUR, relief=tk.GROOVE)
y_label = tk.Label(data_frame, text="y", font='"Segoe UI Variable" 12', bg=MAIN_COLOUR,
                   fg=ADD_COLOUR, relief=tk.GROOVE)
z_label = tk.Label(data_frame, text="z", font='"Segoe UI Variable" 12', bg=MAIN_COLOUR,
                   fg=ADD_COLOUR, relief=tk.GROOVE)
xlabel = tk.Label(data_frame, text="x", font='"Segoe UI Variable" 12', bg=MAIN_COLOUR,
                   fg=ADD_COLOUR, relief=tk.GROOVE)
zlabel = tk.Label(data_frame, text="z", font='"Segoe UI Variable" 12', bg=MAIN_COLOUR,
                   fg=ADD_COLOUR, relief=tk.GROOVE)
from_label = tk.Label(data_frame, text="От", font='"Segoe UI Variable" 12', bg=MAIN_COLOUR,
                      fg=ADD_COLOUR, relief=tk.GROOVE)
to_label = tk.Label(data_frame, text="До", font='"Segoe UI Variable" 12', bg=MAIN_COLOUR,
                    fg=ADD_COLOUR, relief=tk.GROOVE)
step_label = tk.Label(data_frame, text="Шаг", font='"Segoe UI Variable" 12', bg=MAIN_COLOUR,
                      fg=ADD_COLOUR, relief=tk.GROOVE)
func_label = tk.Label(data_frame, text="Функция", font='"Segoe UI Variable" 12', bg=MAIN_COLOUR,
                      fg=ADD_COLOUR, relief=tk.GROOVE)
scale_label = tk.Label(data_frame, text="Коэффициент\nмасштабирования",
                       font=("Consolas", 11), bg=MAIN_COLOUR, fg=ADD_COLOUR, relief=tk.GROOVE)


x_entry = tk.Entry(data_frame, bg='#ffffff', font='"Segoe UI Variable" 12',
                   fg="#000000", justify="center")
y_entry = tk.Entry(data_frame, bg='#ffffff', font='"Segoe UI Variable" 12',
                   fg="#000000", justify="center")
z_entry = tk.Entry(data_frame, bg='#ffffff', font='"Segoe UI Variable" 12',
                   fg="#000000", justify="center")

x_entry.insert(0, "20")
y_entry.insert(0, "20")
z_entry.insert(0, "20")

xfrom_entry = tk.Entry(data_frame, bg='#ffffff', font='"Segoe UI Variable" 12',
                      fg="#000000", justify="center")
xto_entry = tk.Entry(data_frame, bg='#ffffff', font='"Segoe UI Variable" 12',
                    fg="#000000", justify="center")
xstep_entry = tk.Entry(data_frame, bg='#ffffff', font='"Segoe UI Variable" 12',
                      fg="#000000", justify="center")

xfrom_entry.insert(0, str(x_from))
xto_entry.insert(0, str(x_to))
xstep_entry.insert(0, str(x_step))

zfrom_entry = tk.Entry(data_frame, bg='#ffffff', font='"Segoe UI Variable" 12',
                      fg="#000000", justify="center")
zto_entry = tk.Entry(data_frame, bg='#ffffff', font='"Segoe UI Variable" 12',
                    fg="#000000", justify="center")
zstep_entry = tk.Entry(data_frame, bg='#ffffff', font='"Segoe UI Variable" 12',
                      fg="#000000", justify="center")

zfrom_entry.insert(0, str(z_from))
zto_entry.insert(0, str(z_to))
zstep_entry.insert(0, str(z_step))

scale_entry = tk.Entry(data_frame, bg='#ffffff', font='"Segoe UI Variable" 12',
                      fg="#000000", justify="center")
scale_entry.insert(0, str(sf))


x_btn = tk.Button(data_frame, text="Вращать", font='"Segoe UI Variable" 12',
                  bg=MAIN_COLOUR, fg=ADD_COLOUR, command=rotate_x,
                  activebackground=ADD_COLOUR, activeforeground=MAIN_COLOUR)
y_btn = tk.Button(data_frame, text="Вращать", font='"Segoe UI Variable" 12',
                  bg=MAIN_COLOUR, fg=ADD_COLOUR, command=rotate_y,
                  activebackground=ADD_COLOUR, activeforeground=MAIN_COLOUR)
z_btn = tk.Button(data_frame, text="Вращать", font='"Segoe UI Variable" 12',
                  bg=MAIN_COLOUR, fg=ADD_COLOUR, command=rotate_z,
                  activebackground=ADD_COLOUR, activeforeground=MAIN_COLOUR)
confirm_btn = tk.Button(data_frame, text="Применить", font='"Segoe UI Variable" 12',
                        bg=MAIN_COLOUR, fg=ADD_COLOUR, command=set_meta,
                        activebackground=ADD_COLOUR, activeforeground=MAIN_COLOUR)
scale_button = tk.Button(data_frame, text="Изменить", font='"Segoe UI Variable" 12',
                         bg=MAIN_COLOUR, fg=ADD_COLOUR, command=set_sf,
                         activebackground=ADD_COLOUR, activeforeground=MAIN_COLOUR)

res_btn = tk.Button(data_frame, text="Нарисовать", font='"Segoe UI Variable" 12',
                    bg=MAIN_COLOUR, fg=ADD_COLOUR, command=solve,
                    activebackground=ADD_COLOUR, activeforeground=MAIN_COLOUR)
color_btn = tk.Button(data_frame, text="", font='"Segoe UI Variable" 12', bg=color,
                      command=change_color, relief=tk.GROOVE)
clear_btn = tk.Button(data_frame, text="Очистить поле", font='"Segoe UI Variable" 12',
                      bg=MAIN_COLOUR, fg=ADD_COLOUR, command=clear_all,
                      activebackground=ADD_COLOUR, activeforeground=MAIN_COLOUR)

offset = 0

color_label.place(x=0, y=DATA_HEIGHT * offset // ROWS, width=DATA_WIDTH,
                  height=DATA_HEIGHT // ROWS)
offset += 1

color_btn.place(x=0, y=SLOT_HEIGHT * offset,
                width=DATA_WIDTH, height=SLOT_HEIGHT)
offset += 2

func_label.place(x=0, y=SLOT_HEIGHT * offset, width=DATA_WIDTH,
                 height=SLOT_HEIGHT)

for i in range(len(func_radios)):
    offset += 1
    func_radios[i].place(x=0, y=SLOT_HEIGHT * offset, width=DATA_WIDTH,
                     height=SLOT_HEIGHT)
offset += 2

meta_label.place(x=0, y=SLOT_HEIGHT * offset,
                 width=DATA_WIDTH, height=SLOT_HEIGHT)

from_label.place(x=DATA_WIDTH // 4, y=SLOT_HEIGHT * offset,
                 width=DATA_WIDTH // 4, height=SLOT_HEIGHT)
to_label.place(x=2 * DATA_WIDTH // 4, y=SLOT_HEIGHT * offset, width=DATA_WIDTH // 4,
               height=SLOT_HEIGHT)
step_label.place(x=3 * DATA_WIDTH // 4, y=SLOT_HEIGHT * offset, width=DATA_WIDTH // 4,
                 height=SLOT_HEIGHT)
offset += 1

xlabel.place(x=0, y=SLOT_HEIGHT * offset, width=DATA_WIDTH // 4, height=SLOT_HEIGHT)
xfrom_entry.place(x=DATA_WIDTH // 4, y=SLOT_HEIGHT * offset,
                 width=DATA_WIDTH // 4, height=SLOT_HEIGHT)
xto_entry.place(x=2 * DATA_WIDTH // 4, y=SLOT_HEIGHT * offset, width=DATA_WIDTH // 4,
               height=SLOT_HEIGHT)
xstep_entry.place(x=3 * DATA_WIDTH // 4, y=SLOT_HEIGHT * offset, width=DATA_WIDTH // 4,
                 height=SLOT_HEIGHT)
offset += 1

zlabel.place(x=0, y=SLOT_HEIGHT * offset, width=DATA_WIDTH // 4, height=SLOT_HEIGHT)
zfrom_entry.place(x=DATA_WIDTH // 4, y=SLOT_HEIGHT * offset,
                 width=DATA_WIDTH // 4, height=SLOT_HEIGHT)
zto_entry.place(x=2 * DATA_WIDTH // 4, y=SLOT_HEIGHT * offset, width=DATA_WIDTH // 4,
               height=SLOT_HEIGHT)
zstep_entry.place(x=3 * DATA_WIDTH // 4, y=SLOT_HEIGHT * offset, width=DATA_WIDTH // 4,
                 height=SLOT_HEIGHT)
offset += 1

confirm_btn.place(x=0, y=SLOT_HEIGHT * offset,
                  width=DATA_WIDTH, height=SLOT_HEIGHT)
offset += 2

scale_label.place(x=0, y=SLOT_HEIGHT * offset, width=DATA_WIDTH // 3 + 35, height=SLOT_HEIGHT)
scale_entry.place(x=DATA_WIDTH // 3 + 35, y=SLOT_HEIGHT * offset,
                 width=DATA_WIDTH // 3 - 35, height=SLOT_HEIGHT)
scale_button.place(x=2 * DATA_WIDTH // 3, y=SLOT_HEIGHT * offset,
                 width=DATA_WIDTH // 3, height=SLOT_HEIGHT)

rotate_label.place(x=0, y=SLOT_HEIGHT * offset,
                   width=DATA_WIDTH, height=SLOT_HEIGHT)
offset += 1

x_label.place(x=0, y=SLOT_HEIGHT * offset,
              width=DATA_WIDTH // 3 + 35, height=SLOT_HEIGHT)
x_entry.place(x=DATA_WIDTH // 3 + 35, y=SLOT_HEIGHT * offset, width=DATA_WIDTH // 3 - 35,
              height=SLOT_HEIGHT)
x_btn.place(x=2 * DATA_WIDTH // 3, y=SLOT_HEIGHT * offset, width=DATA_WIDTH // 3,
            height=SLOT_HEIGHT)
offset += 1

y_label.place(x=0, y=SLOT_HEIGHT * offset,
              width=DATA_WIDTH // 3 + 35, height=SLOT_HEIGHT)
y_entry.place(x=DATA_WIDTH // 3 + 35, y=SLOT_HEIGHT * offset, width=DATA_WIDTH // 3 - 35,
              height=SLOT_HEIGHT)
y_btn.place(x=2 * DATA_WIDTH // 3, y=SLOT_HEIGHT * offset, width=DATA_WIDTH // 3,
            height=SLOT_HEIGHT)
offset += 1

z_label.place(x=0, y=SLOT_HEIGHT * offset,
              width=DATA_WIDTH // 3 + 35, height=SLOT_HEIGHT)
z_entry.place(x=DATA_WIDTH // 3 + 35, y=SLOT_HEIGHT * offset, width=DATA_WIDTH // 3 - 35,
              height=SLOT_HEIGHT)
z_btn.place(x=2 * DATA_WIDTH // 3, y=SLOT_HEIGHT * offset, width=DATA_WIDTH // 3,
            height=SLOT_HEIGHT)

offset = ROWS - 2

res_btn.place(x=0, y=SLOT_HEIGHT * offset,
              width=DATA_WIDTH, height=SLOT_HEIGHT)
offset += 1

clear_btn.place(x=0, y=SLOT_HEIGHT * offset,
                width=DATA_WIDTH, height=SLOT_HEIGHT)

canvas_frame = tk.Frame(root, bg="white")
canvas = tk.Canvas(canvas_frame, bg="white")
root.bind("<Return>", lambda x: solve())

canvas_frame.place(x=3 * BORDERS_WIDTH + DATA_WIDTH, y=BORDERS_HEIGHT,
                   width=FIELD_WIDTH, height=FIELD_HEIGHT)

canvas.place(x=0, y=0, width=FIELD_WIDTH, height=FIELD_HEIGHT)

root.mainloop()