"""
Modèle de données pour une carte Magic
"""

from dataclasses import dataclass, asdict


@dataclass
class MagicCard:
    """Représentation d'une carte Magic Cardmarket"""
    
    name: str
    card_set: str
    condition: str
    language: str
    comments: str
    price: str
    quantity: str
    is_altered: bool = False
    is_foil: bool = False
    is_signed: bool = False
    
    def to_dict(self) -> dict:
        """Convertit la carte en dictionnaire"""
        return asdict(self)
    
    def to_csv_row(self) -> dict:
        """Convertit la carte en ligne CSV avec tous les champs"""
        return {
            'Name': self.name,
            'Set': self.card_set,
            'Condition': self.condition,
            'Language': self.language,
            'Comments': self.comments,
            'Price': self.price,
            'Number': self.quantity,
            'Altered': 'True' if self.is_altered else 'False',
            'Foil': 'True' if self.is_foil else 'False',
            'Signed': 'True' if self.is_signed else 'False',
        }
    
    @classmethod
    def csv_fieldnames(cls) -> list:
        """Retourne les noms des colonnes CSV"""
        return [
            'Name', 'Set', 'Condition', 'Language', 'Comments', 
            'Price', 'Number', 'Altered', 'Foil', 'Signed'
        ]
