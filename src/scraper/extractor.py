"""
Module d'extraction des cartes Cardmarket avec Selenium et BeautifulSoup
"""

import logging
from typing import List
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from ..models.card import MagicCard
from ..utils.selectors import CSS_SELECTORS

logger = logging.getLogger(__name__)


class CardExtractor:
    """Extrait les cartes des pages Cardmarket"""
    
    @staticmethod
    def extract_cards_from_page(driver) -> List[MagicCard]:
        """
        Extrait les cartes de la page actuelle
        
        Args:
            driver: Webdriver Selenium
        
        Returns:
            Liste des cartes MagicCard
        """
        try:
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            
            cards = []
            articles = soup.find_all('div', class_='row g-0 article-row')
            
            if not articles:
                logger.warning("⚠️  Aucune carte trouvée")
                return cards
            
            logger.info(f"📍 {len(articles)} carte(s) trouvée(s)")
            
            for article in articles:
                try:
                    card = CardExtractor._extract_single_card(article)
                    if card:
                        cards.append(card)
                        logger.debug(
                            f"  ✓ {card.name} | {card.card_set} | "
                            f"{card.condition} | {card.quantity} | "
                            f"{'[A]' if card.is_altered else ''}"
                            f"{'[F]' if card.is_foil else ''}"
                            f"{'[S]' if card.is_signed else ''}"
                        )
                
                except Exception as e:
                    logger.debug(f"  ✗ Erreur extraction: {e}")
                    continue
            
            return cards
        
        except Exception as e:
            logger.error(f"✗ Erreur lors de l'extraction: {e}")
            return []
    
    @staticmethod
    def _extract_single_card(article) -> MagicCard:
        """
        Extrait une seule carte
        
        Args:
            article: Élément BeautifulSoup de la ligne de carte
        
        Returns:
            Objet MagicCard ou None
        """
        # Nom - .col-seller > a
        name_element = article.select_one('.col-seller a')
        name = name_element.get_text(strip=True) if name_element else "N/A"
        
        # Set - a.expansion-symbol avec data-bs-original-title
        set_element = article.select_one('a.expansion-symbol')
        card_set = set_element.get('data-bs-original-title', 'N/A') if set_element else "N/A"
        
        # Condition - span.badge
        condition_element = article.select_one('span.badge')
        condition = condition_element.get_text(strip=True) if condition_element else 'N/A'
        
        # Langue - chercher span avec data-bs-original-title (langue, pas rareté)
        language = 'N/A'
        lang_spans = article.select('span[data-bs-original-title]')
        for span in lang_spans:
            label = span.get('data-bs-original-title', '')
            if label and label not in ['Rare', 'Uncommon', 'Common', 'Mythic', 'Special']:
                language = label
                break
        
        # Rareté - svg.me-2 avec data-bs-original-title
        rarity = 'N/A'
        rarity_element = article.select_one('svg.me-2[data-bs-original-title]')
        if rarity_element:
            rarity = rarity_element.get('data-bs-original-title', 'N/A')
        
        # Commentaires - product-comments span
        comments_element = article.select_one('.product-comments span')
        comments = comments_element.get_text(strip=True) if comments_element else ''
        
        # Prix - .price-container span.color-primary
        price_element = article.select_one('.price-container .color-primary')
        price = price_element.get_text(strip=True) if price_element else 'N/A'
        
        # Quantité - .amount-container .item-count
        qty_element = article.select_one('.amount-container .item-count')
        quantity = qty_element.get_text(strip=True) if qty_element else 'N/A'
        
        # Détecter les propriétés spéciales via data-bs-original-title exact
        special_titles = {
            span.get('data-bs-original-title', '')
            for span in article.select('span[data-bs-original-title]')
        }
        is_foil = 'Foil' in special_titles
        is_altered = bool(special_titles & {'Altérée', 'Altered'})
        is_signed = bool(special_titles & {'Signé', 'Signed'})
        
        return MagicCard(
            name=name,
            card_set=card_set,
            condition=condition,
            language=language,
            comments=comments,
            price=price,
            quantity=quantity,
            rarity=rarity,
            is_altered=is_altered,
            is_foil=is_foil,
            is_signed=is_signed
        )
