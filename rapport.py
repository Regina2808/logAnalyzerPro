#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime


def generer_rapport(stats, meta, source):
    
    """
    Rôle: Transforme les resultats de l'analyse en un fichier structuré au format JSON.

    """
    # Determination du chemin absolu du dossier de stockage des rapports
    base = os.path.dirname(os.path.abspath(__file__))

    dossier_rapports = os.path.join(base, "rapports")

    # Creation automatique du dossier 'rapports' s'il n'existe pas encore
    os.makedirs(dossier_rapports, exist_ok=True)

    # Generation d'un nom de fichier unique basé sur l'heure exacte
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    nom_fichier_json = f"rapport_{date_str}.json"

    chemin = os.path.join(dossier_rapports, nom_fichier_json)

    # Construction de la structure de données finale
    structure_rapport = {
        "metadata": {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "utilisateur": meta["utilisateur"],
            "os": meta["os"],
            "source": source
        },
        "statistiques": {
            "total_lignes": stats["total_lignes"],
            "par_niveau": stats["niveaux"],
            "top5_erreurs": stats["top_5"]
        },
        "fichiers_traites": stats["fichiers"]
    }

    try:
        # Ecriture des donnees dans le fichier avec une indentation propre pour la lisibilité
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(structure_rapport, f, indent=4, ensure_ascii=False)

        print(f"Rapport genere avec succes : {nom_fichier_json}")
        return chemin
    
    except Exception as e:
        print(f"Erreur lors de la generation du fichier JSON : {e}")
        return None