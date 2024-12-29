import sqlite3, random
from datetime import datetime, timedelta

# Ouverture/initialisation de la base de donnée 
conn = sqlite3.connect('logement.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Fonction pour ajouter des mesures aléatoires
def add_mesures_temperatures():
    # Récupérer tous les capteurs de température et actionneurs de lumière
    c.execute("SELECT id_capteur_actionneur, id_type FROM Capteur_Actionneur WHERE id_type IN (1)")
    capteurs_actionneurs = c.fetchall()

    # Si on a des capteurs/actionneurs pour la température et la lumière
    if capteurs_actionneurs:
        for capteur in capteurs_actionneurs:
            # Si c'est un capteur de température (id_type = 1)
            if capteur['id_type'] == 1:
                for _ in range(2):  # Ajouter 2 mesures par capteur/actionneur
                    # Générer une valeur de température aléatoire entre 18.0 et 30.0°C
                    valeur_mesure = random.uniform(18.0, 30.0)
                    c.execute("INSERT INTO Mesure (id_capteur_actionneur, valeur) VALUES (?, ?)", 
                              (capteur['id_capteur_actionneur'], round(valeur_mesure, 2)))
                    print(f"Mesure ajoutée pour le capteur de température (ID: {capteur['id_capteur_actionneur']}): {valeur_mesure}°C")
        print("Mesures ajoutées pour la température avec succès.")
    else:
        print("Aucun capteur de température trouvé.")

def add_mesures_luminosite():
    # Récupérer tous les capteurs de température et actionneurs de lumière
    c.execute("SELECT id_capteur_actionneur, id_type FROM Capteur_Actionneur WHERE id_type IN (3)")
    capteurs_actionneurs = c.fetchall()

    # Si on a des capteurs/actionneurs pour la température et la lumière
    if capteurs_actionneurs:
        for capteur in capteurs_actionneurs:
            # Si c'est un actionneur de lumière (id_type = 3)
            if capteur['id_type'] == 3:
                for _ in range(2):  # Ajouter 2 mesures par capteur/actionneur
                    # Générer une valeur de lumière aléatoire entre 100 et 1000 lux
                    valeur_mesure = random.uniform(100, 1000)
                    c.execute("INSERT INTO Mesure (id_capteur_actionneur, valeur) VALUES (?, ?)", 
                              (capteur['id_capteur_actionneur'], round(valeur_mesure, 2)))
                    print(f"Mesure ajoutée pour l'actionneur de lumière (ID: {capteur['id_capteur_actionneur']}): {valeur_mesure} Lux")
        
        print("Mesures ajoutées pour la lumière avec succès.")
    else:
        print("Aucun actionneur de lumière trouvé.")


# Fonction pour ajouter des factures aléatoires
def add_factures():
    # Récupérer tous les logements de la base de données
    c.execute("SELECT id_logement FROM Logement")
    logements = c.fetchall()

    # Si on a des logements dans la base
    if logements:
        for logement in logements:
            # Créer 4 factures aléatoires pour chaque logement
            for _ in range(4):
                # Choisir un type de facture aléatoire
                types_facture = ['Électricité', 'Eau', 'Gaz', 'Déchets']
                type_facture = random.choice(types_facture)

                # Générer une date aléatoire pour la facture (entre aujourd'hui et 6 mois en arrière)
                date_facture = datetime.now() - timedelta(days=random.randint(1, 180))
                date_facture_str = date_facture.strftime('%Y-%m-%d')

                # Générer des valeurs aléatoires pour le montant et la consommation
                montant = round(random.uniform(20.0, 150.0), 2)  # Montant entre 20 et 150
                valeur_consommation = round(random.uniform(10.0, 400.0), 2)  # Consommation entre 10 et 400

                c.execute("INSERT INTO Facture (id_logement, type, date_facture, montant, valeur_consommation) "
                          "VALUES (?, ?, ?, ?, ?)", 
                          (logement['id_logement'], type_facture, date_facture_str, montant, valeur_consommation))

        print("Factures ajoutées avec succès.")
    else:
        print("Aucun logement trouvé.")

# Appeler les fonctions pour ajouter des mesures et des factures
add_mesures_temperatures()
add_mesures_luminosite()
add_factures()

# Fermeture
conn.commit()
conn.close()
