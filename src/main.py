import matplotlib.pyplot as plt
from donnees import charger_donnees, graphique_prix, graphique_surface_prix

df = charger_donnees()
graphique_prix(df)
graphique_surface_prix(df)
plt.show()


# à changer car le graphique n'apparait pas là où je veux
