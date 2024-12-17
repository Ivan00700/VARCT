import krpc
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

try:
    conn = krpc.connect(name='Trajectory')
    vessel = conn.space_center.active_vessel

    # Списки данных
    x_coords = []
    y_coords = []
    z_coords = []
    time_list = []

    # Установка графика
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    line, = ax.plot(x_coords, y_coords, z_coords)
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Траектория ракеты в Оxyz')

    ref_frame = vessel.orbit.body.reference_frame

    # Сбор данных
    start_time = time.time()
    while True:
        try:
            current_time = time.time() - start_time
            current_position = vessel.position(ref_frame)
            # Меняем ось Y и Z для лучшей наглядности
            x_coords.append(current_position[0])  #X
            y_coords.append(current_position[2])  #Z
            z_coords.append(current_position[1])  #Y
            time_list.append(current_time)

            line.set_data_3d(x_coords, y_coords, z_coords)

            # Лимиты
            ax.set_xlim(min(x_coords), max(x_coords))
            ax.set_ylim(min(y_coords), max(y_coords))
            ax.set_zlim(min(z_coords), max(z_coords))

            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(0.1)
        except Exception as e:
            print(f"Error data collection: {e}")
            break

except krpc.ConnectionError as e:
    print(f"Connection error: {e}")
except KeyboardInterrupt:
    print("Закрытие графика")  # Ctrl+C
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    if 'conn' in locals() and conn:
        conn.close()
    plt.close()