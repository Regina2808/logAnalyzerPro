#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tarfile
import shutil
import time
from datetime import datetime


def verifier_espace():
    """
    Rôle: Verifie si l'espace disque disponible sur le lecteur courant est suffisant.

    """
    
    total, used, free = shutil.disk_usage(".")

    # Conversion des octets en Mega-octets (Mo)
    free_mb = free // (1024 * 1024)

    if free_mb < 100:
        print(f"Erreur : Espace disque insuffisant ({free_mb} Mo restants).")
        return False

    return True


def archiver_logs(fichiers, dest):

    """
    Rôle: Compresse une liste de fichiers logs dans une archive .tar.gz et 
    la deplace vers le dossier de destination.

    """

    # Determination du repertoire de base via le script courant
    base = os.path.dirname(os.path.abspath(__file__))

    dossier_destination = os.path.join(base, dest)

    # Creation du dossier de backups s'il n'existe pas
    os.makedirs(dossier_destination, exist_ok=True)

    # Generation du nom de l'archive avec horodatage
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    nom_archive = f"backup_{date_str}.tar.gz"

    archive_path = os.path.join(base, nom_archive)

    try:

        # Creation de l'archive
        with tarfile.open(archive_path, "w:gz") as tar:

            for f in fichiers:
                if os.path.exists(f):
                    # On ajoute le fichier en gardant uniquement son nom
                    tar.add(f, arcname=os.path.basename(f))

        # Deplacement de l'archive vers le dossier final
        shutil.move(archive_path, dossier_destination)
        print(f"Succes : Archive creee dans {dossier_destination}")
    
    except Exception as e:
        print(f"Erreur lors de l'archivage : {e}")


def nettoyer_rapports(retention):

    """
    Rôle: Supprime les anciens rapports JSON qui depassent le delai de retention.

    """

    base = os.path.dirname(os.path.abspath(__file__))

    dossier_rapports = os.path.join(base, "rapports")

    # Si le dossier n'existe pas, on arrete la fonction
    if not os.path.exists(dossier_rapports):
        return

    now = time.time()

    try:
        for fichier in os.listdir(dossier_rapports):

            if not fichier.endswith(".json"):
                continue

            path = os.path.join(dossier_rapports, fichier)

            # Calcul de l'age du fichier en secondes
            age_secondes = now - os.path.getmtime(path)

            age_jours = age_secondes / 86400

            if age_jours > retention:
                os.remove(path)
                print(f"Nettoyage : Rapport obsolete supprime ({fichier}).")
    except Exception as e:
        print(f"Erreur lors du nettoyage : {e}")