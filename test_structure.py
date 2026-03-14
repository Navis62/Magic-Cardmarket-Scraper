"""
Script de test pour vérifier la structure et les imports
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au chemin
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Teste les imports principaux"""
    print("🧪 Test des imports...")
    print("-" * 70)
    
    try:
        print("📦 Import src.models.MagicCard...", end=" ")
        from src.models import MagicCard
        print("✓")
        
        print("📦 Import src.utils.CSVExporter...", end=" ")
        from src.utils import CSVExporter
        print("✓")
        
        print("📦 Import src.scraper.CardmarketScraper...", end=" ")
        from src.scraper import CardmarketScraper
        print("✓")
        
        print("📦 Import src.scraper.CardExtractor...", end=" ")
        from src.scraper import CardExtractor
        print("✓")
        
        print("\n✅ Tous les imports sont OK!")
        return True
    
    except ImportError as e:
        print(f"\n❌ Erreur d'import: {e}")
        return False


def test_magic_card_model():
    """Teste le modèle MagicCard"""
    print("\n🧪 Test du modèle MagicCard...")
    print("-" * 70)
    
    try:
        from src.models import MagicCard
        
        # Créer une carte de test
        card = MagicCard(
            name="Aladdin's Ring",
            card_set="Foreign Black Bordered",
            condition="NM",
            language="French",
            comments="Foil",
            price="12,00 €",
            quantity="1",
            is_foil=True
        )
        
        print(f"✓ Carte créée: {card.name}")
        print(f"  - Set: {card.card_set}")
        print(f"  - Condition: {card.condition}")
        print(f"  - Foil: {card.is_foil}")
        
        # Test conversion en dict
        csv_row = card.to_csv_row()
        print(f"\n✓ Conversion en ligne CSV:")
        for key, value in csv_row.items():
            print(f"  - {key}: {value}")
        
        # Test fieldnames
        fieldnames = MagicCard.csv_fieldnames()
        print(f"\n✓ Colonnes CSV: {len(fieldnames)}")
        print(f"  {fieldnames}")
        
        print("\n✅ Test MagicCard OK!")
        return True
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_csv_exporter():
    """Teste l'exporteur CSV"""
    print("\n🧪 Test du CSVExporter...")
    print("-" * 70)
    
    try:
        from src.models import MagicCard
        from src.utils import CSVExporter
        
        # Créer des cartes de test
        cards = [
            MagicCard(
                name="Aladdin's Ring",
                card_set="Foreign Black Bordered",
                condition="NM",
                language="French",
                comments="",
                price="12,00 €",
                quantity="1"
            ),
            MagicCard(
                name="Black Lotus",
                card_set="Limited Edition",
                condition="VG",
                language="English",
                comments="Foil",
                price="1500,00 €",
                quantity="1",
                is_foil=True,
                is_altered=True
            )
        ]
        
        # Exporter
        exporter = CSVExporter(output_dir='output')
        filepath = exporter.export(cards, filename='test_export.csv')
        
        print(f"✓ Export réussi: {filepath}")
        
        # Vérifier le fichier
        if Path(filepath).exists():
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                lines = f.readlines()
                print(f"✓ Fichier créé avec {len(lines)} lignes (header + données)")
        
        print("✅ Test CSVExporter OK!")
        return True
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_selectors():
    """Teste les sélecteurs CSS"""
    print("\n🧪 Test des sélecteurs CSS...")
    print("-" * 70)
    
    try:
        from src.utils.selectors import CSS_SELECTORS, ALTERED_KEYWORDS, FOIL_KEYWORDS, SIGNED_KEYWORDS
        
        print("✓ Sélecteurs CSS chargés:")
        for key, value in CSS_SELECTORS.items():
            if isinstance(value, tuple):
                print(f"  - {key}: {value[0]}.{value[1]}")
            else:
                print(f"  - {key}: {value}")
        
        print(f"\n✓ Mots-clés détection:")
        print(f"  - Altérée: {ALTERED_KEYWORDS}")
        print(f"  - Foil: {FOIL_KEYWORDS}")
        print(f"  - Signée: {SIGNED_KEYWORDS}")
        
        print("\n✅ Test sélecteurs OK!")
        return True
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def main():
    """Lance tous les tests"""
    print("\n" + "="*70)
    print("🧪 TESTS DE STRUCTURE - MAGIC CARDMARKET SCRAPER")
    print("="*70)
    
    tests = [
        ("Imports", test_imports),
        ("Modèle MagicCard", test_magic_card_model),
        ("CSVExporter", test_csv_exporter),
        ("Sélecteurs CSS", test_selectors),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Erreur critique: {e}")
            results.append((name, False))
    
    # Résumé
    print("\n" + "="*70)
    print("📊 RÉSUMÉ")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print("-" * 70)
    print(f"✅ {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS! Le projet est prêt!")
    else:
        print(f"\n⚠️  {total - passed} test(s) échoué(s)")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
