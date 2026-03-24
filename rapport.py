#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime


def generer_rapport(stats, meta, source):

    base = os.path.dirname(os.path.abspath(__file__))

    dossier = os.path.join(base, "rapports")

    os.makedirs(dossier, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    nom = f"rapport_{date_str}.json"

    chemin = os.path.join(dossier, nom)

    contenu = {
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

    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(contenu, f, indent=4, ensure_ascii=False)

    return chemin