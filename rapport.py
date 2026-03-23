import json
import os
from datetime import datetime

def generer_rapport(data, output_dir):
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rapport = {
        "metadata": {
            "date": date_str,
            "utilisateur": data["metadata"]["utilisateur"],
            "os": data["metadata"]["os"],
            "source": data["metadata"]["source"],
        },
        "statistiques": data["statistiques"],
        "fichiers_traites": data["fichiers_traites"],
    }

    filename = f"rapport_{datetime.now().strftime('%Y-%m-%d')}.json"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(rapport, f, indent=4, ensure_ascii=False)

    return filepath
