import sys
import os

def main():
    try:
        origine_source = ""
        final_dest = ""
        output_dir = ""
        
        #recuperation des données
        logs = analyser_logs(source, niveau="ALL")
        
        #recuperation chemin vers les rapports 
        rapport = generer_rapport(logs,output_dir)
        
        #achivage 
        archive = archive_logs(source, dest)
        #nettoyage
        delete_anciens_rapports(output_dir, retention_days=30)
        
        print(f"Rapport généré: {rapport}")
        print(f"Archive créer {archive}")
        print(f"Nettoyage des anciens rapports terminés")
except Exception as e:
    print(f"Erreur fatale: {e}")
    sys.exit(1)
    
    if __name__ == "__main__":
        main()           
        
        
        
        
        
        
        
