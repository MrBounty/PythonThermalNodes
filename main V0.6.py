from Thermal_Class import *
from My_Graphs_Functions import show_quad

quad_1 = { #Surface data
        'position': (0., 0.),   #In m
        'size': (100., 100.),   #In m
        'Nx': 15,               #Nb of nodes in the X axs
        'Ny': 15,               #Nb of nodes in the Y axs
        'lbda': 35,             #Thermal conductivity
        'rho': 7850,            #Volumic mass
        'Cp': 476,              #Heat capacity
        'T_init': 0,            #Temperature initial
        'masse': 1.,            #Weight
        'boundary': [0, 0, 0, 0],
        'indice': 0
    }

work = Thermal_Workbench() #Creation of the workbench, this is the main object

work.Add_Rect(quad_1) #Add a surface

work.Create_Nodes() #Make nodes

#Add boundary condition
work.Add_Fixed_Temperature_Edge(surface_indice=0, edge_indice=0, Temperature=0) 
work.Add_Fixed_Temperature_Edge(surface_indice=0, edge_indice=1, Temperature=100)
work.Add_Fixed_Temperature_Edge(surface_indice=0, edge_indice=2, Temperature=0)
work.Add_Fixed_Temperature_Edge(surface_indice=0, edge_indice=3, Temperature=0)

work.Calcul_Temps(100, 0.01) #Run simulation

show_quad(work.surfaces[0]) #Show result
