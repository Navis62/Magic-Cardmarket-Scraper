"""
Modèle de données pour une carte Magic
"""

from dataclasses import dataclass, asdict
import re


LANGUAGE_ALIASES = {
    "S-Chinese": "Chinese Simplified",
    "T-Chinese": "Chinese Traditional"
}

EXPANSION_ALIASES = {
    "Foreign Black Bordered": "Foreign Black Border",
    "Unlimited": "Unlimited Edition",
    "Ravnica Remastered: Extras": "Ravnica Remastered",
    "Alpha": "Limited Edition Alpha",
    "Beta": "Limited Edition Beta",
    "Legends Italian": "Legends",
    "Fourth Edition: Black Bordered": "Fourth Edition Foreign Black Border",
    "Chronicles: Japanese": "Chronicles Foreign Black Border",
    "MagicFest Promos": "Secret Lair Promo",
    "MagicCon Products": "Secret Lair Drop",
    "Secrets of Strixhaven: Mystical Archive": "Secrets of Strixhaven Mystical Archive",
    "Strixhaven: Mystical Archive": "Strixhaven Mystical Archive"
}

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
    rarity: str = 'N/A'
    is_altered: bool = False
    is_foil: bool = False
    is_signed: bool = False
    
    def to_dict(self) -> dict:
        """Convertit la carte en dictionnaire"""
        return asdict(self)
    
    def _normalize_name(self) -> str:
        return re.sub(r' \(V\.\d+\)$', '', self.name)

    def _normalize_expansion(self) -> str:
        if self.rarity == "Time Shifted":
            return "Time Spiral Timeshifted"
        if self.card_set.startswith("Secret Lair Drop"):
            return "Secret Lair Drop"
        if self.card_set.startswith("Commander: "):
            return self.card_set[len("Commander: "):] + " Commander"
        if self.card_set.endswith(": Promos"):
            return self.card_set[:-len(": Promos")] + " Promos"
        if self.card_set.endswith(": Extras"):
            return self.card_set[:-len(": Extras")]
        return EXPANSION_ALIASES.get(self.card_set, self.card_set)

    def _normalize_language(self) -> str:
        return LANGUAGE_ALIASES.get(self.language, self.language)

    def to_csv_row(self) -> dict:
        """Convertit la carte en ligne CSV avec tous les champs"""
        return {
            'Name': self._normalize_name(),
            'Expansion': self._normalize_expansion(),
            'Condition': 'NM' if self.condition == 'MT' else self.condition,
            'Language': self._normalize_language(),
            'Rarity': self.rarity,
            'Comments': self.comments,
            'Price': self.price,
            'Quantity': self.quantity,
            'Altered': 'Altered' if self.is_altered else 'Non-Altered',
            'Foil': 'Foil' if self.is_foil else 'Non-Foil',
            'Signed': 'Signed' if self.is_signed else 'Non-Signed',
        }
    
    @classmethod
    def csv_fieldnames(cls) -> list:
        """Retourne les noms des colonnes CSV"""
        return [
            'Name', 'Expansion', 'Condition', 'Language', 'Rarity', 'Comments', 
            'Price', 'Quantity', 'Altered', 'Foil', 'Signed'
        ]
