@echo off
echo Predicteur de Couts d'Assurance Maladie
echo =====================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python n est pas installe ou n est pas dans le PATH
    echo Veuillez installer Python 3.8+ depuis https://www.python.org/
    pause
    exit /b 1
)

echo Python detecte
echo.

REM Vérifier si les dépendances sont installées
echo  Verification des dependances...
pip show streamlit >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo  Installation des dependances...
    pip install -r requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo  Erreur lors de l'installation des dependances
        pause
        exit /b 1
    )
    echo  Dependances installees avec succes
) else (
    echo  Dependances deja installees
)

echo.

REM Vérifier si le modèle existe
if not exist "xgboost_optimized_pipeline.pkl" (
    echo  Modele non trouve: xgboost_optimized_pipeline.pkl
    echo  Executez d'abord le notebook data_analysis.ipynb pour generer le modele
    pause
    exit /b 1
)

echo  Modele trouve
echo.

REM Lancer l'application
echo  Lancement de l'application Streamlit...
echo  L'application va s'ouvrir dans votre navigateur à l'adresse: http://localhost:8501
echo.
echo  Pour arreter l'application, appuyez sur Ctrl+C
echo.

streamlit run app.py

pause