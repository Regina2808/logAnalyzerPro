#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tarfile
import shutil
import time
from datetime import datetime


def verifier_espace():

    total, used, free = shutil.disk_usage(".")

    free_mb = free // (1024 * 1024)

    if free_mb < 100:
        print("Espace disque insuffisant")
        return False

    return True


def archiver_logs(fichiers, dest):

    base = os.path.dirname(os.path.abspath(__file__))

    dossier = os.path.join(base, dest)

    os.makedirs(dossier, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    archive = f"backup_{date_str}.tar.gz"

    archive_path = os.path.join(base, archive)

    with tarfile.open(archive_path, "w:gz") as tar:

        for f in fichiers:
            tar.add(f)

    shutil.move(archive_path, dossier)


def nettoyer_rapports(retention):

    base = os.path.dirname(os.path.abspath(__file__))

    dossier = os.path.join(base, "rapports")

    now = time.time()

    for f in os.listdir(dossier):

        if not f.endswith(".json"):
            continue

        path = os.path.join(dossier, f)

        age = now - os.path.getmtime(path)

        jours = age / 86400

        if jours > retention:
            os.remove(path)