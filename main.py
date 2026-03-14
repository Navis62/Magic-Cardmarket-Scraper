"""
Lanceur interactif - Magic Cardmarket Scraper avec Login MANUEL

Nouvelle structure organisée:
- src/scraper/     : Logique de scraping
- src/models/      : Modèles de données (MagicCard)
- src/utils/       : Utilitaires (CSV, sélecteurs)
- output/          : Fichiers CSV générés
"""

import logging
import sys
from pathlib import Path

# Ajouter le répertoire src au chemin
sys.path.insert(0, str(Path(__file__).parent))

from src.scraper import CardmarketScraper
from src.utils import CSVExporter

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def display_menu():
    """Affiche le menu principal"""
    print("\n" + "="*70)
    print("🎭 MAGIC CARDMARKET SCRAPER - LOGIN MANUEL")
    print("="*70)
    print("""
📋 Menu:
1. Scraper avec login manuel
2. Quitter
    """)


def scrape_inventory():
    """Lance le scraper d'inventaire"""
    try:
        # Initialiser le scraper
        scraper = CardmarketScraper(headless=False)
        
        # Connexion manuelle
        if not scraper.manual_login():
            logger.warning("❌ Connexion annulée")
            scraper.close()
            return
        
        # Demander l'URL
        print("\n" + "-"*70)
        url = input("🔗 Entrez l'URL de votre inventaire Cardmarket:\n> ").strip()
        
        if not url:
            logger.warning("❌ URL vide")
            scraper.close()
            return
        
        # S'assurer que l'URL a le bon format
        if not url.startswith('http'):
            url = 'https://' + url
        
        # Ajouter &site=1 si pas présent
        if '&site=' not in url and '?site=' not in url:
            separator = '&' if '?' in url else '?'
            url = url + separator + 'site=1'
        
        logger.info(f"✓ URL finale: {url}")
        
        # Demander le nombre de pages
        max_pages_input = input("\n📑 Nombre de pages à scraper (vide = toutes): ").strip()
        max_pages = int(max_pages_input) if max_pages_input else None
        
        # Scraper
        cards = scraper.scrape_all_pages(url, max_pages)
        
        if cards:
            # Exporter en CSV
            exporter = CSVExporter(output_dir='output')
            filepath = exporter.export(cards)
            
            logger.info("\n" + "="*70)
            logger.info("✅ SCRAPING RÉUSSI!")
            logger.info("="*70)
            logger.info(f"📊 {len(cards)} cartes exportées")
            logger.info(f"💾 Fichier: {filepath}")
            
            # Afficher un résumé
            altered_count = sum(1 for c in cards if c.is_altered)
            foil_count = sum(1 for c in cards if c.is_foil)
            signed_count = sum(1 for c in cards if c.is_signed)
            
            if altered_count or foil_count or signed_count:
                logger.info("\n📋 Résumé des variantes:")
                if altered_count:
                    logger.info(f"   🔨 Altérées: {altered_count}")
                if foil_count:
                    logger.info(f"   ✨ Foil: {foil_count}")
                if signed_count:
                    logger.info(f"   ✍️  Signées: {signed_count}")
        
        else:
            logger.warning("⚠️  Aucune carte trouvée")
        
        scraper.close()
    
    except Exception as e:
        logger.error(f"✗ Erreur: {e}")
        if scraper:
            scraper.close()


def main():
    """Fonction principale"""
    while True:
        display_menu()
        
        choice = input("Choisissez (1 ou 2): ").strip()
        
        if choice == "1":
            scrape_inventory()
        
        elif choice == "2":
            logger.info("👋 Au revoir!")
            break
        
        else:
            logger.warning("❌ Choix invalide")


if __name__ == "__main__":
    main()
