#!/usr/bin/env python 3

"""
Module 1: Ingestion et Analyse (analyser.py)

Rôle:
• Accepter les arguments CLI suivants via argparse : – --source : chemin vers le dossier contenant les fichiers logs (obligatoire) – --niveau : niveau de filtrage parmi ERROR, WARN, INFO, ALL (défaut : ALL) 
• Scanner tous les fichiers .log du dossier source avec glob 
• Lire chaque fichier ligne par ligne et filtrer selon le niveau demandé 
• Calculer les statistiques suivantes : – Nombre total de lignes analysées – Comptage par niveau (ERROR, WARN, INFO) – Top 5 des messages ERROR les plus fréquents 
• Détecter l'OS courant (platform) et l'utilisateur (os.environ) pour les métadonnées

"""

import os
import sys
import argparse
import glob
from pathlib import Path

def recuperer_metadonnees():
    # Récupère le nom de l'utilisateur et le système d'exploitation courant

    # 1- Récupération du nom de l'utilisateur
    utilisateur = os.environ.get('USERNAME') or " Utilisateur Inconnu"

    # 2- Récupération du système d'exploitation courant
    systeme = sys.platform

    
    if systeme.startswith('win'):
        nom_systeme = "Windows"
    elif systeme.startswith('linux'):
        nom_systeme = "Linux"
    elif systeme.startswith('darwin'):
        nom_systeme = "macOS"
    else:
         nom_systeme = systeme
    
    return{
        "utilisateur": utilisateur,
        "os": nom_systeme
    }

def configurer_arguments():
    # Configure les arguments de la ligne de commande

    parser = argparse.ArgumentParser(description = "LogAnalyserPro - Module d'Analyse")

    # Le dossier source: chemin vers le dossier contenant les fichiers logs
    parser.add_argument("--source", required=True, help="Chemin vers le dossier des logs")

    # Le niveau: niveau de filtrage des logs parmi ERROR, WARN, INFO, ALL (défaut : ALL) 
    parser.add_argument("--niveau", default="ALL", 
                        choices=["INFO", "WARN", "ERROR", "ALL"], 
                        help="Niveau de filtrage des logs")
    
    return parser.parse_args()

def lister_fichiers_logs(dossier_source):
    # Liste tous les fichiers .log dans le dossier spécifié

    # Récupération du dossier actuel
    dossier_actuel = Path.cwd()

    # Transformation en chemin absolu
    chemin_complet = os.path.join(dossier_actuel, dossier_source)

    # Vérification de l'existence du dossier
    if not os.path.exists(chemin_complet):
        print(f"Erreur: Le dossier '{dossier_source}' est introuvable")
        sys.exit(1)

    # Création de la recherche
    filtre_log = os.path.join(chemin_complet, "*.log")
    liste_fichiers = glob.glob(filtre_log)

    if not liste_fichiers:
        print(f"Attention: Aucun fichier .log trouvé dans {chemin_complet}")

    return liste_fichiers

def analyser_fichiers(liste_fichiers, niveau_filtre):
    # Rôle: Lit les fichiers ligne par ligne et extrait les statistiques

    # Initialisation des compteurs
    statistiques = {
        "total_lignes": 0,
        "niveaux": {"INFO": 0, "WARN": 0, "ERROR": 0},
        "erreurs_frequentes": {} # Pour le top 5 des messages ERROR
    }

    for fichier in liste_fichiers:
        # Ouverture du fichier en mode lecture 'r'
        with open(fichier, 'r', encoding='utf-8') as file:
            for ligne in file:
                statistiques["total_lignes"] += 1

                # On nettoie la ligne pour l'analyser
                ligne = ligne.strip()

                # Vérification du niveau de la ligne
                for niveau in ["INFO", "WARN", "ERROR"]:
                    if niveau in ligne:
                        statistiques["niveaux"][niveau] += 1

                        # Si c'est une ERROR, on stocke le message pour le Top 5
                        if niveau == "ERROR":
                            # On découpe pour ne garder que le message après "ERROR"
                            parties = ligne.split("ERROR:")

                            if len(parties)> 1:
                                message = parties[1].strip()
                                statistiques["erreurs_frequentes"][message] = statistiques["erreurs_frequentes"].get(message,0) + 1
    
    # Top 5 des erreurs

    # Récupération de toutes les erreurs
    total_erreurs = statistiques["erreurs_frequentes"]

    # On trie par le nombre du plus grand au plus petit
    erreurs_triés = sorted(total_erreurs.items(), key=lambda x: x[1], reverse=True)

    # On ne garde que les cinq premières
    statistiques["top_5"] = erreurs_triés[:5]

    return statistiques
    
# --- ZONE DE TEST ---
if __name__ == "__main__":
    args = configurer_arguments()
    meta = recuperer_metadonnees()
    fichiers = lister_fichiers_logs(args.source)
    
    # Nouvelle étape : Analyse
    resultats = analyser_fichiers(fichiers, args.niveau)
    
    print(f"\n=== Résultats pour {meta['utilisateur']} ===")
    print(f"Lignes totales analysées : {resultats['total_lignes']}")
    print(f"Répartition : {resultats['niveaux']}")

    print("\n--- TOP 5 DES ERREURS ---")
    for msg, count in resultats["top_5"]:
        print(f"- {msg} : {count} fois")