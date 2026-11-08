import pandas as pd
import matplotlib.pyplot as plt

def charger_donnees():
    return pd.read_csv("donnees/USA_price.csv")


"""cleaning des données"""
def clean_donnees(df):
    # prix nuls et négatifs
    df = df[df["price"] > 0]        # renvoie true sur les ligne valide et ne garde que les true
    # année de rénovation avant construction
    renov_invalide = (df["yr_renovated"] > 0) & (df["yr_renovated"] < df["yr_built"])       # renvoie true sur les mauvaises lignes
    df = df[~renov_invalide]        # prends l'inverse
    return df.reset_index(drop=True)        # recréé un index cohérent


"""Partie graphique de l'étape 1"""
def graphique_prix(df):
    plt.figure(figsize=(8, 5))
    plt.hist(df["price"], bins=50)
    plt.title("Distribution des prix des maisons")
    plt.xlabel("Prix en $")
    plt.ylabel("Nombre de maisons")
    plt.savefig("graphiques/graphique_prix.png")

def graphique_surface_prix(df):
    plt.figure(figsize=(8, 5))
    plt.scatter(df["sqft_living"], df["price"], alpha=0.3)
    plt.title("Prix selon la surface habitable")
    plt.xlabel("Surface habitable (sqft)")
    plt.ylabel("Prix ($)")
    plt.savefig("graphiques/graphique_surface_prix.png")
