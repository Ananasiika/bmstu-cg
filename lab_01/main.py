from tkinter import *
import tkinter.messagebox as box
from tkinter import messagebox
from math import *

root = Tk()
root.geometry('900x900')
var = IntVar()
story = []
c = Canvas(root, width=900, height=900, bg='white')
text1 = Text(c, width=36, height=10, state=DISABLED)
text2 = Text(c, width=36, height=10, state=DISABLED)
text = Text(c, width=25, height=10, state=DISABLED)
num_1, num_2, edit, wx, wy = 1, 1, 0, 1, 1

ent1 = Entry(c, width=8)
ent2 = Entry(c, width=8)
ent1.place(x=wx * 32, y=wy * 177)
ent2.place(x=wx * 132, y=wy * 177)
ent3 = Entry(c, width=8)
ent4 = Entry(c, width=8)
ent3.place(x=wx * 460, y=wy * 177)
ent4.place(x=wx * 560, y=wy * 177)
ent5 = Entry(c, width=4)
ent5.place(x=wx * 176, y=wy * 215)
ent6 = Entry(c, width=4)
ent6.place(x=wx * 600, y=wy * 215)
TASK = 'Вариант 18:\nДаны два множества точек на плоскости. Выбрать три различные точки\
    первого множества так, чтобы круг, ограниченный окружностью, проходящей через\
    эти точки, содержал минимум 80% точек второго множества и имел минимальную площадь'
AUTHOR = '\n\nПронина Лариса ИУ7-44Б'
sz = 1

def enable():
    text1.configure(state=NORMAL)
    text2.configure(state=NORMAL)

def disable():
    text1.configure(state=DISABLED)
    text2.configure(state=DISABLED)

def add_dot(num): # добавление точки через ввод координат
    global num_1, num_2
    if num == 1:
        d1 = ent1.get()
        d2 = ent2.get()
        ent1.delete(0, END)
        ent2.delete(0, END)
    else:
        d1 = ent3.get()
        d2 = ent4.get()
        ent3.delete(0, END)
        ent4.delete(0, END)
    try:
        d1 = float(d1)
        d2 = float(d2)
        if abs(d1) >= 10000 or abs(d2) >= 10000:
            box.showinfo('Error', 'Некорректные координаты!\nКоордината должна быть числом < 10000, \nразделителем между целой и дробной частями является точка.')
            return
        enable()
        if num == 1: # в первое множество
            text1.insert(END, f'{num_1}: ({d1:g}; {d2:g})\n')
            story.append('')
            sett1 = text1.get(1.0, END).split('\n')[:-1]
            if not sett1[-1]:
                sett1 = sett1[:-1]
            end = len(sett1)
            story[-1] += f'text1.delete({end}.0, END)'
            story[-1] += '; text1.insert(END, "\\n")' if end > 1 else ''
            num_1 += 1
        else: # во второе множество
            text2.insert(END, f'{num_2}: ({d1:g}; {d2:g})\n')
            story.append('')
            sett2 = text2.get(1.0, END).split('\n')[:-1]
            if not sett2[-1]:
                sett2 = sett2[:-1]
            end = len(sett2)
            story[-1] += f'text2.delete({end}.0, END)'
            story[-1] += '; text2.insert(END, "\\n")' if end > 1 else ''
            num_2 += 1
        disable()
        x, y = coord_true(d1, d2)
        print_dot(x, y, num)
        scale()
    except:
        box.showinfo('Error', 'Некорректные координаты!\nКоордината должна быть числом < 10000, \nразделителем между целой и дробной частями является точка.')


def back(): # Отмена действия
    enable()
    if not len(story):
        return

    command = story[-1]
    commands = []
    if ';' in command:
        commands = command.split(';', 1)
    else:
        commands.append(command)

    for com in commands:
        if not com:
            continue
        eval(com)

    del story[-1]

    global num_1, num_2 # пересчет количества точек
    data = text1.get(1.0, END).replace(': ', '\n').split('\n')[:-1]
    if not data[-1]:
        data = data[:-1]
    data = data[1::2]
    num_1 = len(data) + 1
    data = text2.get(1.0, END).replace(': ', '\n').split('\n')[:-1]
    if not data[-1]:
        data = data[:-1]
    data = data[1::2]
    num_2 = len(data) + 1

    update_dots()
    disable()
    scale()


def is_cursor_touch_dot(dot, event): # Проверка кликнули ли по существующей точке
    coo = c.coords(dot)
    x, y = event.x, event.y
    if coo[0] <= x <= coo[0] + 4 and coo[1] <= y <= coo[1] + 4:
        return 1
    else:
        return 0


def click(event): # Добавление точки через клик по полю
    global num_1, num_2
    x, y = (event.x - 365 * wx) * sz / wx, (550 * wy - event.y) * sz  / wy
    click_dot = 0
    dotts = c.find_withtag('dot')
    for dot in dotts:
        if is_cursor_touch_dot(dot, event):
            click_dot = 1

    if click_dot == 0:
        enable()
        if var.get() + 1 == 1:  # в первое множество
            text1.insert(END, f'{num_1}: ({x:g}; {y:g})\n')
            story.append('')
            sett1 = text1.get(1.0, END).split('\n')[:-1]
            if not sett1[-1]:
                sett1 = sett1[:-1]
            end = len(sett1)
            story[-1] += f'text1.delete({end}.0, END)'
            story[-1] += '; text1.insert(END, "\\n")' if end > 1 else ''
            num_1 += 1
        else:  # во второе множество
            text2.insert(END, f'{num_2}: ({x:g}; {y:g})\n')
            story.append('')
            sett2 = text2.get(1.0, END).split('\n')[:-1]
            if not sett2[-1]:
                sett2 = sett2[:-1]
            end = len(sett2)
            story[-1] += f'text2.delete({end}.0, END)'
            story[-1] += '; text2.insert(END, "\\n")' if end > 1 else ''
            num_2 += 1
        disable()
        print_dot(event.x, event.y, var.get() + 1)
    else: # кликнули по существующей точке
        dotts = c.find_withtag('dot')
        for dot in dotts:
            if is_cursor_touch_dot(dot, event):
                c.delete(dot)

        data = text1.get(1.0, END).replace(': ', '\n').split('\n')[:-1]
        if not data[-1]:
            data = data[:-1]
        data = data[1::2]
        
        i = 0
        for dot in data:
            a, b = map(float, dot.strip('\n').strip(')').strip('(').split(';'))
            if abs(a - x) < 4 and abs(b - y) < 4:
                break
            i += 1
        if i < len(data):
            enable()
            text1.delete(0.0, END)
            for j in range(i):
                text1.insert(END, f'{j+1}: ' + data[j] + '\n')
            for j in range(i + 1, len(data)):
                text1.insert(END, f'{j}: ' + data[j] + '\n')
            disable()
            story.append('')
            story[-1] += '; text1.insert(END, "{}: ""{}" + "\\n")'.format(num_1 - 1, data[i])
            num_1 -= 1

        data = text2.get(1.0, END).replace(': ', '\n').split('\n')[:-1]
        if not data[-1]:
            data = data[:-1]
        data = data[1::2]
        
        i = 0
        for dot in data:
            a, b = map(float, dot.strip('\n').strip(')').strip('(').split(';'))
            if abs(a - x) < 4 and abs(b - y) < 4:
                break
            i += 1
        if i < len(data):
            enable()
            text2.delete(0.0, END)
            for j in range(i):
                text2.insert(END, f'{j+1}: ' + data[j] + '\n')
            for j in range(i + 1, len(data)):
                text2.insert(END, f'{j}: ' + data[j] + '\n')
            disable()
            story.append('')
            story[-1] += '; text2.insert(END, "{}: ""{}" + "\\n")'.format(num_2 - 1, data[i])
            num_2 -= 1
    scale()

def update_dots(): # Отрисовка всех точек заново
    clean_points()
    data = text1.get(1.0, END).replace(': ', '\n').split('\n')[:-1]
    if not data[-1]:
        data = data[:-1]
    data = data[1::2]

    for dot in data:
        x, y = map(float, dot.strip('\n').strip(')').strip('(').split(';'))
        x, y = coord_true(x, y)
        print_dot(x, y, 1)

    data = text2.get(1.0, END).replace(': ', '\n').split('\n')[:-1]
    if not data[-1]:
        data = data[:-1]
    data = data[1::2]

    for dot in data:
        x, y = map(float, dot.strip('\n').strip(')').strip('(').split(';'))
        x, y = coord_true(x, y)
        print_dot(x, y, 2)


def edit_dot(n): # редактирование точки в списке
    global num_1, num_2, edit

    if edit == 1:
        data = text1.get(1.0, END).replace(': ', '\n').split('\n')[:-1]
        if not data[-1]:
            data = data[:-1]
        data = data[1::2]

        enable()
        text1.delete(0.0, END)
        for j in range(int(ent5.get()) - 1):
            text1.insert(END, f'{j+1}: ' + data[j] + '\n')
        
        d1 = ent1.get()
        d2 = ent2.get()
        ent1.delete(0, END)
        ent2.delete(0, END)
        if len(d1) != 0 and len(d2) != 0:
            try:
                d1 = float(d1)
                d2 = float(d2)
                if abs(d1) >= 10000 or abs(d2) >= 10000:
                    box.showinfo('Error', 'Некорректные координаты!\nКоордината должна быть числом < 10000, \nразделителем между целой и дробной частями является точка.')
                    return
                text1.insert(END, f'{int(ent5.get())}: ({d1:g}; {d2:g})\n')
            except:
                box.showinfo('Error', 'Некорректные координаты!\nКоордината должна быть числом < 10000, \nразделителем между целой и дробной частями является точка.')
        else:
            num_1 -= 1
            story.append('')
            story[-1] += '; text1.insert(END, "{}: ""{}" + "\\n")'.format(num_1, data[int(ent5.get()) - 1])


        for j in range(int(ent5.get()), len(data)):
            text1.insert(END, f'{j}: ' + data[j] + '\n')
        disable()

        scale()
        update_dots()
        edit = 0
        ent5.delete(0, END)
        return

    if edit == 2:
        data = text2.get(1.0, END).replace(': ', '\n').split('\n')[:-1]
        if not data[-1]:
            data = data[:-1]
        data = data[1::2]

        enable()
        text2.delete(0.0, END)
        for j in range(int(ent6.get()) - 1):
            text2.insert(END, f'{j+1}: ' + data[j] + '\n')
        
        d1 = ent3.get()
        d2 = ent4.get()
        ent3.delete(0, END)
        ent4.delete(0, END)
        if len(d1) != 0 and len(d2) != 0:
            try:
                d1 = float(d1)
                d2 = float(d2)
                if abs(d1) >= 10000 or abs(d2) >= 10000:
                    box.showinfo('Error', 'Некорректные координаты!\nКоордината должна быть числом < 10000, \nразделителем между целой и дробной частями является точка.')
                    return
                text2.insert(END, f'{int(ent6.get())}: ({d1:g}; {d2:g})\n')
            except:
                box.showinfo('Error', 'Некорректные координаты!\nКоордината должна быть числом < 10000, \nразделителем между целой и дробной частями является точка.')
        else:
            num_2 -= 1
            story.append('')
            story[-1] += '; text2.insert(END, "{}: ""{}" + "\\n")'.format(num_2, data[int(ent6.get()) - 1])

        for j in range(int(ent6.get()), len(data)):
            text2.insert(END, f'{j}: ' + data[j] + '\n')
        disable()

        scale()
        update_dots()
        edit = 0
        ent6.delete(0, END)
        return

    if n == 1:
        num = ent5.get()
        if len(num) == 0:
            box.showinfo('info', f'Введите номер точки от 1 до {num_1}' if text1.get(1.0, END) != '\n' else 'нет точек для редактирования')
            return
        try:
            num = int(num)
            if num >= num_1:
                box.showerror('error', 'Такой точки нет')
                return
            
            box.showinfo('info', 'Введите новые координаты точки в поля для координат или оставьте их пустыми для удаления точки и нажмите еще раз эту кнопку')
            edit = 1
        except:
            box.showerror('error', 'Введено не число')
    else:
        num = ent6.get()
        if len(num) == 0:
            box.showinfo('info', f'Введите номер точки от 1 до {num_2}' if text2.get(1.0, END) != '\n' else 'нет точек для редактирования')
            return
        try:
            num = int(num)
            if num >= num_2:
                box.showerror('error', 'Такой точки нет')
                return
            
            box.showinfo('info', 'Введите новые координаты точки в поля для координат или оставьте их пустыми для удаления точки и нажмите еще раз эту кнопку')
            edit = 2
        except:
            box.showerror('error', 'Введено не число')


def print_dot(x, y, num): # Отрисовка точки
    if num == 2:
        c.create_oval(x - 2, y - 2, x + 2, y + 2, outline='blue', fill='blue', tag='dot', activeoutline='violet', activefill='violet')
    else:
        c.create_oval(x - 2, y - 2, x + 2, y + 2, outline='green', fill='green', tag='dot', activeoutline='violet', activefill='violet')


def clean_oval(): # Удаление всех окружностей
    ovals = c.find_withtag('oval')
    for oval in ovals:
        c.delete(oval)

def clean_points(): # Удаление всех точек с поля
    points = c.find_withtag('dot')
    for point in points:
        c.delete(point)

def find_oval(): # Решение задачи
    clean_oval()
    data = text1.get(1.0, END).replace(': ', '\n').split('\n')[:-1]
    if not data[-1]:
        data = data[:-1]
    data = data[1::2]

    data2 = text2.get(1.0, END).replace(': ', '\n').split('\n')[:-1]
    if not data2[-1]:
        data2 = data2[:-1]
    data2 = data2[1::2]

    points = [[data[i], data[j], data[k]] for i in range(len(data)-2) for j in range(i+1, len(data)-1) for k in range(j+1, len(data))]

    r_min = 10000
    a1, b1, x4, y4 = 0, 0, 0, 0
    for dot in points:
        x1, y1 = map(float, dot[0].strip('\n').strip(')').strip('(').split(';'))
        x2, y2 = map(float, dot[1].strip('\n').strip(')').strip('(').split(';'))
        x3, y3 = map(float, dot[2].strip('\n').strip(')').strip('(').split(';'))
        x1, y1 = coord_true(x1, y1)
        x2, y2 = coord_true(x2, y2)
        x3, y3 = coord_true(x3, y3)
        x4, y4 = x1, y1
    
        zx = (y1 - y2) * (x3 * x3 + y3 * y3) + (y2 - y3) * (x1 * x1 + y1 * y1) + (y3 - y1) * (x2 * x2 + y2 * y2)
        zy = (x1 - x2) * (x3 * x3 + y3 * y3) + (x2 - x3) * (x1 * x1 + y1 * y1) + (x3 - x1) * (x2 * x2 + y2 * y2)
        z = (x1 - x2) * (y3 - y1) - (y1 - y2) * (x3 - x1)
        if z == 0:
            continue
        a = -zx / (2 * z)
        b = zy / (2 * z)
        r = sqrt((x1 - a) * (x1 - a) + (y1 - b) * (y1 - b))

        num = 0
        for poi in data2:
            x, y = map(float, poi.strip('\n').strip(')').strip('(').split(';'))
            x, y = coord_true(x, y)
            if ((x - a) * (x - a) + (y - b) * (y - b) < r * r):
                num += 1

        if ((num / len(data2) * 100 if len(data2) > 0 else 100) >= 80 and r_min > r):
            r_min = r
            a1 = a
            b1 = b

    if r_min != 10000:
        story.append('')
        c.create_oval(a1 - r_min, b1 - r_min, a1 + r_min, b1 + r_min, tag='oval')

        a1, b1 = (a1 - 365 * wx) * sz / wx, (550 * wy - b1) * sz  / wy
        text.configure(state=NORMAL)
        text.delete(0.0, END)
        text.insert(1.0, 'Результат:\nцентр - ({:g},{:g})\nрадиус - {:g}'.format(a1, b1, r_min / wx * sz))
        text.configure(state=DISABLED)

        ovals = c.find_withtag('oval')
        for oval in ovals:
            story[-1] += f'c.delete({oval});'
    else:
        if len(points) < 1:
            box.showinfo('Error', 'Точек меньше 3')
        else:
            box.showinfo('Error', 'Окружность не найдена')


def clean_all(): # Очищение всех полей
    clean_points()
    clean_oval()
    enable()
    text1.delete(1.0, END)
    text2.delete(1.0, END)
    ent1.delete(0, END)
    ent2.delete(0, END)
    ent3.delete(0, END)
    ent4.delete(0, END)
    disable()
    text.configure(state=NORMAL)
    text.delete(1.0, END)
    text.configure(state=DISABLED)
    global story
    story = []
    global num_1, num_2
    num_1 = num_2 = 1

def scale(): # Масштабирование
    max = 0
    data = text1.get(1.0, END).replace(': ', '\n').split('\n')[:-1]
    if not data[-1]:
        data = data[:-1]
    data = data[1::2]

    for dot in data:
        x, y = map(float, dot.strip('\n').strip(')').strip('(').split(';'))
        if abs(x) > max:
            max = abs(x)
        if abs(y) > max:
            max = abs(y)   

    data = text2.get(1.0, END).replace(': ', '\n').split('\n')[:-1]
    if not data[-1]:
        data = data[:-1]
    data = data[1::2]

    for dot in data:
        x, y = map(float, dot.strip('\n').strip(')').strip('(').split(';'))
        if abs(x) > max:
            max = abs(x)
        if abs(y) > max:
            max = abs(y)    
    global sz  
    if max == 0:
        sz = 1
        redraw()
        return

    prev_sz = sz
    while max < 150 * sz and 300 * sz < 10000:
        sz /= 2

    while max > 300 * sz and 300 * sz < 10000:
        sz *= 2

    if sz != prev_sz:
        redraw()

def clean_coords(): # Удаление чисел около осей
    coords = c.find_withtag('coord')
    for cor in coords:
        c.delete(cor)

def redraw(): # Перерисовка чисел у осей при масштабировании
    global sz
    clean_oval()
    clean_coords()

    for i in range(50, 350, 50):
        c.create_text(coord_true(-20 * sz, i * sz), text = i * sz, tag='coord')
        c.create_text(coord_true(-20 * sz, -i * sz), text = -i * sz, tag='coord')
        c.create_text(coord_true(i * sz, 15 * sz), text = i * sz, tag='coord')
        c.create_text(coord_true(-i * sz, 15 * sz), text = -i * sz, tag='coord')

    update_dots()



def coord_true(x, y): # Перевод в координаты относительно экрана
    return wx * (365 + x / sz), wy * (550 - y / sz)


def text_and_labels_creation(): # Создание текстовых полей
    text1.place(x=int(wx * 20), y=int(33 * wy))
    scroll = Scrollbar(command=text1.yview)
    scroll.pack(side=LEFT, fill=Y)
    text1.config(yscrollcommand=scroll.set)

    text2.place(x=int(wx * 445), y=int(33 * wy))
    scroll = Scrollbar(command=text2.yview)
    scroll.pack(side=RIGHT, fill=Y)
    text2.config(yscrollcommand=scroll.set)

    text.place(x=int(wx * 710), y=int(wy * 650))
    label1.place(x=int(wx * 20), y=int(wy * 12))
    label2.place(x=int(wx * 445), y=int(wy * 12))
    label4.place(x=int(wx * 20), y=int(wy * 208))


def buttons_creation(): # Создание кнопок
    btn_add1.place(x=int(wx * 222), y=int(wy * 168))
    btn_add2.place(x=int(wx * 646), y=int(wy * 168))
    btn_edit1.place(x=int(wx * 222), y=int(wy * 207))
    btn_edit2.place(x=int(wx * 646), y=int(wy * 207))
    btn_cl_all.place(x=int(wx * 315), y=int(wy * 140))
    btn_back.place(x=int(wx * 315), y=int(wy * 170))
    btn_oval.place(x=int(wx * 315), y=int(wy * 110))


def coordinate_field_creation(): # Создание осей координат и сетки
    lines = c.find_withtag('line')
    for line in lines:
        c.delete(line)
    clean_coords()

    c.create_line(int(33 * wx), int(wy * 550), int(wx * 690), int(wy * 550), fill='black',
                  width=3, arrow=LAST, arrowshape="10 17 6", tag='line')
    c.create_line(int(wx * 365), int(wy * 860), int(wx * 365), int(wy * 210), fill='black',
                  width=3, arrow=LAST, arrowshape="10 17 6", tag='line')
    c.create_text(int(wx * 355), int(wy * 562), text='0', tag='coord')

    for i in range(50, 350, 50):
        c.create_line(coord_true(-5 * sz, i * sz), coord_true(5 * sz, i * sz), fill='black', width=2, tag='line')
        c.create_line(coord_true(-5 * sz, -i * sz), coord_true(5 * sz, -i * sz), fill='black', width=2, tag='line')
        c.create_line(coord_true(i * sz, -5 * sz), coord_true(i * sz, 5 * sz), fill='black', width=2, tag='line')
        c.create_line(coord_true(-i * sz, -5 * sz), coord_true(-i * sz, 5 * sz), fill='black', width=2, tag='line')
        c.create_text(coord_true(-20 * sz, i * sz), text = i * sz, tag='coord')
        c.create_text(coord_true(-20 * sz, -i * sz), text = -i * sz, tag='coord')
        c.create_text(coord_true(i * sz, 15 * sz), text = i * sz, tag='coord')
        c.create_text(coord_true(-i * sz, 15 * sz), text = -i * sz, tag='coord')
        c.create_line(coord_true(-300 * sz, i * sz), coord_true(300 * sz, i * sz), fill='black', width=1, dash=(1, 9), tag='line')
        c.create_line(coord_true(-300 * sz, -i * sz), coord_true(300 * sz, -i * sz), fill='black', width=1, dash=(1, 9), tag='line')
        c.create_line(coord_true(i * sz, -300 * sz), coord_true(i * sz, 300 * sz), fill='black', width=1, dash=(1, 9), tag='line')
        c.create_line(coord_true(-i * sz, -300 * sz), coord_true(-i * sz, 300 * sz), fill='black', width=1, dash=(1, 9), tag='line')
        
    c.create_text(coord_true(320, 15), text='X', font='Verdana 13', fill='black', tag='line')
    c.create_text(coord_true(15, 340), text='Y', font='Verdana 13', fill='black', tag='line')


def radiobutton_creation(): # Создание переключателя
    var.set(0)
    label3.place(x=int(wx * 315), y=int(wy *12))
    set0.place(x=int(wx * 315), y=int(wy * 55))
    set1.place(x=int(wx * 315), y=int(wy * 77))

def redraw_window():
    c.configure(width=wx * 900, height=wy * 900)
    text1.configure(width=int(wx * 36), height=int(wy * 10))
    text2.configure(width=int(wx * 36), height=int(wy * 10))
    text.configure(width=int(wx * 25), height=int(wy * 10))
    ent1.configure(width=int(wx * 8))
    ent2.configure(width=int(wx * 8))
    ent3.configure(width=int(wx * 8))
    ent4.configure(width=int(wx * 8))
    ent5.configure(width=int(wx * 4))
    ent6.configure(width=int(wx * 4))

    ent1.place(x=int(wx * 32), y=int(wy * 172))
    ent2.place(x=int(wx * 132), y=int(wy * 172))
    ent3.place(x=int(wx * 460), y=int(wy * 172))
    ent4.place(x=int(wx * 560), y=int(wy * 172))
    ent5.place(x=int(wx * 178), y=int(wy * 215))
    ent6.place(x=int(wx * 600), y=int(wy * 215))

    text_and_labels_creation()
    buttons_creation()
    coordinate_field_creation()
    radiobutton_creation()
    update_dots()

def config(event):
    global wx, wy
    if event.widget == root:
        x, y = root.geometry().split('x')
        y = int(y.split('+')[0])
        x = int(x)
        if x != 900 or y != 900:
            wx, wy = x / 900, y / 900
        redraw_window()
        

btn_add1 = Button(c, text='добавить', fg='green', command=lambda: add_dot(1))
btn_back = Button(c, text='назад', fg='purple', command=lambda: back())
btn_add2 = Button(c, text='добавить', fg='blue', command=lambda: add_dot(2))
btn_oval = Button(c, text='найти Ｏ', fg='purple', command=lambda: find_oval())
btn_cl_all = Button(c, text='очистить все', fg='purple', command=lambda: clean_all())
btn_edit1 = Button(c, text='редакт.', fg='green', command=lambda: edit_dot(1))
btn_edit2 = Button(c, text='редакт.', fg='blue', command=lambda: edit_dot(2))
label1 = Label(c, text='Точки первого множества:')
label2 = Label(c, text='Точки второго множества:')
label4 = Label(c, text='Номер точки \nдля редактирования:')
label3 = Label(c, text='Ввод точек \nна плоскости:')
set0 = Radiobutton(c, text="1-го мн-ва", fg='green', variable=var, value=0)
set1 = Radiobutton(c, text="2-го мн-ва", fg='blue', variable=var, value=1)

c.bind('<1>', click)
root.bind('<Configure>', config)

text_and_labels_creation()
buttons_creation()
coordinate_field_creation()
radiobutton_creation()

mmenu = Menu(root)
add_menu = Menu(mmenu)
add_menu.add_command(label='О программе и авторе', command=lambda: messagebox.showinfo('О программе и авторе', TASK + AUTHOR))
add_menu.add_command(label='Выход', command=exit)
mmenu.add_cascade(label='About', menu=add_menu)
root.config(menu=mmenu)

c.pack()
root.mainloop()
