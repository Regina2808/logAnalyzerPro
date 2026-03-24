#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import glob
import platform
from collections import Counter


def configurer_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--source", required=True)
    parser.add_argument(
        "--niveau",
        default="ALL",
        choices=["INFO", "WARN", "ERROR", "ALL"]
    )

    parser.add_argument("--dest", default="backups")
    parser.add_argument("--retention", type=int, default=30)

    return parser.parse_args()


def recuperer_metadonnees():

    utilisateur = os.environ.get("USER") or os.environ.get("USERNAME")

    systeme = platform.system()

    return {
        "utilisateur": utilisateur,
        "os": systeme
    }


def lister_fichiers_logs(source):

    base = os.path.dirname(os.path.abspath(__file__))

    dossier = os.path.join(base, source)

    if not os.path.exists(dossier):
        print("Dossier introuvable")
        exit(1)

    pattern = os.path.join(dossier, "*.log")

    return glob.glob(pattern)


def analyser_fichiers(fichiers, niveau_filtre):

    total = 0

    niveaux = {
        "INFO": 0,
        "WARN": 0,
        "ERROR": 0
    }

    erreurs = []

    for fichier in fichiers:

        with open(fichier, "r", encoding="utf-8") as f:

            for ligne in f:

                total += 1

                parts = ligne.strip().split()

                if len(parts) < 3:
                    continue

                level = parts[2]

                if niveau_filtre != "ALL" and level != niveau_filtre:
                    continue

                if level in niveaux:
                    niveaux[level] += 1

                if level == "ERROR":
                    message = " ".join(parts[3:])
                    erreurs.append(message)

    top5 = Counter(erreurs).most_common(5)

    return {
        "total_lignes": total,
        "niveaux": niveaux,
        "top_5": top5,
        "fichiers": fichiers
    }