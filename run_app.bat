@echo off
echo 🏥 Prédicteur de Coûts d'Assurance Maladie
echo =====================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python 3.8+ depuis https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python détecté
echo.

REM Vérifier si les dépendances sont installées
echo 📦 Vérification des dépendances...
pip show streamlit >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo 📥 Installation des dépendances...
    pip install -r requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo ❌ Erreur lors de l'installation des dépendances
        pause
        exit /b 1
    )
    echo ✅ Dépendances installées avec succès
) else (
    echo ✅ Dépendances déjà installées
)

echo.

REM Vérifier si le modèle existe
if not exist "xgboost_optimized_pipeline.pkl" (
    echo ❌ Modèle non trouvé: xgboost_optimized_pipeline.pkl
    echo 💡 Exécutez d'abord le notebook data_analysis.ipynb pour générer le modèle
    pause
    exit /b 1
)

echo ✅ Modèle trouvé
echo.

REM Lancer l'application
echo 🚀 Lancement de l'application Streamlit...
echo 🌐 L'application va s'ouvrir dans votre navigateur à l'adresse: http://localhost:8501
echo.
echo 🛑 Pour arrêter l'application, appuyez sur Ctrl+C
echo.

streamlit run app.py

pause