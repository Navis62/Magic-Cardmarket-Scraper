"""
Scraper principal pour Cardmarket avec login manuel
"""

import logging
import time
from typing import List
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import TimeoutException

from .extractor import CardExtractor
from ..models.card import MagicCard

logger = logging.getLogger(__name__)


class CardmarketScraper:
    """Scraper Cardmarket avec login manuel"""
    
    def __init__(self, headless: bool = False):
        """
        Initialise le scraper
        
        Args:
            headless: Mode sans interface
        """
        self.cards: List[MagicCard] = []
        self.driver = None
        self.headless = headless
        self._init_driver()
    
    def _init_driver(self):
        """Initialise le navigateur Chrome"""
        try:
            chrome_options = ChromeOptions()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("✓ Navigateur Chrome initialisé")
        
        except Exception as e:
            logger.error(f"✗ Erreur initialisation Chrome: {e}")
            raise
    
    def manual_login(self) -> bool:
        """
        Ouvre Cardmarket et permet login manuel
        
        Returns:
            True si connexion réussie
        """
        try:
            logger.info("\n" + "="*70)
            logger.info("🔐 CONNEXION MANUELLE")
            logger.info("="*70)
            
            logger.info("📱 Ouverture de Cardmarket...")
            self.driver.get("https://www.cardmarket.com/fr/")
            
            logger.info("\n" + "-"*70)
            logger.info("📋 INSTRUCTIONS:")
            logger.info("-"*70)
            print("""
✨ Le navigateur vient de s'ouvrir!

📝 Étapes:
1. Cherchez le bouton "Connexion" sur la page
2. Cliquez dessus
3. Entrez votre email
4. Entrez votre mot de passe
5. Si 2FA, entrez le code (SMS/Authenticator)
6. Une fois connecté, revenez au terminal

⏳ Quand vous êtes connecté, tapez: C (pour Continuer)
⏹️  Pour annuler: A (pour Annuler)
            """)
            
            logger.info("-"*70)
            
            while True:
                choice = input("\n👉 Êtes-vous connecté? (C=Continuer, F=Forcer, A=Annuler): ").strip().upper()
                
                if choice == "A":
                    logger.info("❌ Connexion annulée par l'utilisateur")
                    return False
                
                if choice == "F":
                    logger.info("✓ Connexion forcée par l'utilisateur (vérification ignorée)")
                    return True
                
                if choice == "C":
                    logger.info("✓ Vérification de la connexion...")
                    time.sleep(2)
                    
                    # Vérifier que l'utilisateur est connecté
                    if self._is_logged_in():
                        logger.info("✓ Connexion vérifiée!")
                        return True
                    else:
                        logger.warning("⚠️  Connexion non détectée automatiquement.")
                        logger.warning("   → Tapez F pour forcer la suite si vous êtes bien connecté.")
        
        except Exception as e:
            logger.error(f"✗ Erreur: {e}")
            return False
    
    def _is_logged_in(self) -> bool:
        """Vérifie si l'utilisateur est connecté"""
        try:
            page_source = self.driver.page_source.lower()
            # Ces mots n'apparaissent que sur une session active
            session_indicators = ['logout', 'log out', 'déconnexion', 'sign out', 'signout']
            return any(ind in page_source for ind in session_indicators)
        except:
            return False
    
    def load_page(self, url: str) -> bool:
        """
        Charge une page
        
        Args:
            url: URL à charger
        
        Returns:
            True si succès
        """
        try:
            logger.info(f"📄 Chargement: {url}")
            self.driver.get(url)
            time.sleep(2)
            return True
        except Exception as e:
            logger.error(f"✗ Erreur chargement page: {e}")
            return False
    
    def go_to_next_page(self) -> bool:
        """
        Navigue vers la page suivante
        
        Returns:
            True s'il y a une page suivante
        """
        try:
            next_button = self.driver.find_element(By.CSS_SELECTOR, 'a[rel="next"]')
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(1)
            next_button.click()
            time.sleep(2)
            return True
        except:
            logger.info("✓ Pas de page suivante")
            return False
    
    @staticmethod
    def _normalize_url_to_english(url: str) -> str:
        """
        S'assure que l'URL utilise la version anglaise du site (/en/).
        Remplace toute autre langue (ex: /fr/, /de/) par /en/.
        """
        import re
        normalized = re.sub(
            r'^(https://www\.cardmarket\.com/)[a-z]{2}(-[a-z]{2})?(/)',
            r'\1en\3',
            url
        )
        if normalized != url:
            logger.info(f"🌐 Langue détectée, redirection vers la version anglaise: {normalized}")
        return normalized

    def _build_paginated_url(self, base_url: str, page: int) -> str:
        """
        Construit l'URL avec le paramètre de pagination site=X
        
        Args:
            base_url: URL de base
            page: Numéro de la page
        
        Returns:
            URL avec pagination
        """
        parsed = urlparse(base_url)
        params = parse_qs(parsed.query)
        
        # Ajouter ou mettre à jour le paramètre site
        params['site'] = [str(page)]
        
        # Reconstruire l'URL
        new_query = urlencode(params, doseq=True)
        new_parsed = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        ))
        
        return new_parsed
    
    def scrape_all_pages(self, start_url: str, max_pages: int = None) -> List[MagicCard]:
        """
        Scrape plusieurs pages avec pagination site=X
        
        Args:
            start_url: URL initiale
            max_pages: Nombre max de pages (None = toutes)
        
        Returns:
            Liste des cartes extraites
        """
        try:
            current_page = 1
            start_url = self._normalize_url_to_english(start_url)
            
            logger.info(f"\n🚀 Début du scraping...")
            logger.info(f"📄 URL: {start_url}")
            if max_pages:
                logger.info(f"📑 Pages max: {max_pages}")
            logger.info("-" * 70)
            
            while True:
                url = self._build_paginated_url(start_url, current_page)
                
                if not self.load_page(url):
                    logger.error(f"✗ Impossible de charger la page {current_page}")
                    break
                
                logger.info(f"\n📄 Page {current_page} → {url}")
                
                # Extraire les cartes de cette page
                page_cards = CardExtractor.extract_cards_from_page(self.driver)
                
                # Aucune carte = fin de la pagination
                if not page_cards:
                    logger.info("✓ Aucune carte sur cette page, fin de la pagination")
                    break
                
                self.cards.extend(page_cards)
                logger.info(f"✓ Total: {len(self.cards)} cartes")
                
                if max_pages and current_page >= max_pages:
                    logger.info(f"✓ Limite de {max_pages} pages atteinte")
                    break
                
                current_page += 1
                time.sleep(1)
            
            logger.info("\n" + "-" * 70)
            logger.info(f"✓ Scraping terminé!")
            logger.info(f"📊 Total: {len(self.cards)} cartes sur {current_page} page(s)")
            
            return self.cards
        
        except Exception as e:
            logger.error(f"✗ Erreur scraping: {e}")
            return []
    
    def close(self):
        """Ferme le navigateur"""
        if self.driver:
            self.driver.quit()
            logger.info("✓ Navigateur fermé")
