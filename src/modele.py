import pandas as pd                    # Sauvegarder les donnees
import numpy as np                     # Effetuer les calculs
import matplotlib.pyplot as plt        # Creer les graphiques
import joblib as jb                    # Sauvegarder le modele
import json as js                      # Sauvegarder les metadonnees

from sklearn.model_selection import train_test_split       # Separer les donnees en 2 categories : entrainement et test
from sklearn.linear_model import LinearRegression          # Creer un modele de regression lineaire 
from sklearn.preprocessing import OneHotEncoder            # Transformer les colonnes categorielles en "nombres", ex: "city"
from sklearn.compose import ColumnTransformer              # Choisir quels modifs appliquer a certaines colonne de notre tableau
from sklearn.pipeline import Pipeline                      # Regrouper plusieurs etapes en un seul processus

from src.donnees import colonnes_utiles                    # colonnes a utiliser pour la regression lineaire 





# =================================
# 8. DÉFINIR LE PROBLÈME
# =================================

cible = "price"
caracteristiques = [colonne for colonne in colonnes_utiles if colonne != cible]
caracteristiques_categorielles = [
    "waterfront",
    "view",
    "condition",
    "city",
]
caracteristiques_numeriques = [colonne for colonne in caracteristiques if colonne not in caracteristiques_categorielles]


def definir_probleme(df):
    x = df[caracteristiques].copy()   # Creer une copie des donnees des caracteristiques (variable x) pour eviter de modifier accidentellement notre ensemble de donnees (df)
    y = df[cible].copy()              # # Creer une copie des donnees des prix (variable y) pour eviter de modifier accidentellement notre ensemble de donnees (df)
    return x, y





# =================================
# 9. SÉPARER LES DONNÉES
# =================================

def separer_donnees(x, y):
    x_train, x_test, y_train, y_test = train_test_split(
        x,                  # Caracteristiques des maisons
        y,                  # Variale cible : prix des maisons 
        test_size=0.2,      # Conserver 20% de nos donnees pour les tests et 80% de nos donnees pour l'entrainement de notre modele
        random_state=42     # Fixe une graine aleatoire pour obtenir des resultats reproductibles
    )
    return x_train, x_test, y_train, y_test





# =================================
# 10. CALCULER LE RMSE
# =================================

def calculer_rmse(y_reel, y_predit):               # Calculer le rmse entre le prix reel vs le prix predit d'une maison
    reels = np.asarray(y_reel, dtype=float)        # Convertir les donnees reels en tableau numpy
    predits = np.asarray(y_predit, dtype=float)    # Convertir les donnees predits en tableay numpy

    if reels.size == 0:                                       # Si la liste des prix reels est vide
        raise ValueError("Aucune observation à évaluer")      # Python affiche une erreur
    if reels.shape != predits.shape:                          # On verifie si on possede autant de prix reels que de prix predits
        raise ValueError("Dimensions incompatibles")          # Sinon, Python affiche une erreur

    erreurs_au_carre = (reels - predits)**2                   # Selon la formule, calculer le carre de chaque erreur (reel - predit)^2
    rmse = np.sqrt(np.mean(erreurs_au_carre))                 # Calcul la racime carre de la moyenne des erreurs au carre (formule rmse)
    return float(rmse)





# =================================
# 11. MODÈLE DE RÉFÉRENCE
# =================================

def modele_de_reference(y_train, y_test):                           # Nous sert de point de compraison : est-ce que notre regression lineaire predit mieux les prix que le fait de donner le prix moyen a toutes les maisons 
    prix_moyen_entrainement = y_train.mean()                        # Calculer le prix moyen pour les donnees d'entrainement (80%)
    predictions = np.full(len(y_test), prix_moyen_entrainement)     # Predire le prix moyen pour toutes les maisons du test
    rmse = calculer_rmse(y_test, predictions)                       # Calculer le rmse
    return rmse 





# =======================================
# 12. ENTRAÎNER LA RÉGRESSION LINÉAIRE
# =======================================

def entrainer_modele(x_train, y_train):
    preparer_donnees = ColumnTransformer(                      # ColumnTransformer : choisit les colonnes à transformer
        transformers = [
            (
                "categories",                                  # "categories" : nom qu'on donne à cette transformation
                OneHotEncoder(handle_unknown="ignore"),        # OneHotEncoder() : transforme les catégories en colonnes numériques de 0 et de 1 ; handle_unknown="ignore" : évite une erreur si une nouvelle catégorie apparaît lors des prédictions
                caracteristiques_categorielles                 # liste des colonnes à transformer (city, view, condition, waterfront)
            )
        ],
        remainder="passthrough"                                # remainder="passthrough" : les autres colonnes de x_train sont conservées telles quelles
    )

    modele_regression_lineaire = Pipeline([("preparer les donnees", preparer_donnees), ("regression lineaire", LinearRegression())])  # Creer la regression lineaire
    modele_regression_lineaire.fit(x_train, y_train)           # Entrainer le modele sur les donnees d'entrainement (80%)
    return modele_regression_lineaire                          # Modele entrainer





# ===============================================
# 13. ÉVALUER LE MODÈLE DE RÉGRESSION LINÉAIRE
# ===============================================

def evaluer_modele(modele, x_test, y_test):        # Evaluer la precision de notre modele sur le prix de maisons auxquelles il n'a pas ete exposees (pour voir si le modele marche bien)
    predictions = modele.predict(x_test)           # Predire le prix des maisons contenues dans l'ensemble de donnees de test (20%)
    rmse = calculer_rmse(y_test, predictions)      # Calculer le RMSE
    return predictions, rmse





# ====================================================================
# 14. GRAPHIQUE - PRIX DE MAISONS PRÉDITS VS RÉELS (NUAGE DE POINTS)
# ====================================================================

def graphique_predictions_reels(y_test, predictions, chemin):
    plt.figure(figsize=(12, 7))

    plt.figure(figsize=(12, 7))
    plt.scatter(
        y_test,
        predictions,
        color="blue",
        alpha=0.4,
        label="Prix prédits des maisons"
    )
    plt.plot(
        sorted(y_test),
        sorted(y_test),
        color="red",
        label="Prédiction parfaite"
    )
    plt.xlabel("Prix réel ($)")
    plt.ylabel("Prix prédit ($)")
    plt.title("Prix prédits vs prix réels des maisons")
    plt.legend()
    plt.tight_layout()
    plt.savefig(chemin, bbox_inches="tight")
    plt.close()





# ==================================================================
# 15. Sauvegarder le modele (joblib et fichier json/métadonnées)
# ==================================================================

def sauvegarder_modele(modele, x_train, rmse, chemin_modele, chemin_json):
    jb.dump(modele, chemin_modele)

    intervalles = {}
    for colonne in caracteristiques_numeriques:
        intervalles[colonne] = {
            "min" : float(x_train[colonne].min()),
            "max" : float(x_train[colonne].max())
        }

        encodeur = modele.named_steps["preparer les donnees"].named_transformers_["categories"]

        categories = {}
        for i, colonne in enumerate(caracteristiques_categorielles):
            valeurs = encodeur.categories_[i].tolist()
            categories[colonne] = [valeur.item() if isinstance(valeur, np.generic) else valeur for valeur in valeurs]

        metadata = {
            "cible": "price",
            "caracteristiques": caracteristiques_numeriques + caracteristiques_categorielles,
            "variables_numeriques": caracteristiques_numeriques,
            "variables_categorielles": categories,
            "metrique": "RMSE",
            "rmse": float(rmse)
        }

        with open(chemin_json, "w", encoding="utf-8") as f:
            js.dump(metadata, f, indent=4, ensure_ascii=False)
