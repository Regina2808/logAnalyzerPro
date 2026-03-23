#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os 
import tarfile
import shutil 
import time 
import subprocess 
from datetime import datetime 



def verifier_espace_disque():
    #Vérifie si on a assez de place (100 Mo minimum)
    try:
        total, utilise, libre = shutil.disk_usage(".")
        libre_mo = libre // (1024 * 1024)
        if libre_mo < 100:
            print(f" Erreur : Espace insuffisant ({libre_mo} Mo restants)")
            return False
        print(f"Espace disque vérifié : {libre_mo} Mo disponibles. ")
        return True
    except Exception as e:
        print(f"Erreur vérification disque : {e}")
        return False

def creer_archive_logs(fichiers_a_traiter, dossier_destination):
    #Compresse les logs et les déplace dans le dossier backups
    date_str = datetime.now().strftime("%Y-%m-%d")
    nom_archive = f"backup_{date_str}.tar.gz"
    try:
        with tarfile.open(nom_archive, "w:gz") as tar:
            for f in fichiers_a_traiter:
                if os.path.exists(f):
                    tar.add(f, arcname=os.path.basename(f))
        
        if not os.path.exists(dossier_destination):
            os.makedirs(dossier_destination)
            
        chemin_final = os.path.join(dossier_destination, nom_archive)
        shutil.move(nom_archive, chemin_final)
        print(f" Archive créée avec succès : {chemin_final}")
        return True
    except Exception as e:
        print(f" Erreur lors de l'archivage : {e}")
        return False

def nettoyer_rapports(dossier_rapports, jours_retention=30):
    #Supprime les fichiers .json de plus de N jours
    maintenant = time.time()
    limite_secondes = jours_retention * 24 * 60 * 60
    try:
        if not os.path.exists(dossier_rapports):
            return
        for fichier in os.listdir(dossier_rapports):
            if fichier.endswith(".json"):
                chemin_complet = os.path.join(dossier_rapports, fichier)
                if (maintenant - os.path.getmtime(chemin_complet)) > limite_secondes:
                    os.remove(chemin_complet)
                    print(f" Nettoyage : {fichier} supprimé.")
    except Exception as e:
        print(f"Erreur nettoyage : {e}")



def executer_archivage_complet(liste_logs):
    
    #Fonction appelée par main.py
    # Définition des chemins absolus
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # On sort de loganalyzer pour trouver les dossiers à la racine
    dossier_backups = os.path.normpath(os.path.join(base_dir, "..", "backups"))
    dossier_rapports = os.path.normpath(os.path.join(base_dir, "..", "rapports"))

    print("--- ARCHIVAGE ---")
    if verifier_espace_disque():
        creer_archive_logs(liste_logs, dossier_backups)
        nettoyer_rapports(dossier_rapports, jours_retention=30)
        print("--- verification avec succès ---")
        return True
    return False


if __name__ == "__main__":
    # test de la fonction principale
    executer_archivage_complet([])