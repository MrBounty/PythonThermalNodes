from Thermal_Class import *
from My_Graphs_Functions import show_quad

quad_1 = {
        'position': (0., 0.),
        'size': (100., 100.),
        'Nx': 100,
        'Ny': 100,
        'lbda': 35,
        'rho': 7850,
        'Cp': 476,
        'T_init': 0,
        'masse': 1.,
        'boundary': [0, 0, 0, 0],
        'indice': 0
    }

work = Thermal_Workbench()

work.Add_Rect(quad_1)

work.Create_Nodes()

work.Add_Fixed_Temperature_Edge(surface_indice=0, edge_indice=0, Temperature=0)
work.Add_Fixed_Temperature_Edge(surface_indice=0, edge_indice=1, Temperature=100)
work.Add_Fixed_Temperature_Edge(surface_indice=0, edge_indice=2, Temperature=0)
work.Add_Fixed_Temperature_Edge(surface_indice=0, edge_indice=3, Temperature=0)

work.Calcul_Temps(100, 0.01)

print(type(work.surfaces))

show_quad(work.surfaces[0])