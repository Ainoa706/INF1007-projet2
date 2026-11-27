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
-	Nombre de chambres (bedrooms)/salles de bain (bathrooms) : valeurs supérieures ou égales à 0.
-	Superficies (sqft_living, sqft_loft, sqft_above, sqft_basement) : nous avons vérifié que les différentes superficies étaient positives et plus grandes que 0. Par contre, pour la colonne sqft_basement, il était possible d’avoir une valeur égale à 0 puisque, réalistiquement, une maison pourrait ne pas avoir de sous-sol.
-   Cohérence des superficies : sqft_living doit être égal à sqft_above + sqft_basement.
-	Nombre d’étages (floors) : nous avons vérifié si les valeurs de cette colonne étaient plus grandes que 0 (+), car réalistiquement, une maison comporte au moins 1 étage.
-	Année de rénovation (yr_renovated) : égale à 0 lorsqu'aucune rénovation n'est indiquée, ou supérieure ou égale à l'année de construction (yr_built).
-	Condition de la maison (condition) : nous avons vérifié si cette variable prenait uniquement les valeurs 1, 2, 3, 4, 5 (échelle prédéfinie dans le jeu de données).
-	Vue (view) : nous avons vérifié si cette variable prenait uniquement les valeurs 0, 1, 2, 3, 4 (échelle prédéfinie dans le jeu de données).
-	Plan d’eau (waterfront) : nous avons vérifié si cette variable prenait uniquement les valeurs 0 et 1 inclusivement (échelle prédéfinie dans le jeu de données).

La sortie de notre code nous a donc permis de déterminer que notre jeu de données ne comportait aucune valeur manquante. Toutefois, nous avons pu détecter certaines incohérences. Par exemple, nous avons déterminé 49 observations dont le prix de la maison était égal à 0. Ainsi, nous avons décidé de retirer ces observations, car 0 ne représente pas un prix de vente exploitable, surtout que l’objectif de notre application sera de prédire le prix des différentes maisons en fonction de leurs caractéristiques. De plus, notre code nous a permis de repérer 179 observations dont l’année de rénovation précède l’année de construction, ce qui n’est pas logique. Nous avons donc décidé de retirer également ces observations.

Nous avons aussi supprimé six colonnes : statezip, street, sqft_basement, sqft_above, date et country. Pour ce qui a trait à statezip et street, celles-ci représentaient des données personelles, donc nous les avons supprimées. Pour ce qui a trait sqft_basement et sqft_above, làddition de ces 2 caracteristiques donnaient dors et déjà sqft_living, donc on en avait pas besoin. Pour ce qui à trait à date et country, cellesci éetaient les mêmes pour toutes les observations. 

Résultat du nettoyage : notre jeu de données contient 3 910 observations et 12 colonnes, soit 230 observations de moins qu'au départ. Ces 12 colonnes comprennent le prix à prédire et 11 caractéristiques utilisées par le modèle ("price", "bedrooms", "bathrooms" "sqft_living", "sqft_lot",  "floors", "waterfront", "view", "condition", "yr_built", "yr_renovated", "city")

Pour explorer les données nettoyées, nous produisons deux graphiques :
- graphique/graphique_prix.png : histogramme de la distribution des prix des maisons.
- graphique/graphique_surface_prix.png : nuage de points représentant le prix en fonction de la superficie habitable.

En analysant le grapgique de nuage de points représentant le prix en fonction de la superficie habitable, nous avons également pu enlever les données extrêmes (maisons les plus chères et les deux maisons ayant les plus grandes superficies habitables)



Étape 2 : Définir le problème
# ===================================================================
# INSTRUCTIONS
# ===================================================================
Variable cible, type de problème (classification ou régression) et métrique
d'évaluation justifiée (exactitude, F1, RMSE, R², etc.).

# ===================================================================
# EXPLICATIONS
# ===================================================================
Notre projet consiste à entraîner un modèle simple, puis à le mettre à la disposition d'un utilisateur grâce à une interface graphique. Pour cela, nous avons décidé d’utiliser un jeu de données sur les prix des maisons aux USA. Notre objectif est de développer une application permettant de déterminer le prix d’une maison (price) en fonction des caractéristiques choisies par l’utilisateur (bedrooms, bathrooms, sqft_living, sqft_loft, floors, yr_built, yr_renovated, condition, view, waterfront). Ainsi, notre variable cible est price (prix). Puisque la valeur cible à prédire (price) est numérique, il s’agit d'un problème de régression linéaire. En ce qui concerne la métrique d’évaluation, nous utiliserons la racine de l’erreur quadratique moyenne (RMSE), car elle mesure l'ampleur moyenne des erreurs de prédiction dans un modèle de régression. Ainsi, une faible valeur de RMSE indiquerait que notre modèle est assez précis dans ses prédictions.

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

D’une part, notre ensemble d’entraînement constitue 80 % des observations de notre jeu de données. Il permet à notre modèle de comprendre le lien entre le prix des maisons (variable cible) et leurs caractéristiques (bedrooms, bathrooms, sqft_living, sqft_loft, floors, yr_built, yr_renovated, condition, view, waterfront). D’autre part, notre ensemble de test constitue 20 % des observations de notre jeu de données. Il nous permet de vérifier si notre modèle est en mesure de prédire correctement le prix des maisons en fonction de leurs caractéristiques et ce, à partir de données auxquelles il n’a jamais été exposé durant son entrainement. Ceci est important, car en évaluant notre modèle sur de nouvelles données (différentes de celles de l'ensemble d'entraînement), nous pouvons mieux évaluer sa capacité à faire des prédictions.

De plus, afin de s’assurer d’obtenir la même répartition des données à chaque exécution du programme (rend nos résultats reproductibles), nous avons fixé random_state=42 (paramètre qui contrôle le mélange de données avant leur séparation en ensemble d’entrainement et ensemble de test).  



Étape 4 : Établir une référence
# ===================================================================
# INSTRUCTIONS
# ===================================================================
Un modèle trivial (classe majoritaire, moyenne) qui sert de point de
comparaison : sans lui, impossible de dire si votre score est bon.

# ===================================================================
# EXPLICATIONS
# ===================================================================
Pour évaluer la performance de notre modèle de prédiction (régression linéaire), nous avons programmé un modèle de référence (point de comparaison). Avec la fonction mean() de Pandas, nous avons calculé le prix moyen de toutes les maisons de notre ensemble d’entraînement (y_train). De plus, avec la fonction np.full() de NumPy, nous avons créé un tableau contenant une prédiction pour chaque maison de notre ensemble de test (y_test) et ce, sans tenir compte de leurs caractéristiques. À la suite de cela, nous avons utilisé notre propre fonction calculer_rmse() pour calculer la RMSE de notre modèle de référence en comparant les prix prédits aux prix réels des maisons. La RMSE obtenue pour notre modèle de référence est de 334 497.56 $. Notre régression linéaire doit donc idéalement obtenir une RMSE inférieure pour montrer qu'elle prédit le prix des maisons de manière plus précise. 



Étape 5 : Entraîner et évaluer le modèle de régression linéaire
# ===================================================================
# INSTRUCTIONS
# ===================================================================
Entraîner le modèle choisi, calculer la métrique sur l'ensemble de test, la
comparer à la référence, puis commenter honnêtement les résultats et les
limites (par exemple avec une matrice de confusion ou un graphique « prédit
contre réel »).

# ===================================================================
# EXPLICATIONS
# ===================================================================
Nous avons créer un modèle de régression linéaire en utilisant LinearRegression de scikit-learn. Notre modèle a pour objectif de déterminer le prix d'une maison en fonction de ses caractéeristiques. Les caractéristiques des maisons que nous avons conservées sont  les suivantes : "price", "bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors" "waterfront", "view", "condition", "yr_built", "yr_renovated" et "city". Nous avons commencé par tranformer nos variables catégorielles (city, view, condition et waterfront) en colonnes numéeriques et ce, en utilisant OneHotEncoder. Le reste des caractéeristiques étaient des variables numériques. Nous avons regroupé la préparation des données et la régression linéaire dans un Pipeline. Puis, nous avons entrainé le modèle sur x_train et y_train, puis utilisons modele.predict(x_test) pour prédire le prix des maisons de l'ensemble de test.

Pour évaluer la précision de nos résultats, nous comparons les prix prédits aux prix réels à l'aide de notre fonction calculer_rmse().

Modèle de référence (prix moyen des maisons) : RMSE = 334 497.56 $
Régréssion linéaire : RMSE = 198 776.19 $

Vu que notre régréssion linéaire obtient un RMSE inférieur à celui du modèle de référence, alors, cela indique qu'elle founit, sur cet ensemble de test, de meilleurs prédictions. Nous avons par la suite généré le graphique graphique/predictions_vs_reelles.png, qui compare les prix prédits aux prix réels. Chaque point représente une maison. La ligne rouge correspond à une prédiction parfaite. Ainsi, plus un point se trouve près de cette ligne, plus la prédiction du modèle est précise. Et plus un point s'en éloigne, plus l'erreur de prédiction est importante. Les points situés au-dessus de la ligne rouge indiquent que le modèle surestime le prix des maisons, tandis que ceux situés en dessous indiquent qu'il le sous-estime. À partir du graphique, il nous ait possible de remarquer que plusieurs points se trouvent près de la ligne rouge, indiquant ainsi que le modèle arrive à prédire certains prix avec une précision raisonnable. Par contre, nous pouvons également remarquer que certains points s'éloignent de cette ligne, iniquant ainsi que le modèle commet parfois des erreurs importantes. Ces erreurs peuvent s'expliquer par le fait que le prix d'une maison dépend de plusieurs facteurs et que notre modèle de régression linéaire n'arrive pas à représenter toutes les différentes relations entre ces variables et le prix d'une maison.



Étape 6 : Sauvegarder le modèle
# ===================================================================
# INSTRUCTIONS
# ===================================================================
Enregistrer le modèle entraîné (avec joblib , installé avec scikit-learn) et un
fichier JSON de métadonnées : noms des colonnes, valeurs possibles des
variables catégorielles, intervalles des variables numériques, métrique obtenue.
L'interface s'en servira pour se construire : le modèle n'est pas ré-entraîné à
chaque lancement.

# ===================================================================
# EXPLICATIONS
# ===================================================================
Pour finir, nous avons sauvegardé le modèle avec joblib dans le fichier modeles/modele.joblib pour réutiliser le modèle entrainé sans recommencer tout le processus d'entrainement. Nous avons aussi créer le fichier modeles/metadata.json qui contient la variable cible (price), les caractéristiques utilisées ("price", "bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors" "waterfront", "view", "condition", "yr_built", "yr_renovated" et "city"), les catégories reconnues pour les variables catégorielles (city, view, condition et waterfront) et la RMSE obtenue.



Étape 7 : Tests automatisés avec pytest
# ===================================================================
# EXPLICATIONS
# ===================================================================
Comme demandé dans l'énoncé du projet, nous avons utilisé pytest pour vérifier plusieurs fonctionnalités de notre programme :
- tests/test_donnees.py : les tests que nous avons effectués servaient principalement à vérifier le chargement du jeu de données, la suppression des colonnes inutiles, la conservation d'observations après nettoyage et la gestion d'un fichier inexistant.
- tests/test_modele.py : les tests que nous avons effectués servaient principalement à vérifier le calcul de la RMSE (avec la fonction que nous avions établit), une prédiction parfaite, des listes de dimensions différentes et des listes vides, la séparation des données et la capacité du modèle à prédire le prix d'une maison.






VOLET 3 : DÉVELOPPER L'INTERFACE GRAPHIQUE 
Étape 1 : Saisie des caractéristiques
# ===================================================================
# INSTRUCTIONS
# ===================================================================
Un champ par variable d'entrée, adapté à son type (champ numérique, liste
déroulante pour une catégorie, etc.), construit à partir des métadonnées du modèle
sauvegardé.
`
# ===================================================================
# EXPLICATIONS
# ===================================================================
Pour développer l'interface graphique, nous avons utilisé le bibliothèque Stramlit. Tout le code dédié à l'interface se trouve dans le fichier interface.py dans le dossier src. Pour lancer l'application de prédiction il faut donc d'abord télécharger les bibliothèques qui se trouve dan requirement.txt avec pip install -r requirements.txt et lancer la commande python -m streamlit run src/interface.py dans le terminal.

L'interface charge le modèle déjà entraîné et ses métadonnées (modele.joblib et metdata.json qui se trouvent dans le dossier modele). Le modèle est donc entraîné une seule fois, ce qui lui permet d'être plus rapide au lancement. L'interface charge également le jeu de données nettoyé grâce à la fonction nettoyer_donnees(), car elle s'en sert pour déterminer les valeurs minimales et maximales des champs numériques pour générer les graphiques proposés à l'utilisateur.
L'interface est divisée en plusieurs pages qui sont dans le menus de navigation à gauche de l'écran qui permet de passer d'une page à l'autre. On y retrouve, l'accueil, l'outil de prédiction, les graphiques d'information, l'historique et quitter.

Les saisies de carctéristiques des maisons pour la prédiction se font dans la page "Outil de prédiction" à l'aide du formulaire st.forme réparti en deux colonnes. Il comporte 11 champs, un par variable d'entrée dont le type est adapté à la nature de la variable:
- Les champs numériques (st.number_input) : nombre de chambres (bedrooms), nombre de salles de bain (bathrooms), nombre d'étages (floors), superficie habitable (sqft_living), superficie du terrain (sqft_lot), année de construction (yr_built) et année de rénovation (yr_renovated, où 0 signifie qu'aucune rénovation n'a été faite). Chaque champ possède une valeur par défaut, un minimum et maximum calculés à partir des données nettoyées. Ainsi, l'utilisateur ne peut pas entrer une valeur en dehors de la plage de notre jeu de données.
- Listes déroulantes (st.selectbox) : ville (city), qualité de la vue (view), état de la maison (condition) et présence d'un plan d'eau (waterfront). Les choix proposés sont lus directement dans la section variables_categorielles du fichier metadata.json : ce sont donc exactement les catégories que le modèle a rencontrées pendant son entraînement (43 villes, vue de 0 à 4, état de 1 à 5, plan d'eau 0 ou 1). Pour waterfront, la liste affiche « Oui » ou « Non » au lieu de 1 ou 0, afin que ce soit plus clair pour l'utilisateur.

Le formulaire contient un bouton "Prédire le prix". Les valeurs saisies ne sont envoyé au modèle que lorsque l'utilisateur clique sur ce bouton ce qui évite de relancer une nouvelle prédiction à chaque changement de caractéristique. Au moment où le bouton est cliqué, l'interface vérifie d'abord que l'année de rénovation est bien postérieure à l'année de construction et affiche un message d'erreur si c'est le cas. Sinon, les valeurs sont regroupées dans un dictionnaire transformées en DataFrame pandas, puis les colonnes sont placées dans le même ordre que celui indiqué dans metadata.json, avant d'appeler modele.predict(). Le prix estimé est ensuite affiché, accompagné d'un graphique qui situe l'estimation par rapport à la distribution des prix, et d'une comparaison avec le prix moyen des maisons de la ville choisie. Une prédiction invalide (prix négatif ou nul) ou une erreur du modèle est signalée à l'utilisateur par un message d'erreur plutôt que par un plantage de l'application.

Les autres pages de l'interface présentent :
- Les graphiques d'informatrion : l'utilisateur à les choix entre plusieurs graphiques : distribution des prix, le nuage de points superficie habitable / prix sur lequel sa dernière estimation apparaît en rouge et la distribution des prix pour une ville donnée.
- L'historique de recherche : Chaque prédiction est sauvegardée dans le fichier historique.csv dans le dossier donnees, avec la date de l'estimation, les caractéristiques saisies, le prix prédit et l'écart avec le prix moyen dans la ville de la prédiction. La page affiche un tableau de la racherche la plus récente à la plus ancienne et permet de télécharger le fichier.
- Quitter : Explique comment fermer l'application. Autrement dit, fermet l'onglet et effectuer un Ctrl + C dans le terminal VsCode.

Enfin, une mise en garde est affiché à l'utilisateur sur le page d'accueil et de prédiction.
