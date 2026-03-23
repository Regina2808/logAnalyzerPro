#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Pour manipuler les chemins et supprimer des fichiers
import os  
# Pour créer l'archive .tar.gz       
import tarfile
 # Pour déplacer des fichiers proprement   
import shutil 
 # Pour calculer l'âge des fichiers   
import time  
# Pour interroger le système    
import subprocess 
# Pour mettre la date sur l'archive
from datetime import datetime 



def verifier_espace_disque():
    """Vérifie si on a assez de place (100 Mo minimum)"""
    try:
        # Utilisation de shutil pour obtenir l'espace disque 
        total, utilise, libre = shutil.disk_usage(".")
        # Conversion en MégaOctets
        libre_mo = libre // (1024 * 1024)
        
        if libre_mo < 100:
            print(f" Erreur : Espace insuffisant ({libre_mo} Mo restants)")
            return False
        return True
    except Exception as e:
        print(f"Erreur vérification disque : {e}")
        return False

def creer_archive_logs(fichiers_a_traiter, dossier_destination):
    """Compresse les logs et les déplace dans le dossier backups"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    nom_archive = f"backup_{date_str}.tar.gz"
    #Utilisation de tarfile (le mode 'w:gz' = écrire + compresser)
    
    try:
        with tarfile.open(nom_archive, "w:gz") as tar:
            for f in fichiers_a_traiter:
                if os.path.exists(f):
                    tar.add(f, arcname=os.path.basename(f))
       # Déplacer l'archive vers backups
        if not os.path.exists(dossier_destination):
            os.makedirs(dossier_destination)
            
        chemin_final = os.path.join(dossier_destination, nom_archive)
        shutil.move(nom_archive, chemin_final)
        
        print(f" Archive créée avec succès : {chemin_final}")
        return True
    except Exception as e:
        print(f"Erreur lors de l'archivage : {e}")
        return False

def nettoyer_rapports(dossier_rapports, jours_retention=30):
    """Supprime les fichiers .json de plus de N jours"""
    maintenant = time.time()
    # 30 jours convertis en secondes
    limite_secondes = jours_retention * 24 * 60 * 60
    
    try:
        # On vérifie si le dossier existe avant de scanner
        if not os.path.exists(dossier_rapports):
            print(f"Info : Le dossier {dossier_rapports} n'existe pas encore.")
            return

        for fichier in os.listdir(dossier_rapports):
            if fichier.endswith(".json"):
                chemin_complet = os.path.join(dossier_rapports, fichier)
                # On récupère la date de modification du fichier
                age_fichier = os.path.getmtime(chemin_complet)
                
                
                if (maintenant - age_fichier) > limite_secondes:
                    os.remove(chemin_complet)
                    print(f"🧹 Nettoyage : {fichier} supprimé (trop vieux)")
    except Exception as e:
        print(f"Erreur nettoyage : {e}")


if __name__ == "__main__":
    print("--- Test du Module 3 (Archivage) ---")
    
    # Définition des chemins absolus
    base_dir = os.path.dirname(os.path.abspath(__file__))

    dossier_backups = os.path.normpath(os.path.join(base_dir, "..", "backups"))
    dossier_rapports = os.path.normpath(os.path.join(base_dir, "..", "rapports"))

    if verifier_espace_disque():
        print(" Espace disque suffisant.")
        # Simulation avec une liste vide
        creer_archive_logs([], dossier_backups)
        nettoyer_rapports(dossier_rapports, jours_retention=30)
        print("--- Fin du test ---")