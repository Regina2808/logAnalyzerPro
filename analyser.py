#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import glob
import platform
from collections import Counter


def configurer_arguments():
    """
    Rôle: Configure et recupere les arguments de la ligne de commande 
    """
    parser = argparse.ArgumentParser(description="LogAnalyzer Pro - Module d'Analyse")

    parser.add_argument("--source", required=True, help="Chemin vers le dossier des logs")
    parser.add_argument(
        "--niveau",
        default="ALL",
        choices=["INFO", "WARN", "ERROR", "ALL"],
        help="Niveau de filtrage des logs"
    )

    parser.add_argument("--dest", default="backups", help="Dossier de destination des archives")
    parser.add_argument("--retention", type=int, default=30, help="Nombre de jours de retention")

    return parser.parse_args()


def recuperer_metadonnees():
    """
    Rôle: Detecte les informations du systeme et l'utilisateur courant.
    
    """
    utilisateur = os.environ.get("USER") or os.environ.get("USERNAME")

    systeme = platform.system()

    return {
        "utilisateur": utilisateur,
        "os": systeme
    }


def lister_fichiers_logs(source):
    """
    Rôle: Scanne le dossier source pour lister les fichiers se terminant par .log.
    Utilise des chemins absolus pour garantir la robustesse.
    
    """
    # On recupere le dossier courant
    base = os.path.dirname((__file__))

    # On construit le chemin vers les logs
    dossier = os.path.join(base, source)

    if not os.path.exists(dossier):
        print(f"Erreur : Le dossier '{dossier}' est introuvable.")
        exit(1)

    critere_recherche = os.path.join(dossier, "*.log")

    return glob.glob(critere_recherche)


def analyser_fichiers(fichiers, niveau_filtre):
    """
    Rôle: Parcourt chaque fichier ligne par ligne pour extraire les statistiques 
    et filtrer selon le niveau.

    """
    total = 0

    niveaux = {
        "INFO": 0,
        "WARN": 0,
        "ERROR": 0
    }

    erreurs = []

    for fichier in fichiers:
        try:

            with open(fichier, "r", encoding="utf-8") as f:

                for ligne in f:

                    total += 1

                    parts = ligne.strip().split()

                    # On verifie si la ligne contient au moins la date, l'heure et le niveau
                    if len(parts) < 3:
                        continue

                    level = parts[2]

                    if niveau_filtre != "ALL" and level != niveau_filtre:
                        continue

                    if level in niveaux:
                        niveaux[level] += 1

                    # Si c'est une erreur, on extrait le message
                    if level == "ERROR":
                        message = " ".join(parts[3:])
                        erreurs.append(message)
        except Exception as e:
            print(f"Attention : Impossible de lire {fichier}. Erreur : {e}")

    # Extraction des 5 erreurs les plus frequentes
    top_5_erreurs = Counter(erreurs).most_common(5)

    return {
        "total_lignes": total,
        "niveaux": niveaux,
        "top_5": top_5_erreurs,
        "fichiers": fichiers
    }