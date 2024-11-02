import pickle
import pandas as pd
import streamlit as st
import numpy as np
import requests
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

# Chemin vers le modèle et l'encodeur
#path = "DemandeVelos/"

# Chargement du modèle, de l'encodeur et des données d'entraînement
with open("modeles/model_predict_velos.pkl", "rb") as f:
    model = pickle.load(f)

# Charger les données d'entraînement
df_data = pd.read_csv("data/hour.csv")  # Remplacez par le vrai fichier de données

# Configuration de l'application Streamlit avec des onglets
tab1, tab2, tab3 = st.tabs(["Prédiction de la demande", "Données observées", "À propos"])

with tab1:
    st.title("Prédiction de la demande de vélos")
    
    # Affichage de l'image avec une taille réduite
    image_url = "https://lvdneng.rosselcdn.net/sites/default/files/dpistyles_v2/vdn_864w/2020/12/14/node_907731/49885272/public/2020/12/14/B9725535150Z.1_20201214183109_000%2BGH5H7UO8U.2-0.jpg?itok=ieilkXI81607967238"
    image = Image.open(requests.get(image_url, stream=True).raw)
    st.image(image, caption="Vélos en libre-service", use_column_width=False, width=500)

    st.write("Ce site permet de faire des prévisions de demande de vélos entre les années 2011 et 2012.")
    
    # Formulaire de saisie pour les variables
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        season = st.selectbox("Saison", ["Été", "Automne", "Hiver", "Printemps"])
        yr = st.selectbox("Année", ["2011", "2012"])
        temp = st.number_input("Température norm", min_value=0.0, max_value=1.0, step=0.1)

    with col2:
        hr = st.selectbox("Heure (0-23)", list(range(24)))
        mnth = st.selectbox("Mois (1-12)", list(range(1, 13)))
        windspeed = st.number_input("Vitesse du vent (en km/h)", min_value=0.0, max_value=1.0, step=0.1)

    with col3:
        holiday = st.selectbox("Jour férié", ["Non", "Oui"])
        weekday = st.selectbox("0=Lundi, 6=Dimanche", list(range(7)))
        hum = st.number_input("Humidité (en %)", min_value=0.0, max_value=1.0, step=0.1)

    with col4:
        workingday = st.selectbox("Jour ouvré", ["Non", "Oui"])
        weathersit = st.selectbox("Condition météo", ["Clair", "Nuageux", "Pluvieux", "Orageux"])
        day = st.selectbox("Jours (1-31)", list(range(1, 32)))
    
    # Conversion des variables pour le modèle
    yr = int(yr)
    holiday = 1 if holiday == "Oui" else 0
    workingday = 1 if workingday == "Oui" else 0
    season = 0 if season == "Été" else 1 if season == "Automne" else 2 if season == "Hiver" else 3
    weathersit = 0 if weathersit == "Clair" else 1 if weathersit == "Nuageux" else 2 if weathersit == "Pluvieux" else 3

    # Prédiction de la demande de vélos
    if st.button("Prédire la demande de vélos"):
        observation = pd.DataFrame({'season': [season], 'yr': [yr], 'mnth': [mnth], 'hr': [hr], 'holiday': [holiday], 
                                    'weekday': [weekday], 'workingday': [workingday], 'weathersit': [weathersit],
                                    'temp': [temp], 'hum': [hum], 'windspeed': [windspeed], 'day': [day]})
        result = model.predict(observation)
        st.write(f"La demande de vélos prédite est : {result} vélos")

with tab2:
    st.title("Données Observées")
    
    # Affichage d'un aperçu des données
    st.write("### Aperçu de la base de données")
    st.write(df_data.head(4))

    st.write("### Visualisation")
    # Configurer le style de seaborn
    sns.set(style="whitegrid")

    # Création d'une figure avec plusieurs sous-graphes
    fig, axs = plt.subplots(3, 2, figsize=(10, 10))

    # 1. Évolution de la demande par heure
    sns.lineplot(x='hr', y='cnt', data=df_data, ax=axs[0, 0], marker='o', color='skyblue')
    axs[0, 0].set_title("Évolution de la demande de vélos par heure", color='white')
    axs[0, 0].set_xlabel("Heure", color='white')
    axs[0, 0].set_ylabel("Demande de vélos (cnt)", color='white')

    # 2. Évolution de la demande par jour
    sns.lineplot(x='day', y='cnt', data=df_data, ax=axs[0, 1], marker='o', color='lightgreen')
    axs[0, 1].set_title("Évolution de la demande de vélos par jour", color='white')
    axs[0, 1].set_xlabel("Jour", color='white')
    axs[0, 1].set_ylabel("Demande de vélos (cnt)", color='white')

    # 3. Évolution de la demande par mois
    sns.lineplot(x='mnth', y='cnt', data=df_data, ax=axs[1, 0], marker='o', color='coral')
    axs[1, 0].set_title("Évolution de la demande de vélos par mois", color='white')
    axs[1, 0].set_xlabel("Mois", color='white')
    axs[1, 0].set_ylabel("Demande de vélos (cnt)", color='white')

    # 4. Évolution de la demande par saison
    sns.barplot(x='season', y='cnt', data=df_data, ax=axs[1, 1], hue='season', palette='pastel', legend=False)
    axs[1, 1].set_title("Demande de vélos moyenne par saison", color='white')
    axs[1, 1].set_xlabel("Saison", color='white')
    axs[1, 1].set_ylabel("Demande moyenne de vélos", color='white')

    # 5. Boxplot de la demande de vélos par workingday
    sns.boxplot(x='workingday', y='cnt', data=df_data, ax=axs[2, 0], hue='workingday', palette='Set2', legend=False)
    axs[2, 0].set_title("Demande de vélos par jour ouvré", color='white')
    axs[2, 0].set_xlabel("Jour Ouvré (1=Oui, 0=Non)", color='white')
    axs[2, 0].set_ylabel("Demande de vélos (cnt)", color='white')

    # 6. Boxplot de la demande de vélos par holiday
    sns.boxplot(x='holiday', y='cnt', data=df_data, ax=axs[2, 1], hue='holiday', palette='Set2', legend=False)
    axs[2, 1].set_title("Demande de vélos par jour férié", color='white')
    axs[2, 1].set_xlabel("Jour Férié (1=Oui, 0=Non)", color='white')
    axs[2, 1].set_ylabel("Demande de vélos (cnt)", color='white')

    # Rendre l'arrière-plan transparent
    for ax in axs.flatten():
        ax.set_facecolor((0, 0, 0, 0))  # Arrière-plan transparent pour chaque axe
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_color('white')  # Couleur des étiquettes des axes

    # Rendre le fond de la figure transparent
    fig.patch.set_facecolor((0, 0, 0, 0))  # Arrière-plan transparent pour la figure

    plt.tight_layout()
    st.pyplot(fig)

with tab3:
    st.title("À propos")

    st.subheader("À propos de l'auteur")
    st.write("**Nom :** MAKAYA PASCALE")
    st.write("**Profession :** Data Scientist")
    st.write("**GitHub du projet:** [MPDErra](https://github.com/MPDerra/Prevision_demande_velo)")
    st.write("**LinkedIn:** [Durcinée Erra MAKAYA PASCALE](https://www.linkedin.com/in/durcinée-erra-makaya-pascale)")
    
    st.subheader("À propos du modèle retenu")
    st.write("Il s'agit d'une forêt aléatoire (random Forest).  \n C'est un modèle d'apprentissage ensembliste qui combine plusieurs arbres de décision pour effectuer des prédictions. Son fonctionnement se déroule en plusieurs étapes clés :")
    st.image("img/rf.png", caption=" Random Forest par E. Scornet",  width=400)
    st.write("- **Construction des arbres de décision** : Plusieurs arbres de décision sont construits de manière aléatoire à partir de sous-ensembles aléatoires du jeu de données d'entraînement.")
    st.write("- **Entraînement indépendant** : Chaque arbre de décision est entraîné indépendamment des autres, avec des échantillons de données différents obtenus par la méthode de bootstrap (échantillonnage aléatoire avec remise).")
    st.write("- **Construction d'un arbre de décision** : À chaque nœud de l'arbre, l'arbre sélectionne aléatoirement \(m\) variables explicatives parmi les \(d\) variables disponibles (avec \(m < d\)). Parmi les \(m\) variables sélectionnées, il choisit celle qui permet la meilleure séparation des données selon un critère d'impureté.")
    st.write("- **Prédiction** : Pour chaque nouvelle observation, la prédiction de la forêt aléatoire est le mode des prédictions de chaque arbre lorsque la variable cible est qualitative, et la moyenne arithmétique des prédictions de chaque arbre lorsque la variable cible est continue.")
