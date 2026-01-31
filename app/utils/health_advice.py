
def get_health_advice(data):
    """
    Analyse les constantes vitales et retourne des conseils.
    data: dictionnaire {'glycemie': float, 'tension': float, 'poids': float, 'poids_precedent': float}
    """
    advice_list = []
    has_alert = False

    # 1. Glycémie
    # Seuil : 1.26 g/L (ou 126 mg/dL)
    glyc = data.get('glycemie')
    if glyc is not None:
        # Normalisation simple : si > 10, on suppose mg/dL, sinon g/L
        is_high = (glyc > 126) if glyc > 10 else (glyc > 1.26)
        
        if is_high:
            has_alert = True
            advice_list.append({
                'type': 'glycemie',
                'title': 'Glycémie',
                'color_class': 'orange-500',
                'bg_class': 'bg-orange-50',
                'border_class': 'border-l-orange-500',
                'text_class': 'text-orange-900',
                'icon': 'candy',
                'message': "Glycémie élevée, évitez les sucres rapides.",
                'to_avoid': ['Sodas & Jus', 'Pâtisseries', 'Pain blanc'],
                'to_favor': ['Légumes fibres', 'Eau', 'Céréales complètes']
            })

    # 2. Tension
    # Seuil : 14 (cmHg) ou 140 (mmHg)
    tens = data.get('tension')
    if tens is not None:
        # Normalisation : si > 30, on suppose mmHg
        is_high = (tens > 140) if tens > 30 else (tens > 14)
        
        if is_high:
            has_alert = True
            advice_list.append({
                'type': 'tension',
                'title': 'Tension',
                'color_class': 'rose-500',
                'bg_class': 'bg-rose-50',
                'border_class': 'border-l-rose-500',
                'text_class': 'text-rose-900',
                'icon': 'activity',
                'message': "Tension haute, surveillez votre consommation de sel.",
                'to_avoid': ['Sel de table', 'Charcuteries', 'Plats préparés'],
                'to_favor': ['Fruits & Légumes', 'Potassium', 'Activités calmes']
            })

    # 3. Poids
    # Seuil : +0.5 kg par rapport au précédent
    poids = data.get('poids')
    poids_prev = data.get('poids_precedent')
    
    if poids is not None and poids_prev is not None:
        diff = poids - poids_prev
        if diff > 0.5:
            has_alert = True
            advice_list.append({
                'type': 'poids',
                'title': 'Poids',
                'color_class': 'blue-500',
                'bg_class': 'bg-blue-50',
                'border_class': 'border-l-blue-500',
                'text_class': 'text-blue-900',
                'icon': 'scale',
                'message': f"Légère prise de poids (+{diff:.1f}kg).",
                'to_avoid': ['Grignotage', 'Plats gras', 'Sédentarité'],
                'to_favor': ['Marche active', 'Protéines magres', 'Repas fixes']
            })

    # 4. Si tout est OK (aucune alerte)
    if not has_alert and (glyc is not None or tens is not None or poids is not None):
        advice_list.append({
            'type': 'general',
            'title': 'Bilan Santé',
            'color_class': 'emerald-500',
            'bg_class': 'bg-emerald-50',
            'border_class': 'border-l-emerald-500',
            'text_class': 'text-emerald-900',
            'icon': 'check-circle-2',
            'message': "Constantes stables, continuez ainsi !",
            'to_avoid': [],
            'to_favor': []
        })

    return advice_list
