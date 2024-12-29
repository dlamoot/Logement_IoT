-- Question 2 : Destruction des tables si elles existent

DROP TABLE IF EXISTS Logement;
DROP TABLE IF EXISTS Facture;
DROP TABLE IF EXISTS Piece;
DROP TABLE IF EXISTS Mesure;
DROP TABLE IF EXISTS Capteur_Actionneur;
DROP TABLE IF EXISTS Type_Capteur_Actionneur;

-- Question 3 : Création des tables

CREATE TABLE Logement (
    id_logement INTEGER PRIMARY KEY AUTOINCREMENT, -- Identifiant unique pour chaque logement
    nom TEXT NOT NULL, -- Nom du logement
    adresse TEXT NOT NULL, -- Adresse du logement
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Date d'insertion automatique
);

CREATE TABLE Piece (
    id_piece INTEGER PRIMARY KEY AUTOINCREMENT,     -- Identifiant unique pour chaque pièce
    id_logement INTEGER,                            -- Référence au logement auquel appartient la pièce
    nom TEXT,                                       -- Nom de la pièce (ex. : salon, cuisine)
    x INT,                                          -- Coordonnée X de la pièce
    y INT,                                          -- Coordonnée Y de la pièce
    z INT,                                          -- Coordonnée Z de la pièce
    FOREIGN KEY (id_logement) REFERENCES Logement(id_logement) ON DELETE CASCADE -- Si un logement est supprimé, toutes les pièces associés sont également supprimés
);


CREATE TABLE Type_Capteur_Actionneur (
    id_type INTEGER PRIMARY KEY AUTOINCREMENT,      -- Identifiant unique pour chaque type de capteur/actionneur
    nom_type TEXT NOT NULL,                         -- Nom du type de capteur/actionneur (ex. : température)
    unite_mesure TEXT,                              -- Unité de mesure (ex. : °C, kWh)
    plage_precision TEXT                            -- Précision d'un capteur ou plage de fonctionnement actionneur
);

CREATE TABLE Capteur_Actionneur (
    id_capteur_actionneur INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identifiant unique
    id_piece INTEGER,                              -- Référence à la pièce où se trouve le capteur/actionneur
    id_type INTEGER,                               -- Type du capteur/actionneur
    reference_commerciale TEXT,                    -- Référence commerciale du capteur/actionneur
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Date d'insertion automatique
    FOREIGN KEY (id_piece) REFERENCES Piece(id_piece) ON DELETE SET NULL, -- Si un capteur_actionneur est supprimé, toutes les mesures associés sont mises à NULL
    FOREIGN KEY (id_type) REFERENCES Type_Capteur_Actionneur(id_type) ON DELETE SET NULL -- Si un capteur_actionneur est supprimé, toutes les mesures associés sont mises à NULL
);

CREATE TABLE Mesure (
    id_mesure INTEGER PRIMARY KEY AUTOINCREMENT,   -- Identifiant unique pour chaque mesure
    id_capteur_actionneur INTEGER,                 -- Référence au capteur/actionneur ayant enregistré la mesure
    valeur FLOAT,                                  -- Valeur mesurée
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Date d'insertion automatique
    FOREIGN KEY (id_capteur_actionneur) REFERENCES Capteur_Actionneur(id_capteur_actionneur) ON DELETE CASCADE -- Si un capteur_actionneur est supprimé
);

CREATE TABLE Facture (
    id_facture INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identifiant unique pour chaque facture
    id_logement INTEGER,                           -- Référence au logement associé à la facture
    type TEXT,                                     -- Type de facture (eau, électricité, déchets, etc.)
    date_facture DATE,                             -- Date de la facture
    montant FLOAT,                                 -- Montant de la facture
    valeur_consommation FLOAT,                     -- Valeur de consommation enregistrée dans la facture
    FOREIGN KEY (id_logement) REFERENCES Logement(id_logement) ON DELETE CASCADE -- Si un logement est supprimé, toutes les factuires associés sont également supprimés
);

-- Question 4 : Ajout d'un logement avec x pièces

-- Insertion d'un logement
INSERT INTO Logement (nom, adresse) 
VALUES ('Campus Pierre et Marie Curie','4 Place Jussieu 75005 Paris');

INSERT INTO Logement (nom, adresse) 
VALUES ('Campus Sorbonne','1 rue Victor Cousin 75005 Paris');

-- Insertion de x pièces dans ce logement
INSERT INTO Piece (id_logement, nom, x, y, z) VALUES (1, 'Amphi 44', 0, 0, 0);
INSERT INTO Piece (id_logement, nom, x, y, z) VALUES (1, 'Amphi Durand', 1, 0, 0);
INSERT INTO Piece (id_logement, nom, x, y, z) VALUES (1, 'Amphi Astier', 0, 1, 0);

INSERT INTO Piece (id_logement, nom, x, y, z) VALUES (2, 'Grand Amphithéâtre', 0, 0, 0);
INSERT INTO Piece (id_logement, nom, x, y, z) VALUES (2, 'Amphi Richelieu', 1, 0, 0);
INSERT INTO Piece (id_logement, nom, x, y, z) VALUES (2, 'Amphi Champollion', 0, 1, 0);

-- Question 5 : Création de 4 types capteurs/actionneurs

-- Type 1 : Capteur de température
INSERT INTO Type_Capteur_Actionneur (nom_type, unite_mesure, plage_precision) VALUES ('Température', '°C', '±0.5°C');

-- Type 2 : Capteur d'humidité
INSERT INTO Type_Capteur_Actionneur (nom_type, unite_mesure, plage_precision) VALUES ('Humidité', '%', '±3%');

-- Type 3 : Actionneur de lumière
INSERT INTO Type_Capteur_Actionneur (nom_type, unite_mesure, plage_precision) VALUES ('Lumière', 'Lux', '0-1000 Lux');

-- Type 4 : Actionneur de chauffage
INSERT INTO Type_Capteur_Actionneur (nom_type, unite_mesure, plage_precision) VALUES ('Chauffage', '°C', '1-30°C');

-- Question 6 : Création de 2 capteurs/actionneurs

-- Capteur dans le Salon (par exemple, un capteur de température)
INSERT INTO Capteur_Actionneur (id_piece, id_type, reference_commerciale)  VALUES (1, 1, 'DHT11');  -- Le type 1 correspond à un capteur de température

-- Actionneur dans la Chambre (par exemple, un actionneur de lumière)
INSERT INTO Capteur_Actionneur (id_piece, id_type, reference_commerciale)  VALUES (3, 3, 'LIGHT');  -- Le type 3 correspond à un actionneur de lumière

-- Question 7 : Création de 2 mesures par capteur/actionneur

-- Mesures pour le capteur de température dans le Salon (id_capteur_actionneur = 1)
INSERT INTO Mesure (id_capteur_actionneur, valeur) VALUES (1, 22.5);  -- Température mesurée : 22.5°C
INSERT INTO Mesure (id_capteur_actionneur, valeur) VALUES (1, 23.0);  -- Température mesurée : 23.0°C

-- Mesures pour l'actionneur de lumière dans la Chambre (id_capteur_actionneur = 2)
INSERT INTO Mesure (id_capteur_actionneur, valeur) VALUES (2, 150.0);  -- Lumière mesurée : 150 Lux
INSERT INTO Mesure (id_capteur_actionneur, valeur) VALUES (2, 180.0);  -- Lumière mesurée : 180 Lux

-- Question 8 : Création de 4 factures au minimum

-- Logement 1 : Campus Pierre et Marie Curie

-- Facture 1 : Facture d'électricité pour le logement 1
INSERT INTO Facture (id_logement, type, date_facture, montant, valeur_consommation) 
VALUES (1, 'Électricité', '2024-01-31', 2200, 350.0);  -- Montant de 120.50 € pour 350 kWh

INSERT INTO Facture (id_logement, type, date_facture, montant, valeur_consommation) 
VALUES (1, 'Électricité', '2024-02-25', 2000, 350.0);  -- Montant de 120.50 € pour 350 kWh

INSERT INTO Facture (id_logement, type, date_facture, montant, valeur_consommation) 
VALUES (1, 'Électricité', '2024-03-29', 1900, 350.0);  -- Montant de 120.50 € pour 350 kWh

INSERT INTO Facture (id_logement, type, date_facture, montant, valeur_consommation) 
VALUES (1, 'Électricité', '2024-04-30', 1800, 350.0);  -- Montant de 120.50 € pour 350 kWh

INSERT INTO Facture (id_logement, type, date_facture, montant, valeur_consommation) 
VALUES (1, 'Électricité', '2024-05-31', 1700, 350.0);  -- Montant de 120.50 € pour 350 kWh

INSERT INTO Facture (id_logement, type, date_facture, montant, valeur_consommation) 
VALUES (1, 'Électricité', '2024-06-28', 1600, 350.0);  -- Montant de 120.50 € pour 350 kWh

INSERT INTO Facture (id_logement, type, date_facture, montant, valeur_consommation) 
VALUES (1, 'Électricité', '2024-07-31', 1400, 350.0);  -- Montant de 120.50 € pour 350 kWh

INSERT INTO Facture (id_logement, type, date_facture, montant, valeur_consommation) 
VALUES (1, 'Électricité', '2024-08-29', 1500, 350.0);  -- Montant de 120.50 € pour 350 kWh

INSERT INTO Facture (id_logement, type, date_facture, montant, valeur_consommation) 
VALUES (1, 'Électricité', '2024-09-30', 1600, 350.0);  -- Montant de 120.50 € pour 350 kWh

INSERT INTO Facture (id_logement, type, date_facture, montant, valeur_consommation) 
VALUES (1, 'Électricité', '2024-10-27', 1900, 350.0);  -- Montant de 120.50 € pour 350 kWh

INSERT INTO Facture (id_logement, type, date_facture, montant, valeur_consommation) 
VALUES (1, 'Électricité', '2024-11-30', 2100, 350.0);  -- Montant de 120.50 € pour 350 kWh


-- Facture 2 : Facture d'eau pour le logement 1
INSERT INTO Facture (id_logement, type, date_facture, montant, valeur_consommation) 
VALUES (1, 'Eau', '2024-10-05', 45.30, 15.5);  -- Montant de 45.30 € pour 15.5 m³

-- Facture 3 : Facture de déchets pour le logement 1
INSERT INTO Facture (id_logement, type, date_facture, montant, valeur_consommation) 
VALUES (1, 'Déchets', '2024-10-10', 25.00, 0);  -- Montant de 25.00 € pour la collecte des déchets

-- Facture 4 : Facture de gaz pour le logement 1
INSERT INTO Facture (id_logement, type, date_facture, montant, valeur_consommation) 
VALUES (1, 'Gaz', '2024-10-15', 78.90, 100.0);  -- Montant de 78.90 € pour 100 m³ de gaz