# Fiche de décisions

| Choix | Options envisagées | Choix retenu et justification | Validé par l'auxiliaire (date) |
|--------|-------------------|-------------------------------|-------------------------------|
| Domaine | Aviation civile et transport aérien, immobilier et qualité de l’air | Immobilier : prédire le prix d'une maison.<br><br>Pourquoi ce domaine : secteur concret et facilement compréhensible, auquel chacun peut s'identifier avec de nombreux facteurs mesurables.<br><br>Ce que peut faire l'utilisateur avec l'application : Estimer le prix d’une maison par rapport à ces nombreux facteurs | 6 nov. |
| Jeu de données | US 2023 Civil Flights, delays, meteo and aircrafts, USA_price, air_quality_dataset | USA_price.csv.<br><br>Comment on a vérifié le nombre de lignes, colonnes d'entrée et types de variables : utilisation de `df.shape`, `df.columns` et `df.info()` | 6 nov. |
| Variable cible et métrique | MAE, RMSE et R² | Cible : prix.<br><br>Métrique : RMSE car permet d’exprimer l’erreur dans la même unité que le prix et pénalise davantage les grandes erreurs de prédiction.<br><br>Référence : modèle trivial prédisant toujours la valeur moyenne de prix. | |
| Modèle | Régression linéaire et le SVR (Support Vector Regression) | Régression linéaire car elle est adaptée à la prédiction d’une variable continue comme le prix d’une maison. | 13 nov. |
| Technologie d'interface | Tkinter, Gradio et Streamlit | Streamlit.<br><br>Pourquoi : facile à mettre en place et graphiques Matplotlib intégrés. | |
