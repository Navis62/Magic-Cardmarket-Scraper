"""
Sélecteurs CSS pour extraire les données des cartes Cardmarket
"""

CSS_SELECTORS = {
    'article_row': ('div', 'row g-0 article-row'),
    'name': '.col-seller a',
    'set': 'a.expansion-symbol',
    'condition': 'span.badge',
    'language': 'span[data-bs-original-title]',
    'comments': '.product-comments span',
    'price': '.price-container .color-primary',
    'quantity': '.amount-container .item-count',
    'altered': '.product-comments span',  # À vérifier dans le HTML
    'foil': '.foil-badge',  # À vérifier dans le HTML
    'signed': '.signed-badge',  # À vérifier dans le HTML
}
