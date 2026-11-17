
import os                                          # Construire un chemin pour les fichiers

from src.donnees import(                           # Importer les fonctions et les variables de donnees.py
    ensemble_colonnes,
    colonnes_a_supprimer,
    colonnes_utiles,
    charger_donnees,
    explorer_donnees,
    verifier_donnees,
    nettoyer_donnees,
    graphique_prix,
    graphique_surface_prix
)

from src.modele import(                           # Importer les fonctions de modele.py
    definir_probleme,
    separer_donnees,
    modele_de_reference,
    entrainer_modele, 
    evaluer_modele,
    graphique_predictions_reels,
    sauvegarder_modele,
)

from src.exceptions import DonneeInvalide        # Importer la classe DonneeInvalide que nous avons creer 





def main():
    dossier = os.path.dirname(os.path.dirname(__file__))
    chemin_csv = os.path.join(dossier, "donnees", "USA_price.csv")          # Chemin du fichier csv
    dossier_graphiques = os.path.join(dossier, "graphique")
    dossier_modeles = os.path.join(dossier, "modeles")

    os.makedirs(dossier_graphiques, exist_ok=True)
    os.makedirs(dossier_modeles, exist_ok=True)





# ======================================
# 1. Explorer et nettoyer les donnees 
# ======================================

    df = charger_donnees(chemin_csv)
    explorer_donnees(df)
    bilan = verifier_donnees(df)
    print("Bilan des valeurs aberrantes :")

    df_clean = nettoyer_donnees(df)
    print("Dimensions finales du tableau (donnees nettoyees) :", df_clean.shape)

    print("Nombre total de colonnes (donnees originales du csv) :", len(ensemble_colonnes))
    print("Nombre total de colonnes supprimees (donnees originales du csv) :", len(colonnes_a_supprimer))
    print("Nombre total de colonnes conservees (apres le nettoyage des donnees) :", len(df_clean.columns))
    print("Colonnes conservees (apres nettoyage) comformes aux colonnes utiles? :", df_clean.columns.tolist() == colonnes_utiles)
    print("Nombre total de maisons supprimees (pendant le nettoyage de donnees) :", len(df) - len(df_clean))

    chemin_clean = os.path.join(dossier, "donnees", "USA_price_CLEAN.csv")

    graphique_prix(df_clean, os.path.join(dossier_graphiques, "graphique_prix.png"))
    graphique_surface_prix(df_clean, os.path.join(dossier_graphiques, "graphique_surface_prix.png"))





# ======================================
# 2. Definir le probleme 
# ======================================

    x, y = definir_probleme(df_clean)
    print("Dimensions de la valeur cible (x) :", x.shape)                         # tuple : (lignes, colonnes)
    print("Dimensions des valeurs de caracteristiques (y) :", y.shape)            # tuple : (lignes, colonnes)





# ======================================
# 3. Separer les donnees 
# ======================================

    x_train, x_test, y_train, y_test = separer_donnees(x, y)
    print("Dimensions de l'ensemble d'entrainement :", x_train.shape)
    print("Dimensions de l'ensemble de test :", x_test.shape)




# ======================================
# 4. Modele de reference 
# ======================================

    rmse_modele_de_reference = modele_de_reference(y_train, y_test)
    print("RMSE de reference :", round(rmse_modele_de_reference, 2))





# ===========================================================
# 5. Entrainer et evaluer le modele de regression lineaire
# ===========================================================

    modele = entrainer_modele(x_train, y_train)                        # Entrainer la regression lineaire
    predictions, rmse = evaluer_modele(modele, x_test, y_test)         # Predire les prix et calculer le RMSE
    print("RMSE de la regression lineaire :", round(rmse, 2))

    if rmse < rmse_modele_de_reference:                                # Comparer le modele de reference avec celui de regression lineaire
        print("La regression lineaire donne de meilleurs resultats que la reference")
    else:
        print("La regression lineaire ne donne pas de meilleurs resultats que la reference")

    chemin_predictions = os.path.join(dossier_graphiques, "predictions_vs_reelles.png")    # Creer le graphique de predictions 
    graphique_predictions_reels(y_test, predictions, chemin_predictions)




# ==================================================================
# 6. Sauvegarder le modele (joblib et fichier json/métadonnées)
# ==================================================================

    chemin_modele = os.path.join(dossier_modeles, "modele.joblib")
    chemin_json = os.path.join(dossier_modeles, "metadata.json")
    sauvegarder_modele(modele, x_train, rmse, chemin_modele, chemin_json)
    print("Modèle et métadonnées sauvegardés - Les six étapes du volet 2 sont terminées")





# ===============================
# 7. Éxécuter le programme
# ===============================

if __name__ == "__main__":
    main()
