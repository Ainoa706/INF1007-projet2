# ==================================================
# 1. IMPORTATION DES BIBLIOTHEQUES
# ==================================================

import os
import json
from datetime import datetime

import joblib
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from src.donnees import nettoyer_donnees


# ==================================================
# 2. CHARGER LE MODELE ET LES DONNEES
# ==================================================

# Retrouver le dossier principal du projet
dossier = os.path.dirname(os.path.dirname(__file__))

chemin_modele = os.path.join(dossier, "modeles", "modele.joblib")
chemin_json = os.path.join(dossier, "modeles", "metadata.json")
chemin_csv = os.path.join(dossier, "donnees", "USA_price.csv")
chemin_historique = os.path.join(dossier, "donnees", "historique.csv")

# Charger le modele deja entraine dans le volet 2
modele = joblib.load(chemin_modele)

# Charger les informations du modele
with open(chemin_json, "r", encoding="utf-8") as fichier:
    metadata = json.load(fichier)

# Charger et nettoyer les donnees pour les graphiques
df = pd.read_csv(chemin_csv)
df_clean = nettoyer_donnees(df)


# ==================================================
# 3. PAGE D'ACCUEIL
# ==================================================

def accueil():

    st.title("Outil d'estimation immobiliere")

    st.header("Bienvenue !")

    st.write(
        "Notre application permet d'estimer le prix d'une maison "
        "a partir de ses caracteristiques."
    )

    st.write("Selectionnez une fonctionnalite dans le menu de gauche.")

    st.info(
        "Cet outil est un exercice pedagogique et ne remplace "
        "pas une evaluation immobiliere professionnelle."
    )


# ==================================================
# 4. OUTIL DE PREDICTION
# ==================================================

def prediction():

    st.title("Outil de prediction")

    st.write("Entrez les caracteristiques de votre maison.")

    # Recuperer les categories du fichier metadata.json
    categories = metadata["variables_categorielles"]

    # Creer un formulaire
    with st.form("formulaire"):

        gauche, droite = st.columns(2)

        # Premiere colonne
        with gauche:

            chambres = st.number_input(
                "Nombre de chambres",
                min_value=0,
                step=1,
                max_value=int(df_clean["bedrooms"].max()),
                value=3
            )

            etages = st.number_input(
                "Nombre d'etages",
                min_value=int(df_clean["floors"].min()),
                max_value=int(df_clean["floors"].max()),
                value=1,
                step=1
            )

            vue = st.selectbox(
                "Qualite de la vue",
                categories["view"]
            )

            superficie = st.number_input(
                "Superficie habitable (pi²)",
                min_value=float(df_clean["sqft_living"].min()),
                max_value=float(df_clean["sqft_living"].max()),
                value=2000.0
            )

            construction = st.number_input(
                "Annee de construction",
                min_value=int(df_clean["yr_built"].min()),
                max_value=int(df_clean["yr_built"].max()),
                value=1980
            )

            ville = st.selectbox(
                "Ville",
                categories["city"]
            )

        # Deuxieme colonne
        with droite:

            salles_bain = st.number_input(
                "Nombre de salles de bain",
                min_value=0,
                max_value=int(df_clean["bathrooms"].max()),
                value=2,
                step=1
            )

            eau = st.selectbox(
                "Au bord de l'eau",
                categories["waterfront"],
                format_func=lambda valeur: "Oui" if valeur == 1 else "Non"
            )

            etat = st.selectbox(
                "Etat de la maison",
                categories["condition"]
            )

            terrain = st.number_input(
                "Superficie du terrain (pi²)",
                min_value=float(df_clean["sqft_lot"].min()),
                max_value=float(df_clean["sqft_lot"].max()),
                value=7500.0
            )

            renovation = st.number_input(
                "Annee de renovation (0 = aucune)",
                min_value=0,
                max_value=int(df_clean["yr_renovated"].max()),
                value=0
            )

        # Bouton de prediction
        bouton = st.form_submit_button("Predire le prix")

    # Effectuer la prediction lorsque le bouton est clique
    if bouton:

        if renovation != 0 and renovation < construction:
            st.error(
                "L'annee de renovation ne peut pas etre "
                "anterieure a l'annee de construction."
            )
            return

        # Creer un dictionnaire avec les informations entrees
        maison = {
            "bedrooms": chambres,
            "bathrooms": salles_bain,
            "sqft_living": superficie,
            "sqft_lot": terrain,
            "floors": etages,
            "yr_built": construction,
            "yr_renovated": renovation,
            "waterfront": eau,
            "view": vue,
            "condition": etat,
            "city": ville
        }

        # Transformer le dictionnaire en DataFrame
        entree = pd.DataFrame([maison])

        # Respecter l'ordre des caracteristiques du modele
        entree = entree[metadata["caracteristiques"]]

        try:
            # Predire le prix avec le modele du volet 2
            prix = float(modele.predict(entree)[0])

        except (ValueError, TypeError) as erreur:
            st.error(f"Prediction impossible : {erreur}")
            return

        if prix <= 0:
            st.error("Le modele a predit un prix invalide.")
            return

        # Sauvegarder le resultat pour les autres pages
        st.session_state["prix"] = prix
        st.session_state["superficie"] = superficie

        # Afficher le prix predit
        st.success("Prediction effectuee !")

        st.metric(
            "Prix estime de la maison",
            f"{prix:,.2f} $ US"
        )
    
        # Comparaison avec le prix moyen de la ville choisie
        donnees_ville = df_clean[df_clean["city"] == ville]

        moyenne = donnees_ville["price"].mean()

        difference = (prix - moyenne) / moyenne * 100

        st.write(
            f"Le prix estime est de {abs(difference):.1f} % "
            f"{'au-dessus' if difference >= 0 else 'en dessous'} "
            f"du prix moyen des maisons dans {ville}."
        )

        # Afficher un graphique dans la page
        fig, ax = plt.subplots()

        ax.hist(
            df_clean["price"],
            bins=30,
            label="Distribution des prix"
        )

        ax.axvline(
            prix,
            color="red",
            label="Votre estimation"
        )

        ax.set_title("Position du prix estime")
        ax.set_xlabel("Prix ($ US)")
        ax.set_ylabel("Nombre de maisons")
        ax.legend()

        st.pyplot(fig)
        plt.close(fig)

        # Ajouter la prediction a l'historique
        recherche = pd.DataFrame([{
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **maison,
            "prix_predit": prix,
            "difference_moyenne_pct": difference
        }])

        if os.path.exists(chemin_historique):

            historique = pd.read_csv(chemin_historique)
            historique = pd.concat(
                [historique, recherche],
                ignore_index=True
            )

        else:
            historique = recherche

        historique.to_csv(
            chemin_historique,
            index=False,
            encoding="utf-8-sig"
        )

    # Avertissement
    st.warning(
        "Cette estimation provient d'un modele de regression lineaire. "
        "Elle ne constitue pas une evaluation immobiliere professionnelle."
    )


# ==================================================
# 5. GRAPHIQUES D'INFORMATION
# ==================================================

def graphiques():

    st.title("Graphiques d'information")

    # L'utilisateur choisit le graphique
    choix = st.selectbox(
        "Choisissez un graphique",
        [
            "Distribution des prix",
            "Superficie / prix",
            "Prix / villes"
        ]
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    # Graphique 1 : distribution des prix
    if choix == "Distribution des prix":

        ax.hist(
            df_clean["price"],
            bins=30,
            label="Prix des maisons"
        )

        ax.set_title("Distribution des prix")
        ax.set_xlabel("Prix ($ US)")
        ax.set_ylabel("Nombre de maisons")
        ax.legend()

    # Graphique 2 : superficie et prix
    elif choix == "Superficie / prix":

        ax.scatter(
            df_clean["sqft_living"],
            df_clean["price"],
            alpha=0.4,
            label="Maisons du jeu de donnees"
        )

        # Afficher la derniere estimation si disponible
        if "prix" in st.session_state:

            ax.scatter(
                st.session_state["superficie"],
                st.session_state["prix"],
                color="red",
                s=100,
                label="Votre estimation"
            )

        ax.set_title("Superficie habitable et prix")
        ax.set_xlabel("Superficie habitable (pi²)")
        ax.set_ylabel("Prix ($ US)")
        ax.legend()

    # Graphique 3 : prix selon la ville
    else:

        ville = st.selectbox(
            "Selectionnez une ville",
            sorted(df_clean["city"].unique())
        )

        donnees_ville = df_clean[df_clean["city"] == ville]

        ax.hist(
            donnees_ville["price"],
            bins=20,
            label=ville
        )

        ax.set_title(f"Distribution des prix a {ville}")
        ax.set_xlabel("Prix ($ US)")
        ax.set_ylabel("Nombre de maisons")
        ax.legend()

    st.pyplot(fig)
    plt.close(fig)


# ==================================================
# 6. HISTORIQUE DES RECHERCHES
# ==================================================

def historique():

    st.title("Historique des recherches")

    if os.path.exists(chemin_historique):

        # Charger les predictions sauvegardees
        recherches = pd.read_csv(chemin_historique)

        # Afficher la recherche la plus recente en premier
        recherches = recherches.iloc[::-1]

        st.dataframe(
            recherches,
            use_container_width=True
        )

        # Permettre le telechargement de l'historique
        st.download_button(
            "Telecharger l'historique",
            recherches.to_csv(index=False).encode("utf-8-sig"),
            file_name="historique.csv",
            mime="text/csv"
        )

    else:
        st.info("Aucune recherche pour le moment.")


# ==================================================
# 7. MENU PRINCIPAL DE L'INTERFACE
# ==================================================

st.set_page_config(
    page_title="Estimation immobiliere",
    layout="wide"
)

# Menu dans la colonne de gauche
page = st.sidebar.radio(
    "Navigation",
    [
        "Accueil",
        "Outil de prediction",
        "Graphiques d'information",
        "Historique des recherches",
        "Quitter"
    ]
)

# Afficher la page choisie
if page == "Accueil":
    accueil()

elif page == "Outil de prediction":
    prediction()

elif page == "Graphiques d'information":
    graphiques()

elif page == "Historique des recherches":
    historique()

else:
    st.title("Quitter")
    st.write(
        "Vous pouvez fermer cet onglet pour quitter l'application."
    )
    st.write(
        "Pour arreter le serveur, appuyez sur Ctrl+C dans le terminal."
    )

