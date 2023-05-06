from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import colorchooser

lineColor = '#79b4f6'
cutterColor = '#de74a4'
resultColor = '#44d036'

class App():
    def __init__(self) -> None:
        self.root = Tk()
        style = ttk.Style(self.root)
        style.configure('default.TButton', font='"Segoe UI Variable" 12')
        style.configure('black.TButton', background='#000000')
        style.configure('white.TButton', background='#ffffff')
        style.configure('red.TButton', background='#ff0000')
        style.configure('green.TButton', background='#00ff00')
        style.configure('blue.TButton', background='#0000ff')

        self.root.geometry('1000x700+250+50')
        self.root.title('Лабораторная работа №8')
        self.root.minsize(900, 630)
        self.root.grab_set()
        self.root.focus_get()

        self.frame = ttk.Frame(self.root)
        self.frame.place(relwidth=0.3, relheight=1)

        self.canv = Canvas(self.root, highlightthickness=0, bg='white')
        self.canv.place(relwidth=0.7, relheight=1, relx=0.3)

        self.menubar = Menu(self.root)
        self.actionmenu = Menu(self.menubar, tearoff='off')
        self.actionmenu.add_command(label='Выход', command=self.root.destroy)
        self.menubar.add_cascade(label='Действия', menu=self.actionmenu)
        self.infomenu = Menu(self.menubar, tearoff='off')
        self.infomenu.add_command(label='О программе', command=self.prog_info)
        self.infomenu.add_command(label='Об авторе', command=self.author_info)
        self.menubar.add_cascade(label='Информация', menu=self.infomenu)
        self.root.config(menu=self.menubar)

        self.canv.bind("<Configure>", self.configure)

        self.all_lines = []

        self.verteces_list = []
        self.sections = []
        self.last_point = [None, None]

        self.lab_color = Label(self.frame, justify='center', text='ЦВЕТ', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_color.place(rely=0.02, relwidth=1)

        self.curCutterColor = ttk.Label(self.frame)

        self.btn_changeCutterColor = ttk.Button(self.frame, text='Выбрать цвет отсекателя', style='default.TButton', command=self.get_color_cutter)
        self.btn_changeCutterColor.place(relwidth=0.78, relx=0.04, rely=0.07, relheight=0.04)

        self.curCutterColor.configure(background=cutterColor)
        self.curCutterColor.place(relx=0.84, relwidth=0.14, rely=0.075, relheight=0.03)

        self.curLineColor = ttk.Label(self.frame)

        self.btn_changeLineColor = ttk.Button(self.frame, text='Выбрать цвет отрезка', style='default.TButton', command=self.get_color_line)
        self.btn_changeLineColor.place(relwidth=0.78, relx=0.04, rely=0.12, relheight=0.04)

        self.curLineColor.configure(background=lineColor)
        self.curLineColor.place(relx=0.84, relwidth=0.14, rely=0.125, relheight=0.03)

        self.curResultColor = ttk.Label(self.frame)

        self.btn_changeResultColor = ttk.Button(self.frame, text='Выбрать цвет результата', style='default.TButton', command=self.get_color_result)
        self.btn_changeResultColor.place(relwidth=0.78, relx=0.04, rely=0.17, relheight=0.04)

        self.curResultColor.configure(background=resultColor)
        self.curResultColor.place(relx=0.84, relwidth=0.14, rely=0.175, relheight=0.03)

        self.lab_cutter = Label(self.frame, justify='center', text='ОТСЕКАТЕЛЬ', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_cutter.place(rely=0.23, relwidth=1)

        self.btn_addPointCutter = ttk.Button(self.frame, text='Добавить точку', style='default.TButton', command=self.set_cutter)
        self.btn_addPointCutter.place(relwidth=0.92, relx=0.05, rely=0.32, relheight=0.04)

        self.btn_closeCutter = ttk.Button(self.frame, text='Замкнуть отсекатель', style='default.TButton', command=lambda: self.return_click(0))
        self.btn_closeCutter.place(relwidth=0.92, relx=0.05, rely=0.37, relheight=0.04)

        self.ent_xlt = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_xlt.insert(0,'X')
        self.ent_xlt.place(relwidth=0.425, relx=0.05, rely=0.27, relheight=0.04)

        self.ent_ylt = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_ylt.insert(0,'Y')
        self.ent_ylt.place(relwidth=0.425, relx=0.525, rely=0.27, relheight=0.04)

        self.cutter_id = -1
        self.cutter_coords = []
        self.cutter_coords_tmp = []

        self.canv.bind('<Button-3>', self.right_click)
        self.root.bind("<Return>", self.return_click)

        self.ent_xlt.bind('<Button-1>', self.entry_mode_xlt)
        self.ent_ylt.bind('<Button-1>', self.entry_mode_ylt)

        self.lab_line = Label(self.frame, justify='center', text='ОТРЕЗОК', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_line.place(rely=0.43, relwidth=1)

        self.ent_xb = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_xb.insert(0,'Xн')
        self.ent_xb.place(relwidth=0.425, relx=0.05, rely=0.47, relheight=0.04)

        self.ent_yb = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_yb.insert(0,'Yн')
        self.ent_yb.place(relwidth=0.425, relx=0.525, rely=0.47, relheight=0.04)

        self.ent_xe = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_xe.insert(0,'Xк')
        self.ent_xe.place(relwidth=0.425, relx=0.05, rely=0.52, relheight=0.04)

        self.ent_ye = ttk.Entry(self.frame, justify=CENTER, foreground='gray')
        self.ent_ye.insert(0,'Yк')
        self.ent_ye.place(relwidth=0.425, relx=0.525, rely=0.52, relheight=0.04)

        self.line_coords = []

        self.btn_addLine = ttk.Button(self.frame, text='Добавить', style='default.TButton', command=self.add_line)
        self.btn_addLine.place(relwidth=0.92, relx=0.04, rely=0.57, relheight=0.04)

        self.canv.bind('<Button-1>', self.left_click)

        self.ent_xb.bind('<Button-1>', self.entry_mode_xb)
        self.ent_yb.bind('<Button-1>', self.entry_mode_yb)
        self.ent_xe.bind('<Button-1>', self.entry_mode_xe)
        self.ent_ye.bind('<Button-1>', self.entry_mode_ye)

        self.lab_cut = Label(self.frame, justify='center', text='ОТСЕЧЕНИЕ', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_cut.place(rely=0.70, relwidth=1)

        self.btn_cut = ttk.Button(self.frame, text='Выполнить отсечение', style='default.TButton', command=self.solve)
        self.btn_cut.place(relwidth=0.92, relx=0.04, rely=0.74, relheight=0.04)

        self.frame.bind_all('<Button-1>', self.unfocus)

        self.lab_clean = Label(self.frame, justify=CENTER, text='ОЧИСТКА КАНВАСА', foreground='gray', font='"Segoe UI Variable" 10')
        self.lab_clean.place(rely=0.89, relwidth=1)

        self.btn_clean = ttk.Button(self.frame, text='Очистить', style='default.TButton', command=self.clean)
        self.btn_clean.place(relwidth=0.9, relx=0.05, rely=0.93, relheight=0.04)

        self.root.mainloop()
    
    def get_color_cutter(self):
        global cutterColor
        _, hex_code = colorchooser.askcolor(
            parent=self.root,
            title="Выберите цвет для закрашивания",
            initialcolor=cutterColor
        )
        self.curCutterColor['background'] = hex_code
        cutterColor = hex_code
    
    def get_color_line(self):
        global lineColor
        _, hex_code = colorchooser.askcolor(
            parent=self.root,
            title="Выберите цвет для закрашивания",
            initialcolor=lineColor
        )
        self.curLineColor['background'] = hex_code
        lineColor = hex_code
    
    def get_color_result(self):
        global resultColor
        _, hex_code = colorchooser.askcolor(
            parent=self.root,
            title="Выберите цвет для закрашивания",
            initialcolor=resultColor
        )
        self.curResultColor['background'] = hex_code
        resultColor = hex_code

    def clean(self):
        self.canv.delete('all')
        self.sections.clear()
        self.verteces_list.clear()
    
    def draw_section(self, xb, yb, xe, ye, color):
        self.canv.create_line(xb, yb, xe, ye, fill=color)

    def left_click(self, event):
        if self.last_point[0]:
            self.sections.append([self.last_point[:], [event.x, event.y]])
            self.draw_section(*self.sections[-1][0], *self.sections[-1][1], lineColor)
            self.last_point[0] = None
        else:
            self.last_point[0], self.last_point[1] = event.x, event.y

    def return_click(self, event):
        if len(self.verteces_list) < 3:
            return
        self.draw_section(*self.verteces_list[-1], *self.verteces_list[0], cutterColor)

    def right_click(self, event):
        self.verteces_list.append([event.x, event.y])
        if len(self.verteces_list) >= 2:
            self.draw_section(*self.verteces_list[-1], *self.verteces_list[-2], cutterColor)

    def add_line(self):
        try:
            x1 = int(self.ent_xb.get())
            y1 = int(self.ent_yb.get())
            x2 = int(self.ent_xe.get())
            y2 = int(self.ent_ye.get())
        except:
            messagebox.showerror("Неверный ввод", "Не удалось считать коориданаты вершины")
            return
        
        self.sections.append([[x1, y1], [x2, y2]])
        self.draw_section(*self.sections[-1][0], *self.sections[-1][1], lineColor)

    def set_cutter(self):
        try:
            x = int(self.ent_xlt.get())
            y = int(self.ent_ylt.get())
        except:
            messagebox.showerror("Неверный ввод", "Не удалось считать коориданаты очередной вершины")
            return
        self.verteces_list.append([x, y])
        if len(self.verteces_list) >= 2:
            self.draw_section(*self.verteces_list[-1], *self.verteces_list[-2], cutterColor)

    def get_vect(self, p1, p2):
        return [p2[0] - p1[0], p2[1] - p1[1]]

    def vect_mul(self, v1, v2):
        return v1[0] * v2[1] - v1[1] * v2[0]

    def scalar_mul(self, v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1]
    
    def check_polygon(self):
        if len(self.verteces_list) < 3:
            return False
        sign = 1 if self.vect_mul(self.get_vect(self.verteces_list[1], self.verteces_list[2]),
                            self.get_vect(self.verteces_list[0], self.verteces_list[1])) > 0 else -1
        for i in range(3, len(self.verteces_list)):
            if sign * self.vect_mul(self.get_vect(self.verteces_list[i - 1], self.verteces_list[i]),
                            self.get_vect(self.verteces_list[i - 2], self.verteces_list[i - 1])) < 0:
                return False

        if sign * self.vect_mul(self.get_vect(self.verteces_list[0], self.verteces_list[1]),
                            self.get_vect(self.verteces_list[len(self.verteces_list) - 1], self.verteces_list[0])) < 0:
            return False

        if sign < 0:
            self.verteces_list.reverse()

        return True
    
    def get_normal(self, p1, p2, cp):
        vect = self.get_vect(p1, p2)
        norm = [1, 0] if vect[0] == 0 else [-vect[1] / vect[0], 1]
        if self.scalar_mul(self.get_vect(p2, cp), norm) < 0:
            for i in range(len(norm)):
                norm[i] = -norm[i]
        return norm

    def get_normals_list(self, verteces):
        length = len(self.verteces_list)
        normal_list = list()
        for i in range(length):
            normal_list.append(self.get_normal(verteces[i], verteces[(i + 1) % length], verteces[(i + 2) % length]))

        return normal_list

    def cut(self, section, verteces_list, normals_list):
        t_start = 0
        t_end = 1
        d = self.get_vect(section[0], section[1])

        for i in range(len(verteces_list)):
            if verteces_list[i] != section[0]:
                wi = self.get_vect(verteces_list[i], section[0])
            else:
                wi = self.get_vect(verteces_list[(i + 1) % len(verteces_list)], section[0])
            Dck = self.scalar_mul(d, normals_list[i])
            Wck = self.scalar_mul(wi, normals_list[i])

            if Dck == 0:
                if self.scalar_mul(wi, normals_list[i]) < 0:
                    return
                else:
                    continue

            t = -Wck / Dck
            if Dck > 0:
                if t > t_start:
                    t_start = t
            else:
                if t < t_end:
                    t_end = t

            if t_start > t_end:
                break
        
        if t_start < t_end:
            p1 = [round(section[0][0] + d[0] * t_start), round(section[0][1] + d[1] * t_start)]
            p2 = [round(section[0][0] + d[0] * t_end), round(section[0][1] + d[1] * t_end)]
            self.draw_section(*p1, *p2, resultColor)

    def solve(self):
        if not self.check_polygon():
            messagebox.showerror("Невыпуклый многоугольник", "Для осуществления отсечения отрезка алгоритмом Кируса-Бека \
                        многоугольник должен быть выпуклым")
            return
        
        big_list = list()
        for vertex in self.verteces_list:
            big_list.extend(vertex)
        self.canv.create_polygon(*big_list, outline=cutterColor, fill="#FFFFFF")
        
        normals_list = self.get_normals_list(self.verteces_list)
        for section in self.sections:
            self.cut(section, self.verteces_list, normals_list)
        
    def entry_mode_xlt(self, event):
        if (self.ent_xlt.get() == 'X'):
            self.ent_xlt.delete(0, END)
            self.ent_xlt['foreground'] = '#000000'

    def entry_mode_ylt(self, event):
        if (self.ent_ylt.get() == 'Y'):
            self.ent_ylt.delete(0, END)
            self.ent_ylt['foreground'] = '#000000'
    
    def entry_mode_xb(self, event):
        if (self.ent_xb.get() == 'Xн'):
            self.ent_xb.delete(0, END)
            self.ent_xb['foreground'] = '#000000'

    def entry_mode_yb(self, event):
        if (self.ent_yb.get() == 'Yн'):
            self.ent_yb.delete(0, END)
            self.ent_yb['foreground'] = '#000000'
    
    def entry_mode_xe(self, event):
        if (self.ent_xe.get() == 'Xк'):
            self.ent_xe.delete(0, END)
            self.ent_xe['foreground'] = '#000000'

    def entry_mode_ye(self, event):
        if (self.ent_ye.get() == 'Yк'):
            self.ent_ye.delete(0, END)
            self.ent_ye['foreground'] = '#000000'

    def unfocus(self, event):
        if event.widget != self.ent_xlt:
            if self.ent_xlt.get() == '':
                self.ent_xlt.insert(0, 'X')
                self.ent_xlt['foreground'] = 'gray'
                event.widget.focus()
        if event.widget != self.ent_ylt:
            if self.ent_ylt.get() == '':
                self.ent_ylt.insert(0, 'Y')
                self.ent_ylt['foreground'] = 'gray'
                event.widget.focus()
        if event.widget != self.ent_xb:
            if self.ent_xb.get() == '':
                self.ent_xb.insert(0, 'Xн')
                self.ent_xb['foreground'] = 'gray'
                event.widget.focus()
        if event.widget != self.ent_yb:
            if self.ent_yb.get() == '':
                self.ent_yb.insert(0, 'Yн')
                self.ent_yb['foreground'] = 'gray'
                event.widget.focus()
        if event.widget != self.ent_xe:
            if self.ent_xe.get() == '':
                self.ent_xe.insert(0, 'Xк')
                self.ent_xe['foreground'] = 'gray'
                event.widget.focus()
        if event.widget != self.ent_ye:
            if self.ent_ye.get() == '':
                self.ent_ye.insert(0, 'Yк')
                self.ent_ye['foreground'] = 'gray'
                event.widget.focus()
        
    def configure(self, event):
        w, h = event.width, event.height
        self.canv.config(width=w, height=h)
    
    def prog_info(self):
        messagebox.showinfo(title='О программе', message='Реализация алгоритма отсечения отрезка произвольным выпуклым отсекателем.\n')
        
    def author_info(self):
        messagebox.showinfo(title='Об авторе', message='Пронина Лариса ИУ7-44Б')

if __name__ == '__main__':
    win = App()