import sys 
import os 
from analyser import recuperer_metadonnees,configurer_arguments,lister_fichiers_logs,analyser_fichiers
from archiver import verifier_espace_disque, creer_archive_logs,nettoyer_rapports
from rapport import generer_rapport 

def main():
    try:
        # recuperation des différents
        args = configurer_arguments()
        source = args.source
        niveau = args.niveau
            
        log_dir = "tests/logs"
        backup_dir = "tests/backups"
        rapport_dir = "tests/reports"
    
        # creation des dossiers si elle n'existais pas 
        os.makedirs(log_dir, exist_ok=True)
        os.makedirs(rapport_dir, exist_ok=True)
        os.makedirs(backup_dir, exist_ok=True) 
        
        #listé les fichiers logs 
        
        fichier_logs = lister_fichiers_logs(source) 
        if not fichier_logs: 
            print("Aucun fichier log trouvé.")
            sys.exit(1)
        # analyse des fichiers    
        resultats = analyser_fichiers(fichier_logs, niveau)
        metadata = recuperer_metadonnees()
        
        #génération du rapport json 
        rapport_path = generer_rapport(resultats,metadata, rapport_dir)
        print(f"Rapport généré:{rapport_path}")
        
        #vérification de l"espace disque 
        if not verifier_espace_disque():
            print(f"Espace disque insufissant pour la créaction du fichier d'archive")
            sys.exit(1)
        #créer archive
        archive_path=creer_archive_logs(fichier_logs,backup_dir)
        print(f"Archive crée avec succes: {archive_path}")
        #nettoyage des anciens rapports
        nettoyer_rapports(rapport_dir, jours_retention=30)
        print(f" Nettoyage des anciens rapports terminé avec succés")
        
        
    except Exception as e:
        print(f"Erreur fatale: {e}")
        sys.exit(1)
if __name__ == "__main__":
    main()    
        
    
     
    
    
    