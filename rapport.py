import json
import os
from datetime import datetime

def generer_rapport(stats, meta, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rapport = {
        "metadata": {
            "date": date_str,
            "utilisateur": meta["utilisateur"],
            "os": meta["os"],
            "source": stats.get("source", "")
        },
        "statistiques": {
            "total_lignes": stats["total_lignes"],
            "par_niveau": stats["niveaux"],
            "top5_erreurs": stats["top_5"]
        },
        "fichiers_traites": stats.get("fichiers_traites", [])
    }

    filename = f"rapport_{datetime.now().strftime('%Y-%m-%d')}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(rapport, f, indent=4, ensure_ascii=False)

    return filepath