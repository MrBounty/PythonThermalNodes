import numpy as np


class Vec3D:
    def __init__(self, x, y, z):
        self.data = np.array([x, y, z])

    @property
    def x(self):
        return self.data[0]

    @x.setter
    def x(self, val):
        self._x = val
        self.data[0] = val

    @property
    def y(self):
        return self.data[1]

    @y.setter
    def y(self, val):
        self._y = val
        self.data[1] = val

    @property
    def z(self):
        return self.data[2]

    @z.setter
    def z(self, val):
        self._z = val
        self.data[2] = val


class Vec2D:
    def __init__(self, x, y):
        self.data = np.array([x, y])

    @property
    def x(self):
        return self.data[0]

    @x.setter
    def x(self, val):
        self._x = val
        self.data[0] = val

    @property
    def y(self):
        return self.data[1]

    @y.setter
    def y(self, val):
        self._y = val
        self.data[1] = val
