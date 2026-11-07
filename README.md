# INF1007-projet2
Entraîner un modèle simple, puis le mettre à la disposition d'un utilisateur grâce à une interface graphique.

VOLET 2 : ENTRAINER UN MODELE SIMPLE 
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




Étape 2 : Définir le problème
# ===================================================================
# INSTRUCTIONS
# ===================================================================
Variable cible, type de problème (classification ou régression) et métrique
d'évaluation justifiée (exactitude, F1, RMSE, R², etc.).

# ===================================================================
# EXPLICATIONS
# ===================================================================
Notre projet consiste à entraîner un modèle simple, puis à le mettre à la disposition d'un utilisateur grâce à une interface graphique. Pour cela, nous avons décidé d’utiliser un jeu de données sur les prix des maisons aux USA. Notre objectif est de développer une application permettant de déterminer le prix d’une maison (price) en fonction des caractéristiques choisies par l’utilisateur (bedrooms, bathrooms, sqft_living, sqft_loft, sqft_above, sqft_basement, floors, yr_built, yr_renovated, condition, view, waterfront). Ainsi, notre variable cible est price (prix). Puisque la valeur cible à prédire (price) est numérique, il s’agit d'un problème de régression. En ce qui concerne la métrique d’évaluation, nous utiliserons la racine de l’erreur quadratique moyenne (RMSE), car elle mesure l'ampleur moyenne des erreurs de prédiction dans un modèle de régression. Ainsi, une faible valeur de RMSE indiquerait que notre modèle est assez précis dans ses prédictions.

En résumé, voici nos principales données :
-	Variable cible : price (prix des maisons)
-	Caractéristiques : bedrooms, bathrooms, sqft_living, sqft_loft, sqft_above, sqft_basement, floors, yr_built, yr_renovated, condition, view, waterfront
-	Type de problème : régression (on prédit le prix des maisons selon différentes caractéristiques choisies par l’utilisateur de l’application)
-	Métrique d’évaluation : RMSE




Étape 3 : Séparer les données
# ===================================================================
# INSTRUCTIONS
# ===================================================================
Ensembles d'entraînement et de test ( train_test_split ) avec une graine
aléatoire fixée pour que les résultats soient reproductibles. On n'évalue jamais
un modèle sur les données qui ont servi à l'entraîner.

# ===================================================================
# EXPLICATIONS
# ===================================================================
Nous avons utilisé traint_test_split(), une fonction de la bibliothèque scikit-learn, pour diviser, de façon aléatoire, l’ensemble de nos observations en deux, soit un ensemble d’entrainement et un ensemble de test.

D’une part, notre ensemble d’entraînement constitue 80 % des observations de notre jeu de données. Il permet à notre modèle de comprendre le lien entre le prix des maisons (variable cible) et leurs caractéristiques (bedrooms, bathrooms, sqft_living, sqft_loft, sqft_above, sqft_basement, floors, yr_built, yr_renovated, condition, view, waterfront). D’autre part, notre ensemble de test constitue 20 % des observations de notre jeu de données. Il nous permet de vérifier si notre modèle est en mesure de prédire correctement le prix des maisons en fonction de leurs caractéristiques et ce, à partir de données auxquelles il n’a jamais été exposé durant son entrainement. Ceci est important, car en évaluant notre modèle sur de nouvelles données (différentes de celles de l'ensemble d'entraînement), nous pouvons mieux évaluer sa capacité à faire des prédictions.

De plus, afin de s’assurer d’obtenir la même répartition des données à chaque exécution du programme (rend nos résultats reproductibles), nous avons fixé random_state=42 (paramètre qui contrôle le mélange de données avant leur séparation en ensemble d’entrainement et ensemble de test).  


































