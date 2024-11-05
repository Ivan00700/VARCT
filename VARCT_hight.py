import krpc
import matplotlib.pyplot as plt
import time as t


def main():
    # Подключение к серверу kRPC
    conn = krpc.connect('hight_checker')
    vessel = conn.space_center.active_vessel

    # Создание массивов для данных о времени и высоте
    time_values = []
    altitude_values = []
    time = 0

    # Получение высоты корабля на протяжении полета
    while True:
        altitude = vessel.flight().surface_altitude
        time_values.append(time)  # Запись текущего времени в массив
        altitude_values.append(altitude)  # Запись текущей высоты в массив

        # Вывод считываемых данных в консоль
        print("Время: {}, Высота: {} м".format(time, altitude))
        t.sleep(1)  # КД 1 секунда для умеренных данных
        time += 1
        # Проверка условия завершения сбора данных
        if altitude > 90_000:  # Остановка считывания данных при наборе высоты 90км
            # 90км тк это идеальный апогей для перехода к другим планетам Кербальской Солнечной системы
            break

    # Построение графика высоты от времени с помощью бибилиотеки pyplot
    plt.plot(time_values, altitude_values)
    plt.title('Зависимость высоты от времени')
    plt.xlabel('Время, s')
    plt.ylabel('Высота, m')
    plt.show()


if __name__ == "__main__":
    main()
