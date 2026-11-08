import matplotlib.pyplot as plt
from donnees import charger_donnees, clean_donnees, graphique_prix, graphique_surface_prix

# ======================
# Cleanning des données
df = charger_donnees()
print (f"Avant nettoyage : {len(df)} maisons.")

df = clean_donnees()
print(f"Après nettoyag : {len(df)} maisons.")
# voir que faire pour les prix annormalement élevé mardi

# =====================================================================================================================
# Création des graphiques qui compare les prix des maisons et qui compare les prix des maisons par rapport a la surface
df = charger_donnees()
graphique_prix(df)
graphique_surface_prix(df)
plt.show()
# à changer car le graphique n'apparait pas là où je veux
