import pytest
import numpy as np
from pathlib import Path

from src.donnees import (
    charger_donnees, 
    nettoyer_donnees
)
from src.modele import (
    calculer_rmse,
    definir_probleme,
    separer_donnees,
    entrainer_modele,
    evaluer_modele
)


# ============================================================
# PRÉPARER LES DONNÉES ET LE MODÈLE POUR LES TESTS
# ============================================================

@pytest.fixture(scope="module")        # @pytest.fixture permet de préparer les données une seule fois et de les réutiliser dans plusieurs tests

def donnees_test():
    chemin = Path(__file__).resolve().parents[1] / "donnees" / "USA_price.csv"      # Trouver le chemin du fichier CSV contenant les maisons

    df = charger_donnees(chemin) # Charger les données des maisons à partir du fichier CSV
    df = nettoyer_donnees(df)    # Données des maisons nettoyées 

    x, y = definir_probleme(df)  # x = caracteristiques des maisons, y = prix des maisons 
    x_train, x_test, y_train, y_test = separer_donnees(x, y)  # train : données utilisées pour entrainer le modele, test : données utilisées pour évaluer le modèle

    modele = entrainer_modele(x_train, y_train)       # Entraîner la régression linéaire à partir des données d'entraînement
    return modele, x_train, x_test, y_train, y_test   # Retourner le modèle et les données pour les réutiliser dans les tests


# ============================================================
# TEST 1 - CAS USUEL (VÉRIFIER LE CALCUL DE LA RMSE)
# ============================================================

def test_rmse_cas_usuel():
    reels = [100000, 200000, 300000]       # Prix réels de trois maisons
    predits = [110000, 190000, 300000]     # Prix prédits pour ces mêmes maisons

    resultat = calculer_rmse(reels, predits)        # Calculer la RMSE avec notre fonction
    assert resultat == pytest.approx(8164.9658, abs=0.01)    # Vérifier le résultat calculé manuellement (pytest.approx permet de comparer des nombres décimaux)





# ============================================================
# TEST 2 - CAS LIMITE (PRÉDICTIONS PARFAITES - RMSE)
# ============================================================

def test_rmse_predictions_parfaites():
    reels = [100000, 200000]
    predits = [100000, 200000]

    resultat = calculer_rmse(reels, predits)
    assert resultat == pytest.approx(0)   # La RMSE doit être nulle si les prix sont identiques





# ============================================================
# TEST 3 - CAS D'ERREUR (DIMENSIONS INCOMPATIBLES)
# ============================================================

def test_rmse_dimensions_invalides():
    reels = [100000, 200000]
    predits = [110000]

    with pytest.raises(ValueError):       # pytest.raises(ValueError) vérifie que la fonction déclenche une erreur lorsque les listes n'ont pas le même nombre d'éléments
        calculer_rmse(reels, predits)     # Vérifier qu'une ValueError est levée (test reussie)





# ============================================================
# TEST 4 - CAS D'ERREUR (LISTES VIDES)
# ============================================================

def test_rmse_liste_vide():
    reels = []
    predits = []

    with pytest.raises(ValueError):
        calculer_rmse(reels, predits)   # Impossible de calculer la RMSE sans observation (fonction déclenche une ValueError)





# ============================================================
# TEST 5 - CAS USUEL (SÉPARATION DES DONNÉES)
# ============================================================

def test_separation_donnees(donnees_test):
    modele, x_train, x_test, y_train, y_test = donnees_test
    total = len(x_train) + len(x_test)   # Calculer le nombre total de maisons (ensemble d'entraînement + ensemble de test)

    assert len(x_test) == pytest.approx(total * 0.2, abs=1)  # Vérifier que 20 % des données servent aux tests
    assert len(x_train) == len(y_train)   # Vérifier que chaque maison possède un prix correspondant
    assert len(x_test) == len(y_test)     # Vérifier la même chose pour l'ensemble de test
    assert set(x_train.index).isdisjoint(set(x_test.index))  # Vérifier qu'une maison n'est pas dans les deux ensembles (# isdisjoint vérifie qu'aucun index n'est présent dans les deux)





# ============================================================
# TEST 6 - CAS USUEL (PRÉDICTION D'UNE MAISON)
# ============================================================

def test_prediction_une_maison(donnees_test):
    modele, x_train, x_test, y_train, y_test = donnees_test
    maison = x_test.head(1)    # Sélectionner la première maison de l'ensemble de test
    prediction = modele.predict(maison)    # Prédire le prix de cette maison
    assert len(prediction) == 1    # Vérifier qu'un seul prix est retourné
    assert np.isfinite(prediction[0])   # Vérifier que le prix prédit est un nombre valide





