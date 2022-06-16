import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from numpy import arange, zeros, array
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from Vectors import *
import Settings as st
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective
import matplotlib.pyplot as plt


def solidQuad(p1, p2, color):
    glBegin(GL_QUADS)
    glColor3f(*color.data)
    glVertex2f(p1.x, p1.y)
    glVertex2f(p1.x, p2.y)
    glVertex2f(p2.x, p2.y)
    glVertex2f(p2.x, p1.y)
    glEnd()


def quad_and_cm(T, Nx, Ny):
    quads = []
    w = 2 / Nx
    h = 2 / Ny
    for y in arange(-1, 1, 2 / Ny):
        for x in arange(-1, 1, 2 / Nx):
            quads.append((Vec2D(x, y), Vec2D(x + w, y + h), Vec3D(0, 0, 0)))

    if np.isnan(T.min()):
        color_map = (.3, .3, .3)
        print("Couleur uniforme dans le quad")
    else:
        norm = Normalize(vmin=T.min(), vmax=T.max())
        cmap = cm.rainbow
        color_map = cm.ScalarMappable(norm=norm, cmap=cmap)

    return quads, color_map


def init_GL(resolution=None):
    pygame.init()
    pygame.display.set_caption("Visualisation nodes 2D")
    if not resolution:
        pygame.display.set_mode(st.screen_resolution, DOUBLEBUF | OPENGL)
    else:
        pygame.display.set_mode(resolution, DOUBLEBUF | OPENGL)

    gluPerspective(45, st.screen_width / st.screen_height, 0, 50)


def rgba2rgb(val):
    return val[0], val[1], val[2]


def Change_Colors(quads, T, cm):
    j = 0
    if type(cm) == tuple:
        for quad in quads:
            quad[2].data = np.array(cm)
            j += 1
    else:
        for quad in quads:
            quad[2].data = np.array(rgba2rgb(cm.to_rgba(T[j])))
            j += 1


def Draw_quads(quads):
    for quad in quads:
        solidQuad(*quad)


def animate_quad(quad):
    while True:
        T = zeros(quad.Ntotal, dtype=np.float)
        quad.update()
        i = 0
        for node in quad.nodes:
            T[i] = node.T
            i += 1

        quads, color_map = quad_and_cm(T, quad.Nx, quad.Ny)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        Change_Colors(quads, T, color_map)
        Draw_quads(quads)

        pygame.display.flip()


def show_quad_GL(quad, resolution=None):
    init_GL(resolution)

    T = zeros(quad.Ntotal, dtype=np.float)
    i = 0
    RUN = True
    for node in quad.nodes:
        T[i] = node.T
        i += 1

    quads_GL, color_map = quad_and_cm(T, quad.Nx, quad.Ny)

    Change_Colors(quads_GL, T, color_map)
    Draw_quads(quads_GL)
    pygame.display.flip()
    while RUN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                RUN = False


def show_quad_plt(quad):
    T = zeros((quad.Nx, quad.Ny), dtype=np.float)
    for y in range(quad.Ny):
        for x in range(quad.Nx):
            T[y, x] = quad.nodes[x + y * quad.Nx].T

    fig, ax = plt.subplots()
    ax.imshow(T, cmap='rainbow')
    ax.invert_yaxis()
    plt.show()