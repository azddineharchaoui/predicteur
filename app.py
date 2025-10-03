import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="🏥 Prédicteur de Coûts d'Assurance Maladie", page_icon="🏥", layout="wide", initial_sidebar_state="expanded")

# TailwindCSS Integration
st.markdown("""
<script src="https://cdn.tailwindcss.com"></script>
<style>
    html, body, [class*="css"] {font-size: 0.75rem !important;}
    .stButton>button {background:linear-gradient(135deg,#667eea 0%,#764ba2 100%)!important;color:white!important;border:none!important;border-radius:25px!important;padding:0.5rem 2rem!important;font-size:0.65rem!important;font-weight:bold!important;transition:all 0.3s!important}
    .stButton>button:hover {transform:translateY(-2px)!important;box-shadow:0 5px 15px rgba(0,0,0,0.2)!important}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    try:
        return joblib.load('xgboost_optimized_pipeline.pkl')
    except FileNotFoundError:
        st.error("❌ Modèle non trouvé! Assurez-vous que le fichier 'xgboost_optimized_pipeline.pkl' est dans le répertoire.")
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du modèle: {str(e)}")
    return None

def create_radar_chart(age, bmi, children, sex_encoded, smoker_encoded, region_encoded):
    values = [age/100, bmi/50, children/5, sex_encoded, smoker_encoded, region_encoded/3]
    labels = ['Âge', 'BMI', 'Enfants', 'Sexe', 'Fumeur', 'Région']
    
    fig = go.Figure(go.Scatterpolar(r=values+[values[0]], theta=labels+[labels[0]], fill='toself', 
                                    line=dict(color='#667eea', width=3), fillcolor='rgba(102,126,234,0.3)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=False, 
                      title="📊 Profil du Patient", title_x=0.5, height=400, font=dict(size=7.5))
    return fig

def create_cost_comparison(prediction):
    categories = ['Très Faible', 'Faible', 'Moyen', 'Élevé', 'Très Élevé']
    avg_costs = [2000, 5000, 10000, 20000, 35000]
    
    if prediction < 3000: category, color = 'Très Faible', '#28a745'
    elif prediction < 8000: category, color = 'Faible', '#6f42c1'
    elif prediction < 15000: category, color = 'Moyen', '#fd7e14'
    elif prediction < 25000: category, color = 'Élevé', '#dc3545'
    else: category, color = 'Très Élevé', '#6f1e1e'
    
    colors = ['#28a745' if cat == category else '#e9ecef' for cat in categories]
    
    fig = go.Figure(go.Bar(x=categories, y=avg_costs, marker_color=colors, 
                           text=[f'${cost:,.0f}' for cost in avg_costs], textposition='auto'))
    fig.add_hline(y=prediction, line_dash="dash", line_color=color, 
                  annotation_text=f"Votre Prédiction: ${prediction:,.0f}", annotation_position="top right")
    fig.update_layout(title="💰 Comparaison des Coûts d'Assurance", xaxis_title="Catégorie de Risque", 
                      yaxis_title="Coût ($)", showlegend=False, height=400)
    return fig

st.markdown('<h1 class="text-4xl font-bold text-center text-blue-600 mb-8 drop-shadow-lg">🏥 Prédicteur de Coûts d\'Assurance Maladie</h1>', unsafe_allow_html=True)

model = load_model()

if model is not None:
    st.sidebar.markdown('<h2 class="text-2xl font-bold text-pink-600 mb-4">📋 Informations Patient</h2>', unsafe_allow_html=True)
    with st.sidebar:
        # st.markdown("### 👤 Informations Personnelles")
        age = st.slider("🎂 Âge", 18, 80, 35, help="Âge du patient en années")
        bmi = st.slider("⚖️ Indice de Masse Corporelle (BMI)", 15.0, 50.0, 25.0, 0.1, help="BMI = poids(kg) / taille(m)²")
        children = st.selectbox("👶 Nombre d'enfants", [0,1,2,3,4,5], 0, help="Nombre d'enfants couverts par l'assurance")
        
        st.markdown("### 🏷️ Caractéristiques")
        sex = st.selectbox("👥 Sexe", ["Femme", "Homme"], 0, help="Sexe du patient")
        sex_encoded = 0 if sex == "Femme" else 1
        smoker = st.selectbox("🚭 Statut fumeur", ["Non-fumeur", "Fumeur"], 0, help="Le patient fume-t-il ?")
        smoker_encoded = 0 if smoker == "Non-fumeur" else 1
        region = st.selectbox("🗺️ Région", ["Northeast", "Northwest", "Southeast", "Southwest"], 0, help="Région géographique")
        region_encoded = {"Northeast": 0, "Northwest": 1, "Southeast": 2, "Southwest": 3}[region]
        
        st.markdown("---")
        predict_button = st.button("🔮 Prédire le Coût", use_container_width=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if predict_button:
            input_data = pd.DataFrame({'age': [age], 'bmi': [bmi], 'children': [children], 
                                      'sex_encoded': [sex_encoded], 'smoker_encoded': [smoker_encoded], 
                                      'region_encoded': [region_encoded]})
            try:
                prediction = model.predict(input_data)[0]
                st.markdown(f'<div class="bg-gradient-to-br from-indigo-500 to-purple-600 p-8 rounded-2xl text-center text-white my-8 shadow-2xl"><h2 class="text-xl mb-4">💰 Coût Prédit d\'Assurance</h2><h1 class="text-4xl font-bold">${prediction:,.2f}</h1><p class="mt-4 text-sm">Estimation basée sur votre profil</p></div>', unsafe_allow_html=True)
                st.plotly_chart(create_cost_comparison(prediction), use_container_width=True)
                st.markdown("### 📊 Analyse Détaillée")
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                
                with col_m1:
                    st.metric("💳 Coût Mensuel", f"${prediction/12:,.0f}", help="Estimation du coût mensuel")
                with col_m2:
                    st.metric("📅 Coût Quotidien", f"${prediction/365:.0f}", help="Estimation du coût quotidien")
                with col_m3:
                    st.metric("⚠️ Facteur Risque", "Élevé" if smoker_encoded == 1 else "Faible", help="Basé sur le statut fumeur")
                with col_m4:
                    bmi_cat = "Insuffisant" if bmi < 18.5 else "Normal" if bmi < 25 else "Surpoids" if bmi < 30 else "Obèse"
                    st.metric("⚖️ Catégorie BMI", bmi_cat, help="Basé sur l'IMC")
                
                st.markdown("### 💡 Conseils Personnalisés")
                advice = []
                if smoker_encoded == 1: advice.append("🚭 **Arrêter de fumer** pourrait considérablement réduire vos coûts d'assurance")
                if bmi >= 30: advice.append("🏃‍♂️ **Maintenir un poids santé** peut aider à réduire les risques de santé")
                elif bmi >= 25: advice.append("🥗 **Une alimentation équilibrée** peut contribuer à maintenir une bonne santé")
                if age >= 50: advice.append("🏥 **Checkups réguliers** sont recommandés pour la prévention")
                if not advice: advice.append("✅ **Félicitations!** Votre profil présente un risque relativement faible")
                
                for tip in advice:
                    st.markdown(f'<div class="bg-gradient-to-r from-pink-400 to-red-500 p-4 rounded-lg my-4 text-white">{tip}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la prédiction: {str(e)}")
    
    with col2:
        if predict_button:
            st.plotly_chart(create_radar_chart(age, bmi, children, sex_encoded, smoker_encoded, region_encoded), use_container_width=True)
        
        st.markdown("### 🤖 À propos du Modèle")
        st.markdown("- **Algorithme**: XGBoost Optimisé\n- **Précision**: R² ≈ 0.90\n- **Variables**: 6 caractéristiques\n- **Optimisation**: GridSearchCV")
        
        st.markdown("### 📈 Statistiques des Données")
        st.markdown("- **Echantillons**: 1,338 patients\n- **Cout moyen**: $13,270\n- **Age moyen**: 39 ans\n- **BMI moyen**: 30.7")

else:
    st.error("❌ Impossible de charger le modèle. Vérifiez que le fichier 'xgboost_optimized_pipeline.pkl' est présent.")

st.markdown("---")
st.markdown('<div class="text-center text-gray-600 py-5"><p>🏥 Prédicteur de Coûts d\'Assurance Maladie | Développé par Azeddine Harchaoui avec Streamlit et XGBoost</p></div>', unsafe_allow_html=True)