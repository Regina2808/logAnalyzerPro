#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

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

    try:

        args = configurer_arguments()

        source = args.source
        niveau = args.niveau
        dest = args.dest
        retention = args.retention

        fichiers = lister_fichiers_logs(source)

        if not fichiers:
            print("Aucun log trouvé")
            sys.exit(1)

        stats = analyser_fichiers(fichiers, niveau)

        meta = recuperer_metadonnees()

        print("Rapport...")
        generer_rapport(stats, meta, source)

        print("Espace disque...")
        if not verifier_espace():
            sys.exit(1)

        print("Archive...")
        archiver_logs(fichiers, dest)

        print("Nettoyage...")
        nettoyer_rapports(retention)

        print("Terminé")

    except Exception as e:
        print("Erreur:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()