
import pytest
import pandas as pd
from pathlib import Path

from src.donnees import (
    charger_donnees,
    nettoyer_donnees
)





# ============================================================
# PRÉPARER LES DONNÉES POUR LES TESTS
# ============================================================

@pytest.fixture(scope="module")  # @pytest.fixture permet de préparer les données une seule fois et de les réutiliser dans plusieurs tests
def donnees_test():
    chemin = Path(__file__).resolve().parents[1] / "donnees" / "USA_price.csv"      # Trouver le chemin du fichier CSV
    df = charger_donnees(chemin)      # Charger les données originales
    df_clean = nettoyer_donnees(df)   # Nettoyer les données
    return df, df_clean





# ============================================================
# TEST 1 - CAS USUEL (CHARGEMENT DES DONNÉES)
# ============================================================

def test_chargement_donnees(donnees_test):
    df, df_clean = donnees_test              # Récupérer les données originales et nettoyées
    assert isinstance(df, pd.DataFrame)      # Vérifier que les données sont dans un DataFrame
    assert len(df) > 0                       # Vérifier que le fichier n'est pas vide





# ============================================================
# TEST 2 - CAS USUEL (SUPPRESSION DES COLONNES INUTILES)
# ============================================================

def test_suppression_colonnes(donnees_test):
    df, df_clean = donnees_test            # Récupérer les données originales et nettoyées
    colonnes_supprimees = [                # Colonnes qui doivent être supprimées pendant le nettoyage
        "statezip",
        "street",
        "sqft_basement",
        "sqft_above",
        "date",
        "country"
    ]

    for colonne in colonnes_supprimees:   # Vérifier que toutes les colonnes inutiles ont été supprimées
        assert colonne not in df_clean.columns





# ============================================================
# TEST 3 - CAS LIMITE (CONSERVATION DES DONNÉES)
# ============================================================

def test_conservation_donnees(donnees_test):
    df, df_clean = donnees_test       # Récupérer les données originales et nettoyées
    assert len(df_clean) > 0          # Vérifier qu'il reste des maisons après le nettoyage
    assert len(df_clean) <= len(df)   # Vérifier que le nettoyage conserve ou supprime des observations seulement (il n'ajoute rien)





# ============================================================
# TEST 4 - CAS D'ERREUR (FICHIER INEXISTANT)
# ============================================================

def test_fichier_inexistant():
    chemin = "fichier_inexistant.csv"    # Définir le chemin d'un fichier CSV qui n'existe pas

    with pytest.raises(FileNotFoundError):    # Vérifier que la fonction déclenche une FileNotFoundError quand le fichier demandé est introuvable
        charger_donnees(chemin)