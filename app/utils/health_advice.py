from app.i18n import t


def get_health_advice(data):
    """
    Analyse vital signs and return translated health tips.
    data: dict with optional keys: 'glycemie', 'tension', 'poids', 'poids_precedent'
    """
    advice_list = []
    has_alert = False

    # Blood sugar — threshold: 126 mg/dL (or 1.26 g/L)
    glyc = data.get('glycemie')
    if glyc is not None:
        is_high = (glyc > 126) if glyc > 10 else (glyc > 1.26)
        if is_high:
            has_alert = True
            advice_list.append({
                'type': 'glycemie',
                'title': t('advice_sugar_title'),
                'color_class': 'orange-500',
                'bg_class': 'bg-orange-50',
                'border_class': 'border-l-orange-500',
                'text_class': 'text-orange-900',
                'icon': 'candy',
                'message': t('advice_sugar_msg'),
                'to_avoid': [t('advice_sugar_avoid_0'), t('advice_sugar_avoid_1'), t('advice_sugar_avoid_2')],
                'to_favor': [t('advice_sugar_favor_0'), t('advice_sugar_favor_1'), t('advice_sugar_favor_2')],
            })

    # Blood pressure — threshold: 140 mmHg (or 14 cmHg)
    tens = data.get('tension')
    if tens is not None:
        is_high = (tens > 140) if tens > 30 else (tens > 14)
        if is_high:
            has_alert = True
            advice_list.append({
                'type': 'tension',
                'title': t('advice_bp_title'),
                'color_class': 'rose-500',
                'bg_class': 'bg-rose-50',
                'border_class': 'border-l-rose-500',
                'text_class': 'text-rose-900',
                'icon': 'activity',
                'message': t('advice_bp_msg'),
                'to_avoid': [t('advice_bp_avoid_0'), t('advice_bp_avoid_1'), t('advice_bp_avoid_2')],
                'to_favor': [t('advice_bp_favor_0'), t('advice_bp_favor_1'), t('advice_bp_favor_2')],
            })

    # Weight — alert on gain > 0.5 kg since last reading
    poids = data.get('poids')
    poids_prev = data.get('poids_precedent')
    if poids is not None and poids_prev is not None:
        diff = poids - poids_prev
        if diff > 0.5:
            has_alert = True
            advice_list.append({
                'type': 'poids',
                'title': t('advice_weight_title'),
                'color_class': 'blue-500',
                'bg_class': 'bg-blue-50',
                'border_class': 'border-l-blue-500',
                'text_class': 'text-blue-900',
                'icon': 'scale',
                'message': t('advice_weight_msg').format(diff=f'{diff:.1f}'),
                'to_avoid': [t('advice_weight_avoid_0'), t('advice_weight_avoid_1'), t('advice_weight_avoid_2')],
                'to_favor': [t('advice_weight_favor_0'), t('advice_weight_favor_1'), t('advice_weight_favor_2')],
            })

    # All clear
    if not has_alert and (glyc is not None or tens is not None or poids is not None):
        advice_list.append({
            'type': 'general',
            'title': t('advice_ok_title'),
            'color_class': 'emerald-500',
            'bg_class': 'bg-emerald-50',
            'border_class': 'border-l-emerald-500',
            'text_class': 'text-emerald-900',
            'icon': 'check-circle-2',
            'message': t('advice_ok_msg'),
            'to_avoid': [],
            'to_favor': [],
        })

    return advice_list
