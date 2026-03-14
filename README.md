# Magic Cardmarket Scraper - Structure Réorganisée

## 📁 Nouvelle Structure du Projet

```
Scraper/
├── src/
│   ├── __init__.py
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── cardmarket.py       # Classe principale CardmarketScraper
│   │   └── extractor.py        # Extraction des cartes (CardExtractor)
│   ├── models/
│   │   ├── __init__.py
│   │   └── card.py             # Modèle MagicCard (dataclass)
│   └── utils/
│       ├── __init__.py
│       ├── csv_exporter.py     # Export CSV (CSVExporter)
│       └── selectors.py        # Sélecteurs CSS et mots-clés
├── output/
│   └── *.csv                   # Fichiers générés
├── main.py                     # Point d'entrée principal
├── requirements.txt            # Dépendances Python
└── README.md                   # Ce fichier
```

## 🚀 Utilisation

### Installation

```bash
# Créer l'environnement virtuel
python -m venv .venv

# Activer l'environnement
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt
```

### Lancer le scraper

```bash
python main.py
```

## 📦 Modules

### `src.scraper.CardmarketScraper`
Classe principale du scraper
- `manual_login()` : Connexion manuelle via navigateur
- `load_page(url)` : Charge une page
- `scrape_all_pages(url, max_pages)` : Scrape plusieurs pages avec pagination `&site=X`
- `go_to_next_page()` : Navigate vers la page suivante

### `src.scraper.CardExtractor`
Extraction des cartes individuelles
- `extract_cards_from_page(driver)` : Extrait toutes les cartes d'une page
- `_extract_single_card(article)` : Extrait une carte unique

### `src.models.MagicCard`
Modèle dataclass d'une carte Magic
```python
@dataclass
class MagicCard:
    name: str           # Nom de la carte
    card_set: str       # Ensemble/Édition
    condition: str      # NM, EX, GD, LP, PL, PO
    language: str       # Langue
    comments: str       # Commentaires
    price: str          # Prix
    quantity: str       # Quantité
    is_altered: bool    # Carte altérée?
    is_foil: bool       # Foil/Brillante?
    is_signed: bool     # Signée?
```

### `src.utils.CSVExporter`
Export en CSV avec tous les champs
- `export(cards, filename)` : Exporte vers fichier CSV

## 🔄 Flux d'Exécution

```
main.py
  ↓
  Affiche menu
  ↓
  Utilisateur choisit option 1 (scraper)
  ↓
  CardmarketScraper.manual_login()
    → Ouvre navigateur
    → Utilisateur se connecte manuellement
    → Valide dans terminal
  ↓
  Demande URL + nombre de pages
  ↓
  Ajoute automatiquement &site=1 si absent
  ↓
  CardmarketScraper.scrape_all_pages()
    ↓
    Pour chaque page:
      ↓
      CardExtractor.extract_cards_from_page()
        ↓
        Pour chaque article:
          ↓
          MagicCard créée avec tous les champs
          ↓
          Détecte is_altered, is_foil, is_signed
  ↓
  CSVExporter.export()
    → Crée fichier dans output/
    → Colonnes: Name, Set, Condition, Language, Comments, Price, Number, Altered, Foil, Signed
  ↓
  Affiche résumé + chemin fichier
```

## ✨ Nouvelles Fonctionnalités

### 1. Détection Automatique des Variations
Détecte dans les commentaires:
- **Altérée**: mots-clés = `['altérée', 'altered', 'alter', 'playset']`
- **Foil**: mots-clés = `['foil', 'brillante']`
- **Signée**: mots-clés = `['signé', 'signed', 'signature']`

Résultats en colonnes CSV:
- `Altered`: "Oui" ou "Non"
- `Foil`: "Oui" ou "Non"
- `Signed`: "Oui" ou "Non"

### 2. Pagination Automatique avec &site=X
- L'URL est automatiquement enrichie de `&site=1`
- Permet une navigation correcte entre les pages
- Paramètre modifié automatiquement pour chaque page suivante

### 3. Organisation Modulaire
- Séparation claire des responsabilités
- Code réutilisable et testable
- Facile d'ajouter de nouvelles fonctionnalités

## 📊 Exemple de Sortie CSV

```csv
Name,Set,Condition,Language,Comments,Price,Number,Altered,Foil,Signed
Aladdin's Ring,Foreign Black Bordered,NM,French,,12,00 €,1,Non,Non,Non
Black Lotus,Limited Edition,VG,English,Slightly played,1500,00 €,1,Oui,Non,Non
Ancestral Vision,Time Spiral,NM,French,Foil,11,80 €,1,Non,Oui,Non
Ancient Tomb,Tempest,EX,German,Signé par l'auteur,45,00 €,1,Non,Non,Oui
```

## 🛠️ Développement Futur

Facile à ajouter:
- [ ] Export en d'autres formats (Excel, JSON)
- [ ] Filtrage avancé (par condition, prix, etc.)
- [ ] Sauvegarde en base de données
- [ ] Interface graphique
- [ ] Notifications de changement de prix
- [ ] Historique des prix

## ⚙️ Configuration

Modifier les mots-clés de détection dans `src/utils/selectors.py`:

```python
ALTERED_KEYWORDS = ['altérée', 'altered', 'alter', 'playset']
FOIL_KEYWORDS = ['foil', 'brillante']
SIGNED_KEYWORDS = ['signé', 'signed', 'signature']
```

## 📝 Logs

Les logs incluent:
- ✓ Cartes trouvées
- ✓ Extraction avec variations `[A] [F] [S]`
- ✓ Total par page
- ✓ Résumé final avec comptage des variantes

Exemple:
```
✓ Aladdin's Ring | Foreign Black Bordered | NM | 1
✓ Black Lotus | Limited Edition | VG | 1 | [A] [F]
✓ Ancestral Vision | Time Spiral | NM | 1 | [F]
```

## 🔧 Troubleshooting

### Aucune carte trouvée
- Vérifier l'URL
- Vérifier la connexion
- Les sélecteurs CSS peuvent être changés (Cardmarket peut avoir mis à jour le HTML)

### Erreur de connexion
- S'assurer que 2FA n'interfère pas
- Augmenter le délai d'attente si nécessaire

### Valeurs N/A
- Les sélecteurs CSS doivent être mis à jour
- Lancer `test_selectors.py` pour vérifier

---

**Version:** 2.0 (Réorganisée avec modules)
**Date:** 13/03/2026
