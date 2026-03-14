# 🚀 DÉMARRAGE RAPIDE

## Installation & Lancement (2 minutes)

```bash
# 1️⃣  Activer l'environnement (optionnel, déjà créé)
.venv\Scripts\activate

# 2️⃣  Lancer le scraper
python main.py

# 3️⃣  Sélectionner option 1 dans le menu
# 4️⃣  Se connecter manuellement quand le navigateur s'ouvre
# 5️⃣  Fournir l'URL de votre inventaire Cardmarket
# 6️⃣  Attendre le scraping
# 7️⃣  ✅ Fichier CSV généré dans output/
```

## 📁 Structure du Projet (ACTUALISÉE 13/03/2026)

```
src/
├── scraper/           → Logique de scraping
│   ├── cardmarket.py  → Classe CardmarketScraper
│   └── extractor.py   → Classe CardExtractor
├── models/            → Modèles de données
│   └── card.py        → Classe MagicCard (dataclass)
└── utils/             → Utilitaires
    ├── csv_exporter.py → Export CSV
    └── selectors.py   → Sélecteurs CSS

output/                → Fichiers CSV générés
main.py               → Point d'entrée ⭐
```

## ✨ Nouvelles Fonctionnalités

### 1️⃣ Booléens pour Variations
```python
card.is_altered = True/False  # Altérée
card.is_foil = True/False     # Foil/Brillante
card.is_signed = True/False   # Signée
```

Détection automatique dans les commentaires avec mots-clés.

### 2️⃣ Pagination avec &site=X
L'URL est automatiquement enrichie:
- `https://example.com/inventory` → `https://example.com/inventory?site=1`

### 3️⃣ Structure Organisée
- **Avant**: 40+ fichiers mélangés
- **Après**: 6 fichiers + structure modulaire

## 📊 Colonnes CSV (10)

```
Name | Set | Condition | Language | Comments | Price | Number | Altered | Foil | Signed
```

## 🧪 Tests

```bash
# Vérifier que la structure fonctionne
python test_structure.py
```

Tous les tests doivent passer ✅

## 📚 Documentation

- **README.md** - Documentation complète
- **CLEANUP.md** - Détails du nettoyage
- **RAPPORT_NETTOYAGE.py** - Rapport avec stats

## ⚠️ Point Important

Le projet est maintenant **PROPRE** :
- ❌ Plus 30+ fichiers obsolètes supprimés
- ✅ Structure modulaire et claire
- ✅ Code réutilisable et maintenable
- ✅ Prêt pour la production

**Lancer le scraper avec confidence !** 🎉
