import matplotlib.pyplot as plt
from src.donnees import (
    charger_donnees, 
    nettoyer_donnees, 
    graphique_prix, 
    graphique_surface_prix
)

# ======================
# Cleanning des données
df = charger_donnees()
print(f"Avant nettoyage : {len(df)} maisons.")

df = nettoyer_donnees(df)
print(f"Après nettoyage : {len(df)} maisons.")

plus_cheres = df["price"].nlargest(2).index
plus_grandes = df["sqft_living"].nlargest(2).index
df = df.drop(plus_cheres.union(plus_grandes)).reset_index(drop=True)

# =====================================================================================================================
# Création des graphiques qui compare les prix des maisons et qui compare les prix des maisons par rapport a la surface
graphique_prix(df)
graphique_surface_prix(df)
plt.show()
