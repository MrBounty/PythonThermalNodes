import matplotlib.pyplot as plt
import numpy as np


def show_quad(quad):
    temperature = np.zeros((quad.Nx, quad.Ny), dtype=np.float)
    for y in range(quad.Ny):
        for x in range(quad.Nx):
            temperature[y, x] = quad.nodes[x + y * quad.Nx].T

    fig, ax = plt.subplots()
    ax.imshow(temperature, cmap='rainbow')
    ax.invert_yaxis()
    plt.show()