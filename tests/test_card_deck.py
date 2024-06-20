import unittest
from src.card_deck import CardDeck

class TestCardDeck(unittest.TestCase):
    def test_shuffle(self):
        # デッキの初期化とシャッフルをテスト
        deck = CardDeck()
        self.assertEqual(len(deck.cards), 52)

    def test_deal_card(self):
        # カードを配る機能をテスト
        deck = CardDeck()
        card = deck.deal_card()
        self.assertEqual(len(deck.cards), 51)
        self.assertIn(card, [f"{rank}{suit}" for suit in 'SHDC' for rank in '23456789TJQKA'])

if __name__ == '__main__':
    unittest.main()
