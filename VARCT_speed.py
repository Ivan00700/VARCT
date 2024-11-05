import krpc
import matplotlib.pyplot as plt


def main():
    # Подключение к серверу kRPC
    conn = krpc.connect('speed_checker')
    vessel = conn.space_center.active_vessel

    # Создание массивов для данных о времени и скорости
    time_array = []
    speed_array = []

    # Получение скорости корабля на во время полета
    while True:
        time = conn.space_center.ut  # Текущее время
        speed = vessel.flight(vessel.orbit.body.reference_frame).speed  # Получение текущей скорости
        time_array.append(time)  # Запись текущего времени в массив
        speed_array.append(speed)  # Запись текущей скорости в массив
        print("Время: {}, Скорость корабля: {} м/с".format(time, speed))  # Вывод считываемых данных в консоль

        # Проверка условия завершения сбора данных по достижении определенной высоты
        altitude = vessel.flight().surface_altitude
        if altitude > 90_000:  # Остановка считывания данных при наборе высоты 90км (начальный апоцентр)
            # 90км тк это идеальный апогей для перехода к другим планетам Кербальской Солнечной системы
            break

    # Построение графика скорости от времени
    plt.plot(time_array, speed_array)
    plt.title('Зависимость скорости от времени')
    plt.xlabel('Время, s')
    plt.ylabel('Скорость, m/s')
    plt.show()


if __name__ == "__main__":
    main()
