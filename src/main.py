import matplotlib.pyplot as plt
from donnees import charger_donnees, clean_donnees, graphique_prix, graphique_surface_prix

# ======================
# Cleanning des données
df = charger_donnees()
print(f"Avant nettoyage : {len(df)} maisons.")

df = clean_donnees(df)
print(f"Après nettoyage : {len(df)} maisons.")

# =====================================================================================================================
# Création des graphiques qui compare les prix des maisons et qui compare les prix des maisons par rapport a la surface
graphique_prix(df)
graphique_surface_prix(df)
plt.show()
