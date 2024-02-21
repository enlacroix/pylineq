from enum import Enum


class SLESols(Enum):
    INFSOL = 'У системы бесконечно много решений.'
    UNIQSOL = 'У системы одно решение.'
    NOSOL = 'У системы нет решения.'

# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
#
# # Задаем два вектора v1 и v2 типа float
# v1 = np.array([1.0, 2.0, 3.0], dtype=float)
# v2 = np.array([4.0, 5.0, 6.0], dtype=float)
#
# # Находим векторное произведение для получения нормали к плоскости
# normal = np.cross(v1, v2)
#
# # Задаем начальную точку для построения плоскости
# point = np.array([0.0, 0.0, 0.0], dtype=float)
#
# # Создаем сетку точек в плоскости
# xx, yy = np.meshgrid(range(10), range(10))
#
# # Находим z координату для каждой точки с помощью уравнения плоскости ax + by + cz + d = 0
# d = -np.sum(point * normal)
# z = (-normal[0] * xx - normal[1] * yy - d) * 1. / normal[2]
#
# # Визуализируем плоскость
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(xx, yy, z, alpha=0.5)
#
# # Добавляем вектора на график
# ax.quiver(0, 0, 0, v1[0], v1[1], v1[2], color='r', arrow_length_ratio=0)
# ax.quiver(0, 0, 0, v2[0], v2[1], v2[2], color='g', arrow_length_ratio=0)
#
# # Находим нормаль к плоскости
# normal /= np.linalg.norm(normal)
# ax.quiver(0, 0, 0, normal[0], normal[1], normal[2], color='b', arrow_length_ratio=0)
#
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
#
# plt.show()
