"""
Gestion des exports CSV pour les cartes Magic
"""

import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


class CSVExporter:
    """Exporte les cartes dans un fichier CSV"""
    
    def __init__(self, output_dir: str = 'output'):
        """
        Initialise l'exporteur CSV
        
        Args:
            output_dir: Répertoire de sortie
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def export(self, cards: List, filename: str = None) -> str:
        """
        Exporte les cartes dans un fichier CSV
        
        Args:
            cards: Liste des cartes MagicCard
            filename: Nom du fichier (généré automatiquement si None)
        
        Returns:
            Chemin du fichier créé
        """
        if not cards:
            logger.warning("⚠️  Aucune carte à exporter")
            return None
        
        # Générer le nom du fichier si nécessaire
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'cards_export_{timestamp}.csv'
        
        filepath = self.output_dir / filename
        
        try:
            # Utiliser le modèle pour obtenir les noms de colonnes
            fieldnames = cards[0].csv_fieldnames()
            
            with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for card in cards:
                    writer.writerow(card.to_csv_row())
            
            logger.info(f"✓ Export réussi: {filepath}")
            logger.info(f"  📊 {len(cards)} cartes exportées")
            
            return str(filepath)
        
        except Exception as e:
            logger.error(f"✗ Erreur lors de l'export: {e}")
            raise
