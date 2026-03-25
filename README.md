# LogAnalyzer Pro

## 📌 Description

LogAnalyzer Pro est un outil en ligne de commande développé en Python permettant d’analyser des fichiers de logs, de générer des rapports JSON, d’archiver les fichiers traités et de nettoyer automatiquement les anciens rapports.

---

## 🎯 Objectif

L’objectif du projet est de concevoir un outil capable de :

* Analyser automatiquement des fichiers de logs applicatifs
* Extraire des informations selon leur niveau de criticité (INFO, WARN, ERROR)
* Générer un rapport structuré au format JSON
* Archiver les fichiers traités
* Nettoyer les anciens rapports
* Permettre une exécution automatique via Cron

---

## ⚙️ Prérequis

* Python 3.x
* Aucune bibliothèque externe requise

---

## 💻 Installation

```bash
git clone https://github.com/votre-repo/loganalyzer-pro.git
cd loganalyzer-pro
```

---

## 📁 Structure du projet

```
loganalyzer/
├── main.py               # Point d'entrée principal
├── analyser.py           # Module 1 : Ingestion et analyse
├── rapport.py            # Module 2 : Génération du rapport JSON
├── archiver.py           # Module 3 : Archivage et nettoyage
├── logs_test/            # Fichiers de logs pour les tests
│   ├── app1.log
│   ├── app2.log
│   └── app3.log
├── rapports/             # Dossier généré automatiquement
├── backups/              # Dossier généré automatiquement
└── README.md             # Documentation technique
```

---

## ▶️ Utilisation

### Commande principale

```bash
python main.py --source logs_test --niveau ERROR --dest backups --retention 30
```

### Arguments disponibles

| Argument      | Description                                            |
| ------------- | ------------------------------------------------------ |
| `--source`    | Dossier contenant les fichiers `.log` (obligatoire)    |
| `--niveau`    | ERROR, WARN, INFO, ALL (défaut : ALL)                  |
| `--dest`      | Dossier de destination pour les archives               |
| `--retention` | Nombre de jours avant suppression des anciens rapports |

---

## 🧩 Modules

### 🔹 analyser.py

* Lecture des fichiers `.log`
* Filtrage des lignes selon le niveau
* Calcul des statistiques :

  * Total des lignes
  * Nombre par niveau
  * Top 5 erreurs

---

### 🔹 rapport.py

* Génération du fichier JSON
* Structuration des données
* Ajout des métadonnées (date, utilisateur, OS)

---

### 🔹 archiver.py

* Compression des fichiers logs (`.tar.gz`)
* Déplacement des archives
* Suppression des anciens rapports

---

### 🔹 main.py

* Coordination de tous les modules
* Gestion des erreurs
* Exécution globale du programme

---

## ⏰ Planification (Cron)

```bash
0 3 * * 0 /usr/bin/python3 /chemin/vers/loganalyzer/main.py --source /chemin/logs --dest /chemin/backups --retention 30
```

### Explication

* `0 3` → à 03h00
* `* *` → tous les jours et tous les mois
* `0` → dimanche

---

## 👥 Répartition des tâches

| Personne   | Module                | Tâches détaillées                                                                                                                |
| ---------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| AWADJIHE Régina | analyser.py           | Lire les fichiers `.log`, filtrer selon INFO/WARN/ERROR, calculer toutes les statistiques, gérer les arguments CLI avec argparse |
| ANAGONOU Richard | rapport.py            | Créer le fichier JSON, organiser les données correctement, ajouter les métadonnées (date, utilisateur, OS)                       |
| AGBODO Fiacresse | archiver.py           | Créer l’archive `.tar.gz`, déplacer les fichiers, supprimer les anciens rapports selon la durée                                  |
| DAYE KANLINSOU Gildas | main.py               | Relier tous les modules, gérer les erreurs, contrôler l’exécution complète                                                       |
| KORE Ange | Tests & Documentation | Créer les fichiers de test, tester tout le projet, détecter les bugs, rédiger README et configurer Cron                          |

---

## 🧪 Données de Test

Pour vos tests, créez un dossier `logs_test/` contenant au minimum **3 fichiers `.log`** simulant des logs applicatifs réels.

Chaque fichier doit contenir des lignes respectant le format suivant :

### Format

```
YYYY-MM-DD HH:MM:SS  NIVEAU  Message
```
## 🕐 Cron

Execution chaque dimanche à 03h

0 3 * * 0 /usr/bin/python3 /home/ackerman/loganalyzer/main.py --source /home/ackerman/loganalyzer/logs_test --dest /home/ackerman/loganalyzer/backups --retention 30


### Exemple

```
2024-04-01 08:22:30  ERROR  Échec de la connexion au serveur LDAP
2024-04-01 08:30:00  INFO   Tâche planifiée de nettoyage démarrée
2024-04-01 09:00:01  WARN   Utilisation CPU supérieure à 85%
```

Chaque fichier doit contenir au moins **20 lignes** avec un mélange de INFO, WARN et ERROR.

---

## 📌 Remarque

* Tous les chemins doivent être absolus
* Le code doit être commenté
* Chaque fonction doit avoir une docstring
* Le programme ne doit jamais planter sans message d’erreur clair

---

## 📌 Projet académique

Projet réalisé en groupe dans le cadre académique.
