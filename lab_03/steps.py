import matplotlib.pyplot as plt
from itertools import count, takewhile
def frange(start, stop, step):
    return takewhile(lambda x: x< stop, count(start, step))


r = 0
angle_step = 0
    
with open("../lab_03/steps_res.txt", "r") as f:
    r = float(f.readline().replace(",", "."))
    angle_step = float(f.readline().replace(",", "."))
    max_angle = float(f.readline().replace(",", "."))
    steps = []
    for line in f:
        steps.append(float(line.replace(",", ".")))
       
angles = list(frange(0, max_angle, angle_step))

plt.title("Анализ ступенчатости")
plt.xlabel("Угол наклона прямой")
plt.ylabel(f"Число ступеней\nДлина отрезка - {r}")
plt.grid(True)
plt.plot(angles, steps[:len(angles)], label='ЦДА')
plt.plot(angles, steps[len(angles):2*len(angles)], label='Брезенхем целочисленный')
plt.plot(angles, steps[2*len(angles):3*len(angles)], label='Брезенхем действительный')
plt.plot(angles, steps[3*len(angles):4*len(angles)], label='Брезенхем сглаживающий')
plt.plot(angles, steps[4*len(angles):5*len(angles)], label='By')

plt.show()
