from flask import Flask, jsonify, request, render_template, redirect
import sqlite3
import random
from datetime import datetime, timedelta
import requests  # Pour interagir avec l'API météo

# Clé API OpenWeatherMap (remplacez par votre clé personnelle)
API_KEY = "67004b1d7629d30d0581b7f290bec5ac"

# URL de base de l'API météo
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/forecast"

app = Flask(__name__)

# Fonction de connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route GET pour récupérer toutes les mesures d'un type de capteur
@app.route('/mesures/<int:type_id>', methods=['GET'])
def get_mesures(type_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM Mesure JOIN Capteur_Actionneur ON Mesure.id_capteur_actionneur = Capteur_Actionneur.id_capteur_actionneur WHERE Capteur_Actionneur.id_type = ?", (type_id,))
    mesures = c.fetchall()
    conn.close()
    return jsonify([dict(mesure) for mesure in mesures])

# Route POST pour ajouter des mesures de température aléatoires
@app.route('/add_mesures_temperature', methods=['POST'])
def add_mesures_temperatures():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id_capteur_actionneur FROM Capteur_Actionneur WHERE id_type = 1")
    capteurs = c.fetchall()

    if capteurs:
        for capteur in capteurs:
            for _ in range(2):  # Ajouter 2 mesures par capteur
                valeur_mesure = random.uniform(18.0, 30.0)
                c.execute("INSERT INTO Mesure (id_capteur_actionneur, valeur) VALUES (?, ?)", 
                          (capteur['id_capteur_actionneur'], round(valeur_mesure, 2)))
    conn.commit()
    conn.close()
    return jsonify({"message": "Mesures de temperature ajoutees avec succes."}), 201

# Route POST pour ajouter des mesures de luminosité aléatoires
@app.route('/add_mesures_luminosite', methods=['POST'])
def add_mesures_luminosite():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id_capteur_actionneur FROM Capteur_Actionneur WHERE id_type = 3")
    capteurs = c.fetchall()

    if capteurs:
        for capteur in capteurs:
            for _ in range(2):  # Ajouter 2 mesures par capteur
                valeur_mesure = random.uniform(100, 1000)
                c.execute("INSERT INTO Mesure (id_capteur_actionneur, valeur) VALUES (?, ?)", 
                          (capteur['id_capteur_actionneur'], round(valeur_mesure, 2)))
    conn.commit()
    conn.close()
    return jsonify({"message": "Mesures de luminosite ajoutées avec succes."}), 201

# Route POST pour ajouter des factures aléatoires
@app.route('/add_factures', methods=['POST'])
def add_factures():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id_logement FROM Logement")
    logements = c.fetchall()

    if logements:
        for logement in logements:
            for _ in range(4):  # Créer 4 factures par logement
                types_facture = ['Électricité', 'Eau', 'Gaz', 'Déchets']
                type_facture = random.choice(types_facture)
                date_facture = datetime.now() - timedelta(days=random.randint(1, 180))
                date_facture_str = date_facture.strftime('%Y-%m-%d')
                montant = round(random.uniform(20.0, 150.0), 2)
                valeur_consommation = round(random.uniform(10.0, 400.0), 2)
                
                c.execute("INSERT INTO Facture (id_logement, type, date_facture, montant, valeur_consommation) "
                          "VALUES (?, ?, ?, ?, ?)", 
                          (logement['id_logement'], type_facture, date_facture_str, montant, valeur_consommation))
    conn.commit()
    conn.close()
    return jsonify({"message": "Factures ajoutees avec succes."}), 201

# -------------------- Logements -------------------- #

@app.route('/logements', methods=['GET'])
def get_logements():
    conn = get_db_connection()
    logements = conn.execute("SELECT * FROM Logement").fetchall()
    conn.close()
    return jsonify([dict(logement) for logement in logements])

@app.route('/logements/<int:logement_id>', methods=['GET'])
def get_logement(logement_id):
    conn = get_db_connection()
    logement = conn.execute("SELECT * FROM Logement WHERE id_logement = ?", (logement_id,)).fetchone()
    conn.close()
    if logement is None:
        return jsonify({"error": "Logement non trouvé"}), 404
    return jsonify(dict(logement))

# -------------------- Pièces -------------------- #

@app.route('/pieces', methods=['GET'])
def get_pieces():
    conn = get_db_connection()
    pieces = conn.execute("SELECT * FROM Piece").fetchall()
    conn.close()
    return jsonify([dict(piece) for piece in pieces])

"""@app.route('/logements/<int:logement_id>/pieces', methods=['GET'])
def get_pieces_by_logement(logement_id):
    conn = get_db_connection()
    pieces = conn.execute("SELECT * FROM Piece WHERE id_logement = ?", (logement_id,)).fetchall()
    conn.close()
    return jsonify([dict(piece) for piece in pieces])"""

# -------------------- Types de Capteurs/Actionneurs -------------------- #

@app.route('/types_capteurs_actionneurs', methods=['GET'])
def get_types_capteurs_actionneurs():
    conn = get_db_connection()
    types = conn.execute("SELECT * FROM Type_Capteur_Actionneur").fetchall()
    conn.close()
    return jsonify([dict(type_) for type_ in types])

# -------------------- Capteurs/Actionneurs -------------------- #

@app.route('/capteurs_actionneurs', methods=['GET'])
def get_capteurs_actionneurs():
    conn = get_db_connection()
    capteurs_actionneurs = conn.execute("SELECT * FROM Capteur_Actionneur").fetchall()
    conn.close()
    return jsonify([dict(ca) for ca in capteurs_actionneurs])

@app.route('/pieces/<int:piece_id>/capteurs_actionneurs', methods=['GET'])
def get_capteurs_actionneurs_by_piece(piece_id):
    conn = get_db_connection()
    capteurs_actionneurs = conn.execute("SELECT * FROM Capteur_Actionneur WHERE id_piece = ?", (piece_id,)).fetchall()
    conn.close()
    return jsonify([dict(ca) for ca in capteurs_actionneurs])

# -------------------- Mesures -------------------- #

@app.route('/capteurs_actionneurs/<int:capteur_actionneur_id>/mesures', methods=['GET'])
def get_mesures_by_capteur(capteur_actionneur_id):
    conn = get_db_connection()
    mesures = conn.execute("SELECT * FROM Mesure WHERE id_capteur_actionneur = ?", (capteur_actionneur_id,)).fetchall()
    conn.close()
    return jsonify([dict(mesure) for mesure in mesures])

@app.route('/capteurs_actionneurs/<int:capteur_actionneur_id>/mesures', methods=['POST'])
def add_mesure(capteur_actionneur_id):
    valeur = request.json.get('valeur')
    if valeur is None:
        return jsonify({"error": "Valeur manquante"}), 400
    conn = get_db_connection()
    conn.execute("INSERT INTO Mesure (id_capteur_actionneur, valeur) VALUES (?, ?)", (capteur_actionneur_id, valeur))
    conn.commit()
    conn.close()
    return jsonify({"message": "Mesure ajoutée avec succès"}), 201

# -------------------- Factures -------------------- #

@app.route('/logements/<int:logement_id>/factures', methods=['GET'])
def get_factures_by_logement(logement_id):
    conn = get_db_connection()
    factures = conn.execute("SELECT * FROM Facture WHERE id_logement = ?", (logement_id,)).fetchall()
    conn.close()
    return jsonify([dict(facture) for facture in factures])

@app.route('/logements/<int:logement_id>/factures', methods=['POST'])
def add_facture(logement_id):
    type_facture = request.json.get('type')
    date_facture = request.json.get('date_facture')
    montant = request.json.get('montant')
    valeur_consommation = request.json.get('valeur_consommation')
    if not all([type_facture, date_facture, montant, valeur_consommation]):
        return jsonify({"error": "Informations de la facture incomplètes"}), 400
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO Facture (id_logement, type, date_facture, montant, valeur_consommation) VALUES (?, ?, ?, ?, ?)",
        (logement_id, type_facture, date_facture, montant, valeur_consommation)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Facture ajoutée avec succès"}), 201


# Route GET pour récupérer toutes les factures d'un logement
@app.route('/factures/<int:logement_id>', methods=['GET'])
def get_factures(logement_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM Facture WHERE id_logement = ?", (logement_id,))
    factures = c.fetchall()
    conn.close()
    return jsonify([dict(facture) for facture in factures])

@app.route('/factures_chart/<int:logement_id>', methods=['GET'])
def factures_chart(logement_id):
    # Connexion à la base de données
    conn = get_db_connection()
    c = conn.cursor()
    
    # Récupérer les types de factures et leurs montants pour le logement donné
    c.execute("""
        SELECT type, SUM(montant) as total_montant
        FROM Facture
        WHERE id_logement = ?
        GROUP BY type
    """, (logement_id,))
    factures = c.fetchall()
    conn.close()
    
    # Préparer les données pour Google Charts
    chart_data = [["Type de Facture", "Montant Total"]]  # En-têtes pour Google Charts
    for facture in factures:
        chart_data.append([facture["type"], facture["total_montant"]])
    
    # Convertir les données en JavaScript
    chart_data_js = str(chart_data)
    
    # Générer la page HTML avec Google Charts
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Diagramme Camembert des Factures</title>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
            google.charts.load('current', {{'packages':['corechart']}});
            google.charts.setOnLoadCallback(drawChart);
            
            function drawChart() {{
                var data = google.visualization.arrayToDataTable({chart_data_js});
                var options = {{
                    title: 'Répartition des Montants des Factures (Logement ID: {logement_id})',
                    is3D: true
                }};
                var chart = new google.visualization.PieChart(document.getElementById('piechart'));
                chart.draw(data, options);
            }}
        </script>
    </head>
    <body>
        <h1>Répartition des Montants des Factures</h1>
        <div id="piechart" style="width: 900px; height: 500px;"></div>
    </body>
    </html>
    """
    return html_content

# -------------------- Météo -------------------- #

@app.route('/meteo/<string:ville>', methods=['GET'])
def meteo_html(ville):
    """
    Route pour afficher les prévisions météo à 5 jours pour une ville donnée dans une page HTML élégante.
    """
    # Paramètres de la requête pour l'API météo
    params = {
        "q": ville,
        "appid": API_KEY,
        "units": "metric",  # Température en Celsius
        "lang": "fr"  # Français
    }

    try:
        # Requête vers l'API météo
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Extraction des prévisions
        previsions = []
        for forecast in data["list"][:5]:  # Limiter aux 5 premières prévisions
            previsions.append({
                "date": forecast["dt_txt"],
                "temperature": forecast["main"]["temp"],
                "description": forecast["weather"][0]["description"],
                "icon": forecast["weather"][0]["icon"]  # Récupérer l'icône
            })

        # Générer une page HTML
        html_content = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Prévisions météo pour {ville.capitalize()}</title>
            <style> /* Styles CSS pour la page HTML */
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                    color: #333;
                }}
                header {{
                    background-color: #007BFF;
                    color: white;
                    padding: 10px 20px;
                    text-align: center;
                }}
                .forecast {{
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                    margin: 20px;
                }}
                .forecast-card {{
                    background: white;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    margin: 10px;
                    padding: 15px;
                    width: 200px;
                    text-align: center;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }}
                .forecast-card img {{
                    width: 50px;
                    height: 50px;
                }}
                .temperature {{
                    font-size: 1.5em;
                    font-weight: bold;
                    color: #007BFF;
                }}
            </style>
        </head>
        <body>
            <header>
                <h1>Prévisions météo pour {ville.capitalize()}</h1>
            </header>
            <div class="forecast">
        """
        # Ajouter chaque prévision au contenu HTML
        for prev in previsions:
            html_content += f"""
            <div class="forecast-card">
                <h3>{prev["date"]}</h3>
                <img src="https://openweathermap.org/img/wn/{prev["icon"]}@2x.png" alt="{prev["description"]}">
                <p class="temperature">{prev["temperature"]}°C</p>
                <p>{prev["description"].capitalize()}</p>
            </div>
            """
        # Fin du contenu HTML
        html_content += """
            </div>
        </body>
        </html>
        """
        return html_content
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Erreur lors de la récupération des données météo", "details": str(e)}), 500
    except KeyError:
        return jsonify({"error": "Impossible de traiter les données reçues de l'API météo."}), 500


# -------------------- Pages Web -------------------- #
@app.route('/')
def accueil():
    # Exemple de données dynamiques pour la page d'accueil
    fonctionnalites = [
        {"titre": "Consommation", "description": "Visualisez votre consommation d'électricité, d'eau, et plus encore.", "lien": "consommation"},
        {"titre": "État des Capteurs", "description": "Surveillez en temps réel vos capteurs et actionneurs connectés.", "lien": "etat_capteurs"},
        {"titre": "Économies Réalisées", "description": "Comparez vos dépenses et suivez vos économies sur le long terme.", "lien": "economies"},
        {"titre": "Configuration", "description": "Ajoutez ou configurez vos capteurs et actionneurs pour une meilleure efficacité.", "lien": "configuration"}
    ]

    # API météo (actuelle + prévisions)
    api_key = "67004b1d7629d30d0581b7f290bec5ac"  # Remplacez par votre clé OpenWeatherMap
    forecast_api_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": "Paris",
        "appid": api_key,
        "units": "metric",  # Température en Celsius
        "lang": "fr"
    }

    try:
        response = requests.get(forecast_api_url, params=params)
        response.raise_for_status()
        forecast_data = response.json()

        # Météo actuelle
        meteo = {
            "description": forecast_data["list"][0]["weather"][0]["description"],
            "temperature": forecast_data["list"][0]["main"]["temp"],
            "icon": forecast_data["list"][0]["weather"][0]["icon"]
        }

        # Prévisions pour les prochains jours
        previsions = []
        for forecast in forecast_data["list"][1:4]:  # Limiter à 3 prévisions
            previsions.append({
                "date": forecast["dt_txt"],
                "temperature": forecast["main"]["temp"],
                "description": forecast["weather"][0]["description"],
                "icon": forecast["weather"][0]["icon"]
            })
    except requests.exceptions.RequestException:
        meteo = {"description": "Données indisponibles", "temperature": "N/A", "icon": "01d"}
        previsions = []

    # Coordonnées des campus
    campuses = [
        {"name": "Campus Pierre et Marie Curie", "lat": 48.84723238468744, "lon": 2.3555696971627142},
        {"name": "Campus Sorbonne", "lat": 48.84853699761031, "lon": 2.3434204860006393}
    ]

    return render_template('index.html', fonctionnalites=fonctionnalites, meteo=meteo, previsions=previsions, campuses=campuses)

@app.route('/consommation', methods=['GET'])
def consommation():
    conn = get_db_connection()

    # Récupérer les logements pour le filtre
    logements = conn.execute("SELECT id_logement, nom FROM Logement").fetchall()

    # Récupérer le logement sélectionné
    selected_logement_id = request.args.get('logement_id', type=int)

    # Récupérer les factures associées
    if selected_logement_id:
        factures = conn.execute("""
            SELECT id_facture, type, date_facture, montant
            FROM Facture
            WHERE id_logement = ?
            ORDER BY date_facture DESC
        """, (selected_logement_id,)).fetchall()
    else:
        factures = conn.execute("""
            SELECT id_facture, type, date_facture, montant
            FROM Facture
            ORDER BY date_facture DESC
        """).fetchall()

    # Préparer les données pour le graphique
    facture_par_mois = {}
    facture_ids = {}
    type_colors = {
        "Électricité": "rgba(255, 99, 132, 0.5)",
        "Eau": "rgba(54, 162, 235, 0.5)",
        "Gaz": "rgba(255, 206, 86, 0.5)",
        "Déchets": "rgba(75, 192, 192, 0.5)"
    }

    for facture in factures:
        mois = facture["date_facture"][:7]  # Extraire l'année et le mois (YYYY-MM)
        if mois not in facture_par_mois:
            facture_par_mois[mois] = {}
            facture_ids[mois] = {}

        facture_par_mois[mois][facture["type"]] = (
            facture_par_mois[mois].get(facture["type"], 0) + facture["montant"]
        )
        facture_ids[mois][facture["type"]] = facture["id_facture"]

    conn.close()

    return render_template(
        'consommation.html',
        logements=logements,
        factures=factures,
        facture_par_mois=facture_par_mois,
        facture_ids=facture_ids,  # Ajout des IDs de factures pour le graphique
        type_colors=type_colors,
        selected_logement_id=selected_logement_id
    )




@app.route('/etat_capteurs', methods=['GET', 'POST'])
def etat_capteurs():
    """
    Affiche l'état des capteurs/actionneurs d'un logement sélectionné et permet leur suppression.
    """
    conn = get_db_connection()

    # Récupérer tous les logements pour le sélecteur
    logements = conn.execute("SELECT id_logement, nom, adresse FROM Logement").fetchall()

    # Gérer la suppression d'un capteur
    if request.method == 'POST':
        id_capteur_actionneur = request.json.get('id_capteur_actionneur')
        if id_capteur_actionneur:
            try:
                conn.execute("DELETE FROM Capteur_Actionneur WHERE id_capteur_actionneur = ?", (id_capteur_actionneur,))
                conn.commit()
                return jsonify({"message": "Capteur supprimé avec succès."}), 200
            except sqlite3.Error as e:
                return jsonify({"error": f"Erreur lors de la suppression du capteur : {e}"}), 500

    # Récupérer le logement sélectionné (via un paramètre GET)
    logement_id = request.args.get('logement_id', type=int)  # None si aucun logement sélectionné
    capteurs_data = []

    if logement_id:
        # Récupérer les capteurs/actionneurs du logement sélectionné
        capteurs = conn.execute("""
            SELECT 
                c.id_capteur_actionneur, 
                c.reference_commerciale, 
                t.nom_type as type,
                m.valeur, 
                MAX(m.date_insertion) as derniere_mise_a_jour,
                p.nom as piece
            FROM Capteur_Actionneur c
            LEFT JOIN Type_Capteur_Actionneur t ON c.id_type = t.id_type
            LEFT JOIN Mesure m ON c.id_capteur_actionneur = m.id_capteur_actionneur
            LEFT JOIN Piece p ON c.id_piece = p.id_piece
            WHERE p.id_logement = ?
            GROUP BY c.id_capteur_actionneur
        """, (logement_id,)).fetchall()

        capteurs_data = [
            {
                "id": capteur["id_capteur_actionneur"],
                "nom": capteur["reference_commerciale"],
                "type": capteur["type"],
                "valeur": capteur["valeur"],
                "derniere_mise_a_jour": capteur["derniere_mise_a_jour"],
                "piece": capteur["piece"]
            }
            for capteur in capteurs
        ]

    conn.close()

    # Rendre la page avec les données des logements et des capteurs
    return render_template('etat_capteurs.html', logements=logements, capteurs_data=capteurs_data, logement_id=logement_id)


@app.route('/economies', methods=['GET'])
def economies():
    conn = get_db_connection()

    # Récupérer les logements pour le filtre
    logements = conn.execute("SELECT id_logement, nom FROM Logement").fetchall()

    # Récupérer le logement sélectionné via un paramètre GET
    selected_logement_id = request.args.get('logement_id', type=int)

    # Récupérer les montants totaux par mois
    if selected_logement_id:
        factures = conn.execute("""
            SELECT
                strftime('%Y-%m', date_facture) AS mois,
                SUM(montant) AS total_montant
            FROM Facture
            WHERE id_logement = ?
            GROUP BY mois
            ORDER BY mois
        """, (selected_logement_id,)).fetchall()
    else:
        factures = conn.execute("""
            SELECT
                strftime('%Y-%m', date_facture) AS mois,
                SUM(montant) AS total_montant
            FROM Facture
            GROUP BY mois
            ORDER BY mois
        """).fetchall()

    conn.close()

    # Calcul des économies réalisées (5% à 10% du montant total)
    economies_par_mois = {}
    for facture in factures:
        mois = facture["mois"]
        montant_total = facture["total_montant"]
        economies = montant_total * random.uniform(0.05, 0.10)  # Entre 5% et 10%
        economies_par_mois[mois] = round(economies, 2)  # Arrondi à 2 décimales

    return render_template(
        'economies.html',
        logements=logements,
        economies_par_mois=economies_par_mois,
        selected_logement_id=selected_logement_id
    )


@app.route('/configuration', methods=['GET', 'POST'])
def configuration():
    """
    Gère la configuration des utilisateurs, l'ajout de capteurs et de factures.
    """
    conn = get_db_connection()

    if request.method == 'POST':
        action = request.form.get('action')  # Identifier l'action (ajout de capteur ou de facture)

        if action == "add_facture":
            id_logement = request.form.get('logement')  # Récupéré depuis le champ caché
            print(f"ID du logement pour la facture : {id_logement}")

            type_facture = request.form.get('type')
            date_facture = request.form.get('date')
            montant = request.form.get('montant')

            conn.execute("""
                INSERT INTO Facture (id_logement, type, date_facture, montant)
                VALUES (?, ?, ?, ?)
            """, (id_logement, type_facture, date_facture, montant))
            conn.commit()

        elif action == "add_capteur":
            id_piece = request.form.get('piece')
            id_type = request.form.get('type')
            reference = request.form.get('reference')

            conn.execute("""
                INSERT INTO Capteur_Actionneur (id_piece, id_type, reference_commerciale)
                VALUES (?, ?, ?)
            """, (id_piece, id_type, reference))
            conn.commit()

        conn.close()
        return redirect('/configuration')

    # Récupérer l'ID du logement sélectionné depuis les paramètres GET
    selected_logement_id = request.args.get('logement', type=int)

    # Récupérer les logements pour le sélecteur
    logements = conn.execute("SELECT id_logement, nom FROM Logement").fetchall()

    # Si un logement est sélectionné, récupérer les pièces associées
    pieces = []
    if selected_logement_id:
        pieces = conn.execute("SELECT id_piece, nom FROM Piece WHERE id_logement = ?", (selected_logement_id,)).fetchall()

    # Récupérer les types de capteurs/actionneurs
    types_capteurs = conn.execute("SELECT id_type, nom_type FROM Type_Capteur_Actionneur").fetchall()
    conn.close()

    # Rendre le formulaire HTML
    return render_template(
        'configuration.html',
        logements=logements,
        pieces=pieces,
        types_capteurs=types_capteurs,
        selected_logement_id=selected_logement_id
    )

@app.route('/api/pieces/<int:logement_id>', methods=['GET'])
def get_pieces_by_logement(logement_id):
    """
    Récupère toutes les pièces d'un logement spécifique.
    """
    conn = get_db_connection()
    pieces = conn.execute("SELECT id_piece, nom FROM Piece WHERE id_logement = ?", (logement_id,)).fetchall()
    conn.close()
    return jsonify([{"id_piece": piece["id_piece"], "nom": piece["nom"]} for piece in pieces])



# -------------------- Test ESP -------------------- #

@app.route('/esp/actionneur/<int:id_actionneur>', methods=['GET'])
def controle_actionneur(id_actionneur):
    """
    Récupère la température extérieure et renvoie une commande pour un actionneur.
    """
    seuil_temperature = 25.0  # Seuil prédéfini pour allumer/éteindre la LED

    # Récupérer la température extérieure via l'API météo
    params = {
        "q": "Paris",  # Remplacez par la ville voulue
        "appid": API_KEY,
        "units": "metric",
        "lang": "fr"
    }
    try:
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        temperature_exterieure = data["list"][0]["main"]["temp"]

        # Logique pour contrôler l'actionneur
        if temperature_exterieure > seuil_temperature:
            commande = "ALLUMER"  # Par exemple, allumer la LED
        else:
            commande = "ETEINDRE"  # Par exemple, éteindre la LED

        return jsonify({
            "id_actionneur": id_actionneur,
            "commande": commande,
            "temperature_exterieure": temperature_exterieure
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Erreur lors de la récupération des données météo", "details": str(e)}), 500


# -------------------- Suppression -------------------- #
@app.route('/delete_facture/<int:id_facture>', methods=['POST'])
def delete_facture(id_facture):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM Facture WHERE id_facture = ?", (id_facture,))
        conn.commit()
        return jsonify({"message": "Facture supprimée avec succès."}), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Erreur lors de la suppression de la facture : {e}"}), 500
    finally:
        conn.close()

@app.route('/delete_capteur/<int:id_capteur_actionneur>', methods=['POST'])
def delete_capteur(id_capteur_actionneur):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM Capteur_Actionneur WHERE id_capteur_actionneur = ?", (id_capteur_actionneur,))
        conn.commit()
        return jsonify({"message": "Capteur/Actionneur supprimé avec succès."}), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Erreur lors de la suppression du capteur/actionneur : {e}"}), 500
    finally:
        conn.close()


# Lancement du serveur
if __name__ == '__main__':
    app.run(debug=True)
