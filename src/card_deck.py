import random

class CardDeck:
    def __init__(self):
        self.cards = [f"{rank}{suit}" for suit in 'SHDC' for rank in '23456789TJQKA']
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
