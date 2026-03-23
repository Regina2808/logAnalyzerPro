import sys 
import os 
from analyser import recuperer_metadonnees,configurer_arguments,lister_fichiers_logs,analyser_fichiers
from archiver import verifier_espace_disque, creer_archive_logs,nettoyer_rapports
from rapport import generer_rapport 

def main():
    try:
        # recuperation des différents
        args = configurer_arguments
        source = args.source
        niveau = args.niveau
            
        log = "tests/logs"
        backup = "tests/backups"
        rapport = "tests/rapports"
    
        # creation des dossiers si elle n'existais pas 
        os.mkdir(log, exist_ok=True)
        os.mkdir(rapport, exist_ok=True)
        os.mkdir(backup, exist_ok=True) 
        
        #listé les fichiers logs 
        
        fichier = lister_fichiers_logs(source) 
        if not fichier: 
            print("Aucun fichier log trouvé.")
            sys.exit(1)
        # analyse des fichiers    
        resultats = analyser_fichiers(source, niveau)
        meta_data = recuperer_metadonnees()
        
        #génération du rapport json 
        rapport_path = generer_rapport(resultats,meta_data)
        print(f"Rapport généré:{rapport_path}")
        
        #vérification de l"espace disque 
        verifier_espace_disque
        #créer archive
        creer_archive_logs()
        #nettoyage des anciens rapports
        nettoyer_rapports()
        
        
    except Exception as e:
        print(f"Erreur fatale: {e}")
        sys.exit(1)
    if __name__ == "__main__":
        main()    
        
    
     
    
    
    