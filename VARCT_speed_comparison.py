import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import constants
import json

with open("data_speed_file.json", "r") as file:
    data_speed = json.load(file)


# Функции для проверки на то, осталось ли топливо в ступени. Если есть, то возвращает 1, иначе - 0
def f1(t):
    global t1
    return t1 - t > 0


def f2(t):
    global t1
    global t2

    return (t1 + t2 - t > 0) and (t1 - t <= 0)


def f3(t):
    global t1
    global t2
    global t3

    return (t1 + t2 - t <= 0) and (t3 + t2 + t1 - t > 0)


temp = 90


# Функция для вычисления угла, связанным с косинусом, в математической модели
def alpha():
    global temp
    temp += 0.1
    return temp * (math.pi / 180)  # Перевод значений угла в градусы


temp_1 = 360


# Функция для вычисления угла, связанным с синусом, в математической модели
def beta():
    global temp_1
    temp_1 += 0.05  # Изменение

    return temp_1 * (math.pi / 180)  # Перевод значений угла в градусы


u = 0  # Скорость ракеты
t1 = 71  # Время, за которое уйдет все топливо из первой ступени
t2 = 39  # Время, за которое уйдет все топливо из второй ступени
t3 = 83  # Время, за которое уйдет все топливо из третьей ступени
g = constants.g  # Ускорение свободного падения
m1 = 210_703  # Масса топлива первой ступени
m2 = 108_753  # Масса топлива второй ступени
m3 = 69_366  # Масса топлива третьей ступени
M0 = 11_556  # Масса полезной нагрузки

I1 = 29  # Удельный импульс 1
I2 = 5  # Удельный импульс 2
I3 = 12  # Удельный импульс 3

M21 = 465_000  # Масса первой ступени без топлива
M22 = 210_703  # Масса второй ступени без топлива
M23 = 69_000  # Масса третьей ступени без топлива

Ni1 = m1 / t1  # Ню1
Ni2 = m2 / t2  # Ню2
Ni3 = m3 / t3  # Ню3
t0 = 0  # Время
speed_values = []  # Массив скоростей
time = []  # Массив по пройденному времени

for _ in range(sum([t1, t2, t3])):  # Идем от 0 секунды до суммы времени, за которое уйдет все топливо из ступеней
    t = 1
    t0 += 1
    # Расчет скорости
    u += (f1(t0) * I1 *
          math.log((M0 + M21 + m1 - (Ni1 * t * f1(t0)) + M22 + m2 - Ni2 * t * f3(t0) + M23 + m3 - Ni3 * t * f3(t0)) /
                   (M0 + M21 + M22 + m2 - Ni2 * t * f2(t0) + M23 + m3 - Ni3 * t * f3(t0))) + f2(t0) * I2 *
          math.log((M0 + M22 + m2 - (Ni2 * (t - t2) * f2(t0)) + M23 + m3 - Ni3 * (t - t2) * f3(t0))
                   / (M0 + M22 + M23 + m3 - Ni3 * t * f3(t0))) + f3(t0) * I3 *
          math.log((M0 + M23 + m3 - Ni3 * (t - t3 - t2) * f3(t0))
                   / (M0 + M23))) - ((f1(t0) * I1 * Ni2 * g * (1 - math.cos(alpha()))) /
                                     (M0 + M21 + m1 - Ni1 * t * f1(t0) + M22 + m2 - Ni2 * t * f3(
                                         t0) + M23 + m3 - Ni3 * t * f3(t0))) - (
                 (f2(t0) * I2 * Ni2 * g * (1 - math.cos(alpha()))) /
                 (M0 + M22 + m2 - Ni2 * t * f2(t0) + M23 + m3 - Ni3 * t * f3(t0))) - (
                 (f3(t0) * I3 * Ni3 * g * (1 - math.cos(alpha()))) /
                 (M0 + M23 + m3 - Ni3 * t * f3(t0))) - g * math.sin(beta())

    speed_values.append(u)  # Добавление текущей скорости
    time.append(t0)  # Добавление текущего времени

x = np.array(time)  # Многомерный массив по значениям х для построения графика
y = np.array(speed_values)  # Многомерный массив по значениям y для построения графика
x1 = np.array([i for i in range(175)])
y1 = np.array(data_speed)

plt.title('График скорости ракеты от времени\n', fontsize=12, fontweight="bold")  # Титульник на графике
plt.ylabel("Скорость V(t)", fontsize=14)  # Описание функции y на графике
plt.xlabel("Время t", fontsize=14)  # Описание функции x на графике
plt.plot(x, y, 'r', label="график мат.модели")  # r, g - red, green colour
plt.plot(x1, y1, 'g', label="график KSP")  # r, g - red, green colour
plt.legend()
plt.show()  # Вывод графика
