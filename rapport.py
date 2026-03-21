"""
Module 2: Génération du Rapport JSON (rapport.py)
"""


import json
import os
import sys
from datetime import datetime
from pathlib import Path


def recuperer_chemin_base():
    
    # Récupère le répertoire où se trouve ce fichier (rapport.py)
    fichier_courant = Path(__file__).resolve()
    # Remonte d'un niveau pour obtenir la racine du projet
    return fichier_courant.parent


def creer_dossier_rapports(chemin_base):
    
    dossier_rapports = os.path.join(chemin_base, "rapports")
    
    if not os.path.exists(dossier_rapports):
        os.makedirs(dossier_rapports)
        print(f"Dossier 'rapports' créé : {dossier_rapports}")
    
    return dossier_rapports


def formater_top5_erreurs(top5_erreurs):
    
    erreurs_formatees = []
    
    for message, occurrences in top5_erreurs:
        erreurs_formatees.append({
            "message": message,
            "occurrences": occurrences
        })
    
    return erreurs_formatees


def generer_rapport(statistiques, liste_fichiers, dossier_source):
    
    # Récupération du chemin de base du projet
    chemin_base = recuperer_chemin_base()
    
    # Création du dossier rapports 
    dossier_rapports = creer_dossier_rapports(chemin_base)
    
    # Génération de la date et heure actuelle
    date_creation = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_fichier = datetime.now().strftime("%Y-%m-%d")
    
    # Récupération des métadonnées système
    utilisateur = os.environ.get('USERNAME') or os.environ.get('USER') or "Utilisateur_Inconnu"
    
    # Détection du système d'exploitation
    systeme = sys.platform
    if systeme.startswith('win'):
        nom_systeme = "Windows"
    elif systeme.startswith('linux'):
        nom_systeme = "Linux"
    elif systeme.startswith('darwin'):
        nom_systeme = "macOS"
    else:
        nom_systeme = systeme
    
    # Conversion du chemin source en absolu
    chemin_source_absolu = os.path.abspath(dossier_source)
    
    # Construction de la structure JSON
    rapport = {
        "metadata": {
            "date": date_creation,
            "utilisateur": utilisateur,
            "os": nom_systeme,
            "source": chemin_source_absolu
        },
        "statistiques": {
            "total_lignes": statistiques.get("total_lignes", 0),
            "par_niveau": statistiques.get("niveaux", {"ERROR": 0, "WARN": 0, "INFO": 0}),
            "top5_erreurs": formater_top5_erreurs(statistiques.get("top_5", []))
        },
        "fichiers_traites": liste_fichiers
    }
    
    # Nom du fichier de rapport
    nom_fichier = f"rapport_{date_fichier}.json"
    chemin_fichier = os.path.join(dossier_rapports, nom_fichier)
    
    # Écriture du fichier JSON
    try:
        with open(chemin_fichier, 'w', encoding='utf-8') as fichier:
            json.dump(rapport, fichier, indent=4, ensure_ascii=False)
        print(f"Rapport JSON généré : {chemin_fichier}")
    except IOError as e:
        print(f"Erreur lors de l'écriture du rapport : {e}")
        raise
    
    return chemin_fichier


#TEST
if __name__ == "__main__":
    # Test avec des données simulées
    print("=== Test du module rapport.py ===\n")
    
    # Données de test
    statistiques_test = {
        "total_lignes": 150,
        "niveaux": {
            "ERROR": 12,
            "WARN": 8,
            "INFO": 130
        },
        "top_5": [
            ("Échec de la connexion au serveur LDAP", 5),
            ("Timeout de la base de données", 3),
            ("Échec de l'authentification", 2),
            ("Fichier de configuration manquant", 1),
            ("Permission refusée", 1)
        ]
    }
    
    fichiers_test = [
        "c:/Users/DELL/Documents/logAnalyzerPro/logs_test/app1.log",
        "c:/Users/DELL/Documents/logAnalyzerPro/logs_test/app2.log",
        "c:/Users/DELL/Documents/logAnalyzerPro/logs_test/app3.log"
    ]
    
    source_test = "logs_test"
    
    # Génération du rapport de test
    try:
        chemin_rapport = generer_rapport(statistiques_test, fichiers_test, source_test)
        print(f"\n Rapport créé avec succès : {chemin_rapport}")
        
        # Lecture et affichage du contenu
        print("\n--- Contenu du rapport ---")
        with open(chemin_rapport, 'r', encoding='utf-8') as f:
            print(f.read())
            
    except Exception as e:
        print(f" Erreur : {e}")
