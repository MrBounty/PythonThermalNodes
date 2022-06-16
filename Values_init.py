nodes_arg = [
    {
        "x": 0,
        "y": 0,
        "lbda": 1,
        "rho": 1,
        "Cp": 1,
        "T_init": 0,
        "masse": 1,
        "indice": 0,
        "neibs_indice": (1, 2)
    }
]

quads_arg = [
    {
        'position': (0, 0),
        'size': (4, 4),
        'Nx': 6,
        'Ny': 5,
        'lbda': 1,
        'rho': 1,
        'Cp': 1,
        'T_init': 5,
        'masse': 1,
        'boundary': [0, 1, 2, 3],# 0 est isolation, 1 pour une temperature fixe, 2 pour un flux fixe, 3 pour convection
        'indice': 0
    }
]