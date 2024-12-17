import numpy as np
import matplotlib.pyplot as plt

# 1. Загрузка данных
data = [3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, 18, 19, 21, 23, 25, 27, 29, 31, 34, 36, 39, 41, 44, 47, 50, 53, 56, 59, 62, 66, 70, 73, 77, 81, 86, 90, 95, 99, 104, 109, 115, 120, 125, 131, 137, 143, 150, 156, 163, 170, 177, 185, 193, 201, 209, 218, 227, 236, 246, 256, 267, 277, 288, 299, 311, 320, 319, 325, 333, 340, 348, 355, 364, 371, 380, 389, 398, 407, 416, 426, 436, 446, 457, 468, 479, 491, 503, 515, 528, 540, 554, 567, 581, 595, 610, 624, 640, 654, 670, 686, 702, 718, 736, 752, 770, 787, 805, 823, 842, 860, 880, 899, 919, 939, 959, 979, 1001, 1022, 1044, 1066, 1088, 1110, 1133, 1156, 1180, 1182, 1190]

data = [float(x) for x in data]

# 2. Создание массива времени
time_data = np.arange(0, len(data), 1)

# 3. Моделирование (метод Эйлера, без сопротивления воздуха)
g = 9.81
dt = 0.1
k = 13
Isp1 = 4700
Isp2 = 2700
delta_v1 = 4600
delta_v2 = 6600
t_stage1 = 70
M0 = 948762
Cd = 0.15  # Убрали, но оставили
A = 4.5  # Убрали, но оставили
rho = 1.225  # Убрали, но оставили

M_dry = M0 / (k + 1)
M_fuel = M0 * k / (k + 1)

m_dry1 = M_dry / (1 + 9.7) * 2.718
m_fuel1 = m_dry1 * k
m_0_stage1 = m_dry1 + m_fuel1

m_dry2 = M_dry - m_dry1
m_fuel2 = m_dry2 * k

v_e1 = Isp1
v_e2 = Isp2

F1 = m_fuel1 * v_e1 / t_stage1 * 0.75
mdot1 = F1 / v_e1

F2 = 17000000
mdot2 = F2 / v_e2
t_stage2 = 125
t = 0
m = M0
v = 0
time_model = [0]
velocity_model = [0]
stage = 1
m_current = M0


def acceleration(t, m, v, stage):
    if stage == 1:
        if t > t_stage1:
            return -g
        else:
            return (F1) / m - g  # Убрали drag
    elif stage == 2:
        if t > t_stage2 or m - m_dry2 <= 0:
            return -g
        else:
            return (F2) / m - g  # Убрали drag
    else:
        return -g


while t <= 125:
    if stage == 1:
        if t > t_stage1:
            stage = 2
            m_current = m - m_dry1 - m_fuel1
            v = velocity_model[-1]
        else:
            a = acceleration(t, m_current, v, stage)  # Используем метод Эйлера
            v += a * dt
            m_current -= mdot1 * dt
    elif stage == 2:
        if t > t_stage2 or m_current - m_dry2 <= 0:
            stage = 3
            a = acceleration(t, m_current, v, stage)
            v += a * dt

        else:
            a = acceleration(t, m_current, v, stage)  # Используем метод Эйлера
            v += a * dt
            m_current -= mdot2 * dt
    else:
        a = acceleration(t, m_current, v, stage)  # Используем метод Эйлера
        v += a * dt

    t += dt
    time_model.append(t)
    velocity_model.append(v)

# 4. Построение графика
plt.figure(figsize=(10, 6))
plt.plot(time_data, data, label='Данные из KSP', linewidth=3)
plt.plot(time_model, velocity_model, label='Моделирование', linestyle='--')
plt.xlabel("Время (с)", fontsize=12)
plt.ylabel("Скорость (м/с)", fontsize=12)
plt.title("Сравнение скорости ракеты: данные KSP vs. модель", fontsize=14)
plt.legend(fontsize=10)
plt.grid(True)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.show()