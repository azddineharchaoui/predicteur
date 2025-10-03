# 🏥 Prédicteur de Coûts d'Assurance Maladie

Une application Streamlit interactive qui utilise un modèle XGBoost optimisé pour prédire les coûts d'assurance maladie basé sur les caractéristiques du patient.

## 🚀 Fonctionnalités

- **Interface intuitive** : Interface utilisateur moderne et responsive
- **Prédictions en temps réel** : Utilise un modèle XGBoost optimisé avec GridSearchCV
- **Visualisations interactives** : Graphiques radar et de comparaison des coûts
- **Conseils personnalisés** : Recommandations basées sur le profil du patient
- **Métriques détaillées** : Coûts mensuels, quotidiens et facteurs de risque

## 📊 Caractéristiques d'entrée

L'application utilise 6 caractéristiques pour faire ses prédictions :

1. **Âge** : 18-80 ans
2. **BMI** : Indice de masse corporelle (15-50)
3. **Enfants** : Nombre d'enfants couverts (0-5)
4. **Sexe** : Homme/Femme
5. **Statut fumeur** : Fumeur/Non-fumeur
6. **Région** : Northeast, Northwest, Southeast, Southwest

## 🛠️ Installation

### Prérequis
- Python 3.8+
- pip

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Exécution de l'application

```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

## 📁 Structure du projet

```
predicteur/
├── app.py                                    # Application Streamlit principale
├── requirements.txt                          # Dépendances Python
├── xgboost_optimized_pipeline.pkl           # Modèle XGBoost pré-entraîné
├── data_analysis.ipynb                       # Notebook d'analyse des données
├── assurance-maladie.csv                    # Jeu de données original
└── README.md                                 # Ce fichier
```

## 🤖 À propos du Modèle

- **Algorithme** : XGBoost (Extreme Gradient Boosting)
- **Optimisation** : GridSearchCV avec validation croisée 5-fold
- **Performance** : R² ≈ 0.87
- **Données d'entraînement** : 1,338 échantillons
- **Pipeline** : Preprocessing complet avec imputation et standardisation

### Hyperparamètres optimisés :
- `learning_rate` : Taux d'apprentissage optimisé
- `max_depth` : Profondeur maximale des arbres
- `subsample` : Fraction d'échantillons par arbre

## 📈 Utilisation

1. **Lancez l'application** : `streamlit run app.py`
2. **Renseignez les informations** dans la barre latérale :
   - Informations personnelles (âge, BMI, enfants)
   - Caractéristiques (sexe, statut fumeur, région)
3. **Cliquez sur "Prédire le Coût"** pour obtenir l'estimation
4. **Consultez les résultats** :
   - Coût annuel prédit
   - Graphiques de comparaison
   - Métriques détaillées (coût mensuel, quotidien, etc.)
   - Conseils personnalisés

## 🎨 Interface

L'application propose :

- **Design moderne** avec dégradés et animations CSS
- **Graphiques interactifs** avec Plotly
- **Responsive design** adaptable à différentes tailles d'écran
- **Conseils intelligents** basés sur le profil utilisateur
- **Métriques visuelles** pour une meilleure compréhension

## ⚠️ Avertissement

Cette application est développée à des fins éducatives et de démonstration. Les prédictions ne doivent pas être utilisées pour prendre des décisions médicales ou financières réelles. Consultez toujours un professionnel qualifié pour des conseils spécialisés.

## 🛡️ Sécurité et Confidentialité

- Aucune donnée personnelle n'est stockée
- Toutes les prédictions sont calculées localement
- Aucune information n'est transmise à des services tiers

## 🚀 Déploiement

### Streamlit Cloud
1. Poussez votre code vers GitHub
2. Connectez-vous à [share.streamlit.io](https://share.streamlit.io)
3. Déployez directement depuis votre repository

### Docker (optionnel)
```bash
# Créer une image Docker
docker build -t predicteur-assurance .

# Lancer le conteneur
docker run -p 8501:8501 predicteur-assurance
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche pour votre feature
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📞 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation Streamlit
- Vérifiez les logs pour les erreurs

---

**Développé avec ❤️ en utilisant Streamlit, XGBoost et Plotly**