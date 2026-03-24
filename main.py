#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

# Importation des fonctions developpées dans les autres modules
from analyser import (
    configurer_arguments,
    recuperer_metadonnees,
    lister_fichiers_logs,
    analyser_fichiers,
)

from rapport import generer_rapport

from archiver import (
    verifier_espace,
    archiver_logs,
    nettoyer_rapports,
)


def main():
    
    """
    Fonction principale qui permet :
    1. Recuperation des arguments et metadonnees.
    2. Analyse des logs et calcul des statistiques.
    3. Generation du rapport JSON.
    4. Archivage des sources et nettoyage des anciens fichiers.
    
    """

    try:
        # 1. Recuperation des paramètres saisis par l'utilisateur en ligne de commande
        args = configurer_arguments()
        
        source = args.source
        niveau = args.niveau
        dest = args.dest
        retention = args.retention
        
        # 2. Recherche des fichiers logs dans le dossier specifie
        fichiers = lister_fichiers_logs(source)

        if not fichiers:
           print(" Aucun fichier .log trouve dans le dossier source.")
           sys.exit(1)

        # 3. Phase d'analyse 
        print(f"Analyse de {len(fichiers)} fichier(s) en cours...")
        
        stats = analyser_fichiers(fichiers, niveau)

        meta = recuperer_metadonnees()

        # 4. Production du Rapport JSON
        print("Generation du rapport...")
        chemin_rapport = generer_rapport(stats, meta, source)
        
        if chemin_rapport:
            print(f"-> Rapport enregistré : {chemin_rapport}")
        
        # 5. Verification de l'espace disque avant archivage
        print("Verification des ressources du système...")
        if not verifier_espace():
            print("Erreur : Operation interrompue pour proteger le systeme.")
            sys.exit(1)

        # 6. Archivage et Maintenance
        print(f"Compression des logs vers le dossier '{dest}'...")
        archiver_logs(fichiers, dest)

        print(f"Nettoyage des rapports vieux de plus de {retention} jours...")
        nettoyer_rapports(retention)

        print("\n--- Pipeline LogAnalyzer Pro termine avec succes ---")

    except Exception as e:
       print(f"\n[ERREUR CRITIQUE] Le programme a rencontré un problème : {e}")
       sys.exit(1)


if __name__ == "__main__":
    main()