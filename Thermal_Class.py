import Settings as st
from time import time
from tqdm import tqdm
import numpy as np


# Ajoute les arguments dans la liste pour etre utilisé par Create_Nodes
def add_node_arg(arg_list, x, y, lbda, rho, Cp, T_init, masse, neibs_indice,
                 indice_surface=None, indice_workbench=None, surface=None, parent=None):
    arg_list.append({
        "x": x,
        "y": y,
        "lbda": lbda,
        "rho": rho,
        "Cp": Cp,
        "T_init": T_init,
        "masse": masse,
        "indice_surface": indice_surface,
        "indice_workbench": indice_workbench,
        "neibs_indice": neibs_indice,
        "parent": parent,
        "surface": surface
    })


# La surface sur laquel on vient dessiner des formes
class Thermal_Workbench:
    def __init__(self):
        self.t = 0
        self.dt = 0
        self.nodes_arg = []
        self.nodes = []
        self.surfaces = []

    def update(self):
        # Update les temperature des surface du workbench
        for surf in self.surfaces:
            surf.update()

    def Create_Nodes(self):
        # Creer les noeuds a partir de la liste de dict qui contient les arguments
        for surf in self.surfaces:
            surf.Create_Nodes()

    def Calcul_Temps(self, t_final, dt):
        # Calcul les temperature jusqu'a un temps pour un certain pas de temps
        self.dt = dt

        for n in self.nodes:
            n.T_history = np.zeros((int(t_final / self.dt) - int(self.t / self.dt), 2))

        t1 = time()
        for t_i in tqdm(range(int(self.t / self.dt), int(t_final / self.dt))):
            self.update()
            self.t += dt
        print("Temps de calcul:", time() - t1, "[s]")

    def Add_Rect(self, arg):
        Thermal_Quad(self, **arg)

    def Add_Fixed_Temperature_Edge(self, surface_indice, edge_indice, Temperature):
        self.surfaces[surface_indice].boundary_condition[edge_indice] = 1
        arg = self.surfaces[surface_indice].edgeID4boundary(edge_indice)
        for i in range(*arg):
            self.surfaces[surface_indice].nodes[i].T_fixe = True
            self.surfaces[surface_indice].nodes[i].T_fixe_list.append(Temperature)
            self.surfaces[surface_indice].nodes[i].Calcul_T_fixe()

    def Add_Fixed_Temperature_Surface(self, surface_indice, Temperature):
        self.surfaces[surface_indice].boundary_condition = [1 for x in range(len(self.surfaces[surface_indice].boundary_condition))]
        for n in self.surfaces[surface_indice].nodes:
            n.T_fixe = True
            n.T_fixe_list.append(Temperature)
            n.Calcul_T_fixe()


# Un rectangle composé de noeud 2D
class Thermal_Quad:
    def __init__(self, workbench, **kwargs):
        self.x = kwargs.get('position')[0]          # Position en x [m]
        self.y = kwargs.get('position')[1]          # Position en y [m]
        self.size = kwargs.get('size')              # Taille (x, y) [m]
        self.Nx = kwargs.get('Nx')                  # Nombre de point suivant x
        self.Ny = kwargs.get('Ny')                  # Nombre de point suivant y
        self.lbda = kwargs.get('lbda')              # Conductivité thermique [W m−1 K−1]
        self.rho = kwargs.get('rho')                # Masse volumique [kg m-3]
        self.Cp = kwargs.get('Cp')                  # Capacite thermique [J K-1 kg-1]
        self.masse = kwargs.get('masse')            # Masse [kg]
        self.T_moyenne = kwargs.get('T_init')       # Temperature initiale [K]
        self.indice_workbench = kwargs.get('indice')  # Indice de la surface
        self.workbench = workbench                  # Le workbench lié au quad
        self.workbench.surfaces.append(self)
        if kwargs.get('boundary') == None:
            self.boundary_condition = [0, 0, 0, 0]  # Le type de condition limite
        else:
            self.boundary_condition = kwargs.get('boundary')

        self.Ntotal = self.Nx * self.Ny             # Nombre total de noeuds
        self.nodes_arg = []                         # Liste des arguments des noeuds de la surface
        self.nodes = []                             # Liste des noeuds de la surface

        self.Nodes_init()

        self.workbench.nodes_arg += self.nodes_arg

    def update(self):
        # Update les temperature des noeuds du quad
        self.calcul()
        for node in self.nodes:
            node.update()

    def calcul(self):
        # Calcul les propriete du quad qui evolu
        T_sum = 0
        for node in self.nodes:
            T_sum += node.T
        self.T_moyenne = T_sum / len(self.nodes)

    def Nodes_init(self):
        # Initialise les nodes
        dx = self.size[0] / self.Nx / 2
        dy = self.size[1] / self.Ny / 2
        id_general = len(self.workbench.nodes)
        id_local = len(self.nodes_arg)
        m = self.masse / (self.Nx * self.Ny)
        for y in range(self.Ny):
            for x in range(self.Nx):
                add_node_arg(self.nodes_arg,
                             x=dx + self.x + (x / (self.Nx - 1)) * self.size[0],
                             y=dy + self.y + (y / (self.Ny - 1)) * self.size[1],
                             lbda=self.lbda, rho=self.rho, Cp=self.Cp, T_init=self.T_moyenne, masse=m,
                             neibs_indice=self.find_id_neib(id_general, id_local),
                             surface=self,
                             indice_surface=len(self.nodes_arg),
                             indice_workbench=len(self.workbench.nodes_arg),
                             parent=self)
                id_general += 1

    def Create_Nodes(self):
        # Creer les noeuds a partir de la liste de dict qui contient les arguments
        for arg in self.nodes_arg:
            self.nodes.append(Thermal_Node(**arg))
        # Met a jour les voisins des noeuds
        for node in self.nodes:
            for neib in node.neibs_indice:
                node.New_Neib(self.nodes[neib])

        self.workbench.nodes += self.nodes  # Ajoute le noeud dans la liste general de noeuds

    def find_id_neib(self, node_id, i):
        # Trouve les id_general des voisins d'un noeud qui sont dans le meme quad
        temporary = (1, -1, self.Nx, -self.Nx)
        neibs_i = []
        for k in temporary:
            if k == 1 and node_id % self.Nx == self.Nx - 1:
                pass
            elif k == -1 and node_id % self.Nx == 0:
                pass
            elif -1 < k + node_id < (self.Nx * self.Ny):
                neibs_i.append(k + node_id)
        return neibs_i

    def edgeID4boundary(self, edge_i):
        if edge_i == 0:
            arg = (0, self.Nx, 1)
        elif edge_i == 1:
            arg = (self.Nx - 1, self.Nx * self.Ny, self.Nx)
        elif edge_i == 2:
            arg = (self.Nx * self.Ny - self.Nx, self.Nx * self.Ny, 1)
        elif edge_i == 3:
            arg = (0, self.Nx * self.Ny - self.Nx + 1, self.Nx)
        else:
            print("Erreur, edge_i doit etre entre 0 et 3")
            arg = None
        return arg


# Le noeud thermique, ici en 2D
class Thermal_Node:
    def __init__(self, **kwargs):
        # Propriete physiques
        self.x = kwargs.get('x')                        # Position en x [m]
        self.y = kwargs.get('y')                        # Position en y [m]
        self.lbda = kwargs.get('lbda')                  # Conductivité thermique [W m−1 K−1]
        self.rho = kwargs.get('rho')                    # Masse volumique [kg m-3]
        self.Cp = kwargs.get('Cp')                      # Capacite thermique [J K-1 kg-1]
        self.T = kwargs.get('T_init')                   # Temperature initiale [K]
        self.masse = kwargs.get('masse')                # Masse [kg]
        self.volume = self.masse / self.rho             # Valume [m3]
        self.mCp = self.masse * self.Cp                 # Masse * Capacité thermique [J kg-1]
        self.dE = 0                                     # Difference d'energie entre deux pas de temps [J]
        self.Puiss_ext = 0                              # Puissance exterieur recu [W]

        # Autres
        self.indice_surface = kwargs.get('indice_surface')      # Indice du noeud de la surface
        self.indice_workbench = kwargs.get('indice_workbench')  # Indice du noeud du workbench
        self.surface = kwargs.get('surface')
        self.neibs_indice = kwargs.get('neibs_indice')          # Tuple contenant les indices des voisins
        self.parent = kwargs.get('parent')                      # Si le noeud a un parent

        # A initialiser
        self.T_fixe = False                             # Si la temperature est fixe et donc si il faut la calculer
        self.T_fixe_list = []
        self.T_amb = None                               # Si convection, il faut une T_amb
        self.neibs_node = []
        self.T_last = self.T # T_last est utilise pour calculer T, sinon l'ordre de calcul aurait une importance

        self.T_history = []
        self.nb_update_done = 0

    def update(self):
        # Update la temperature du noeud
        self.T_last = self.T
        if not self.T_fixe:
            self.Calcul_DeltaE_Echange()
            self.dE += self.Puiss_ext * st.dt
            self.Calcul_Temperature()
            self.dE = 0

    def Calcul_DeltaE_Echange(self):
        # Calcul la difference d'energie du noeud genere par les echange eavec les voisins
        for neib in self.neibs_node:
            self.dE += (neib[0].T_last - self.T) * neib[2] * self.surface.workbench.dt

    def Calcul_Temperature(self):
        # Simple
        self.T = self.dE / self.mCp + self.T
        self.T_history[self.nb_update_done, 0] = self.surface.workbench.t
        self.T_history[self.nb_update_done, 1] = self.T_last
        self.nb_update_done += 1

    def New_Neib(self, node):
        # Ajoute un voisin a la liste
        if type(node) is list:
            for n in node:
                dist_carre = (self.x - n.x) ** 2 + (self.y - n.y) ** 2
                self.neibs_node.append((n, dist_carre, (n.lbda + self.lbda) / 2 / (self.rho * dist_carre)))
        else:
            dist_carre = (self.x - node.x) ** 2 + (self.y - node.y) ** 2
            self.neibs_node.append((node, dist_carre, (node.lbda + self.lbda) / 2))

    def Calcul_T_fixe(self):
        tem = sum(self.T_fixe_list) / len(self.T_fixe_list)
        self.T = tem
        self.T_last = tem
