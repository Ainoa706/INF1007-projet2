import os
import pandas as pd
import matplotlib.pyplot as plt
from src.exceptions import DonneeInvalide

# =================================================
# 1. NOS COLONNES 
# =================================================

# TOUTES NOS COLONNES DU JEU DE DONNEES 
ensemble_colonnes = [
    "date",
    "price",
    "bedrooms",
    "bathrooms",
    "sqft_living",
    "sqft_lot",
    "floors",
    "waterfront",
    "view",
    "condition",
    "sqft_above",
    "sqft_basement",
    "yr_built",
    "yr_renovated",
    "street",
    "city",
    "statezip",
    "country"
]

# TOUTES NOS COLONNES DU JEU DE DONNEES QUI SONT NUMERIQUES
colonnes_numeriques = [
    "price",           # Prix
    "bedrooms",        # Chambres
    "bathrooms",       # Salles de bain
    "sqft_living",     # Superficie habitable
    "sqft_lot",        # Superficie du terrain
    "floors",          # Nombre d'étages
    "waterfront",      # Présence d'un plan d'eau
    "view",            # Vue
    "condition",       # Condition de la maison
    "sqft_above",      # Superficie (pas sous-sol)
    "sqft_basement",   # Superficie du sous-sol
    "yr_built",        # Année de construction
    "yr_renovated"     # Année de rénovation
]

# TOUTES NOS COLONNES DU JEU DE DONNEES QUE L'ON VA SUPPRIMER
colonnes_a_supprimer = [
    "statezip",
    "street",
    "sqft_basement",
    "sqft_above",
    "date",
    "country"
]

# TOUTES NOS COLONNES DU JEU DE DONNEES QUE L'ON VA UTILISER POUR LA REGRESSION LINEAIRE
colonnes_utiles = [
    "price",
    "bedrooms",
    "bathrooms",
    "sqft_living",
    "sqft_lot",
    "floors",
    "waterfront",
    "view",
    "condition",
    "yr_built",
    "yr_renovated",
    "city"
]





# =================================================
# 2. CHARGER NOS DONNEES (OS)
# =================================================

def charger_donnees(chemin):
    if not os.path.exists(chemin):                                #verifie d'abord que le fichier existe
        raise FileNotFoundError("Fichier csv introuvable")        #si fichier existe pas, raise erreur

    with open(chemin, "r", encoding="utf-8") as f:                #ouvrir le fichier
        df = pd.read_csv(f)                                       #lire le fichier et stock les donnees du fichier dans la varuable df
    return df              





# ====================================================
# 3. EXPLORER LES DONNEES/COLONNES DU JEU DE DONNEES
# ====================================================

def explorer_donnees(df):

    """Vérifier le nombre de lignes et de colonnes"""
    print ("Dimension du jeu de données : ", df.shape)


    """Afficher toute les colonnes"""
    print("Nom des colonnes :")
    print (df.columns)


    """Type de données"""
    print("type des donnees")
    print(df.dtypes)





# =================================================
# 4. VERIFIER LES VALEURS MANQUANTES
# =================================================

    """Compter les valeurs manquantes dans toute les colonnes"""
    for colonne in df.columns:
        manquant = df[colonne].isna().sum()                 #isna ->retourne true si valeure manquante et .sum compte les True
        print ("valeurs manquantes de chaque colonne")
        print(f"{colonne} : {manquant}")





# ==========================================================================
# 5. VERIFIER LES VALEURS ABERRANTES (TRY/EXCEPT)/(EXCEPTION PERSONNALISEE)
# ==========================================================================

def verifier_donnees(df):
    bilan = {}

    try:

        for colonne in colonnes_numeriques:
            if colonne == "price":
                invalides = (df[colonne] <= 0).sum()                                                                # .sum() c'est pour calculer le nombre total de valeurs invalides dans la colonne
            elif colonne in ["bedrooms", "bathrooms"]:
                invalides = (df[colonne] < 0).sum()
            elif colonne in ["sqft_living", "sqft_lot", "sqft_above"]:
                invalides = (df[colonne] <= 0).sum()
            elif colonne == "sqft_basement":
                invalides = (df[colonne] < 0).sum()
            elif colonne == "floors":
                invalides = (df[colonne] <= 0).sum()
            elif colonne == "yr_built":
                invalides = (df[colonne] == 0).sum()
            elif colonne == "yr_renovated":
                invalides = ((df[colonne] < 0) | ((df[colonne] != 0) & (df[colonne] < df["yr_built"]))).sum()      # & veut dire ET , | veut dire OU
            elif colonne == "condition":
                invalides = (~df[colonne].isin([0, 1, 2, 3, 4, 5])).sum()                                          # .sum() compte le nombre de True, donc en inversant les True/False avec ~, nous pouvons compter le nombre total de valeurs autres que 0,1,2,3,4 (True)
            elif colonne == "waterfront":
                invalides = (~df[colonne].isin([0, 1])).sum()  
            elif colonne == "view":
                invalides = (~df[colonne].isin([0, 1, 2, 3, 4])).sum() 

            bilan[colonne] = int(invalides)
            print(colonne, ":", invalides, "valeurs invalides")

        superficies_invalides = (df["sqft_living"]) != (df["sqft_above"] + df["sqft_basement"])                   # realistiquement, sqft_living = sqft_above + sqft_basement donc si la logique tiens, nous pourrions seulememt prendre en compte sqft_living dans notre regression lineaire
        bilan["superficies_non_coherentes"] = int(superficies_invalides.sum())
        print("Superficies incoherentes :", bilan["superficies_non_coherentes"])

    except (ValueError) as e:
        raise DonneeInvalide("Erreur rencontree lors de la verification des donnees") from e

    return bilan





# =================================
# 6. NETTOYER LES DONNEES (CLEAN)
# =================================

def nettoyer_donnees(df):
    df_clean = df.copy()

    df_clean = df_clean.dropna(subset=colonnes_utiles + ["sqft_above", "sqft_basement"]).copy()                              # .dropna() sert a supprimer les valeurs manquantes et subset=colonnes_utiles sert a preciser les colonnes dans lesquelles on veut verifier les valeurs manquantes

    df_clean = df_clean[df_clean["price"] > 0].copy()   
    df_clean = df_clean[(df_clean["bedrooms"] >= 0) & (df_clean["bathrooms"] >= 0)].copy()  
    df_clean = df_clean[(df_clean["sqft_living"] > 0) & (df_clean["sqft_lot"] > 0) & (df_clean["sqft_above"] > 0) & (df_clean["sqft_basement"] >= 0)].copy()
    df_clean = df_clean[df_clean["sqft_living"] == df_clean["sqft_above"] + df_clean["sqft_basement"]].copy()                # on garde les sqft_living qui suivent cette regle : sqft_living = sqft_above + sqft_basement (logique dans la vie reelle)                                                              # on garde les maisons dont le prix > 0
    df_clean = df_clean[(df_clean["yr_renovated"] >= df_clean["yr_built"]) | (df_clean["yr_renovated"] == 0)].copy()         # on garde les annees de renovation egal a 0 ou > annee de construction
    df_clean = df_clean[df_clean["floors"] > 0].copy()                                                                       # on garde un nombre positif d'etages
    df_clean = df_clean[df_clean["condition"].isin([1, 2, 3, 4, 5])].copy()                                                  # on garde la meme echelle (1, 2, 3, 4, 5) pour condition
    df_clean = df_clean[df_clean["view"].isin([0, 1, 2, 3, 4])].copy()                                                       # on garde la meme echelle (0, 1, 2, 3, 4) pour view
    df_clean = df_clean[df_clean["waterfront"].isin([0, 1])].copy()                                                          # on garde la meme echelle (0, 1) pour waterfront

    df_clean = df_clean[colonnes_utiles].copy()
    return df_clean.reset_index(drop=True)





# =================================
# 7. GRAPHIQUES D'EXPLOITATION
# =================================

"""Partie graphique de l'étape 1"""
def graphique_prix(df, chemin):
    plt.figure(figsize=(8, 5))
    plt.hist(df["price"], bins=50)
    plt.title("Distribution des prix des maisons")
    plt.xlabel("Prix en $")
    plt.ylabel("Nombre de maisons")
    plt.savefig("graphiques/graphique_prix.png")

def graphique_surface_prix(df, chemin):
    plt.figure(figsize=(8, 5))
    plt.scatter(df["sqft_living"], df["price"], alpha=0.3)
    plt.title("Prix selon la surface habitable")
    plt.xlabel("Surface habitable (sqft)")
    plt.ylabel("Prix ($)")
    plt.savefig("graphiques/graphique_surface_prix.png")
    plt.close()
