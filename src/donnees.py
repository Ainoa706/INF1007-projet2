import pandas as pd
import matplotlib.pyplot as plt

"""cleaning des données"""
def clean_donnees(df):
    # prix nuls et négatifs
    df = df[df["price"] > 0]            # renvoie true sur les ligne valide et ne garde que les true
    # année de rénovation avant construction
    renov_invalide = (df["yr_renovated"] > 0) & (df["yr_renovated"] < df["yr_built"])       # renvoie true sur les mauvaises lignes
    df = df[~renov_invalide]            # prends l'inverse
    return df.reset_index(drop=True)        # recréé un index cohérent

"""Partie graphique de l'étape 1"""
def charger_donnees():
    return pd.read_csv("donnees/USA_price.csv")

def graphique_prix(df):
    df_valide = df[df["price"] > 0]
    plt.figure(figsize=(8, 5))
    plt.hist(df_valide["price"], bins=50)
    plt.title("Distribution des prix des maisons")
    plt.xlabel("Prix en $")
    plt.ylabel("Nombre de maisons")
    plt.savefig("graphique_prix.png")

def graphique_surface_prix(df):
    df_valide = df[df["price"] > 0]
    plt.figure(figsize=(8, 5))
    plt.scatter(df_valide["sqft_living"], df_valide["price"], alpha=0.3)
    plt.title("Prix selon la surface habitable")
    plt.xlabel("Surface habitable (sqft)")
    plt.ylabel("Prix ($)")
    plt.savefig("graphique_surface_prix.png")
