def get_temperature(city: str) -> str:
    '''Get the current weather in a given city.'''
    if city.lower() == 'san francisco': return '72'
    elif city.lower() == 'paris': return '75'
    elif city.lower() == 'tokyo': return '73'
    return '70'
