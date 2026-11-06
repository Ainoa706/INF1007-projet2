# INF1007-projet2
Entraîner un modèle simple, puis le mettre à la disposition d'un utilisateur grâce à une interface graphique.
Étape 1 : Explorer et nettoyer les données

# ===================================================================
# INSTRUCTIONS
# ===================================================================
Charger les données avec pandas ; examiner les types, les valeurs manquantes
et les valeurs aberrantes ; expliquer en quelques lignes ce que vous avez
corrigé et pourquoi. Produire au moins un graphique d'exploration.

# ===================================================================
# EXPLICATIONS
# ===================================================================
Nous avons commencé par explorer notre jeu de données, soit USA_price.csv, grâce à la bibliothèque pandas, que nous avons renommée pd. Avant toute modification, notre jeu de données comportait, au total, 4140 observations et 18 colonnes. Chaque observation représentait une maison en particulier et chaque colonne correspondait à une caractéristique de celle-ci.
Tout d’abord, nous avons développé un programme qui nous a permis de vérifier les types de données de chaque colonne (int, str, boolean, etc) et la présence de valeurs manquantes. Par la suite, nous avons examiné les variables numériques (price, bedrooms, bathrooms, sqft_living, sqft_loft, sqft_above, sqft_basement, floors, yr_built, yr_renovated, condition, view, waterfront) pour déterminer si leurs valeurs étaient aberrantes ou réalistes. Pour cela, nous avons établi plusieurs critères de validation :
-	Prix (price) : le prix de chaque maison devait être plus grand que 0, puisqu’une maison ne peut réalistiquement pas avoir une valeur marchande négative ou égale à 0.
-	Nombre de chambres (bedrooms)/salles de bain (bathrooms) : dans un premier temps, nous avons vérifié que les valeurs de ces caractéristiques n'étaient pas négatives, puisqu’une maison ne peut pas avoir un nombre négatif de chambres/salles de bain.
-	Superficies (sqft_living, sqft_loft, sqft_above, sqft_basement) : nous avons vérifié que les différentes superficies étaient positives et plus grandes que 0. Par contre, pour la colonne sqft_basement, il était possible d’avoir une valeur égale à 0 puisque, réalistiquement, une maison pourrait ne pas avoir de sous-sol.
-	Nombre d’étages (floors) : nous avons vérifié si les valeurs de cette colonne étaient plus grandes que 0, car réalistiquement, une maison comporte au moins 1 étage.
-	Année de construction (yr_built) et année de rénovation (yr_renovated) : nous avons vérifié si l’année de rénovation était plus grande ou égale à l’année de construction de la maison.
-	Condition de la maison (condition) : nous avons vérifié si cette variable prenait uniquement les valeurs 1, 2, 3, 4, 5 (échelle prédéfinie dans le jeu de données).
-	Vue (view) : nous avons vérifié si cette variable prenait uniquement les valeurs 0, 1, 2, 3, 4 (échelle prédéfinie dans le jeu de données).
-	Plan d’eau (waterfront) : nous avons vérifié si cette variable prenait uniquement les valeurs 0 et 1 inclusivement (échelle prédéfinie dans le jeu de données).
La sortie de notre code nous a donc permis de déterminer que notre jeu de données ne comportait aucune valeur manquante. Toutefois, nous avons pu détecter certaines incohérences. Par exemple, nous avons déterminé 49 observations dont le prix de la maison était égal à 0. Ainsi, nous avons décidé de retirer ces observations, car 0 ne représente pas un prix de vente exploitable, surtout que l’objectif de notre application sera de prédire le prix des différentes maisons en fonction de leurs caractéristiques. De plus, notre code nous a permis de repérer 179 observations dont l’année de rénovation précède l’année de construction, ce qui n’est pas logique. Nous avons donc décidé de retirer également ces observations.
Ensuite, nous avons développé un programme permettant de procéder au nettoyage de notre jeu de données en fonction des incohérences détectées précédemment. Au final, notre jeu de données contient présentement …. observations et … colonnes.
