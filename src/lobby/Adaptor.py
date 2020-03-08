from src.game.card import Card


def deserialize_card(data: dict) -> Card:
    card_type = data['type']
    index = data['index']
    value = data['value']
    color = data['color']

    return Card(color, card_type, value, index)


def serialize_card(card: Card) -> dict:
    return {
        'type': card.type,
        'value': card.value,
        'color': card.value,
        'index': card.index
    }
