import unittest
from src.ai import AIPlayer
from src.card_deck import CardDeck
from src.game_rules import GameRules

class TestAIPlayer(unittest.TestCase):
    def test_ai_player_action(self):
        player = AIPlayer("AI Player")
        community_cards = [('D', 'T'), ('D', '8'), ('H', 'Q')]
        pot = 100
        bb = 10
        last_bet = 20
        min_raise = 20

        action, amount = player.decide_action(community_cards, pot, bb, last_bet, min_raise)
        self.assertIn(action, ['fold', 'check', 'call', 'bet', 'raise'])
        if action == 'bet':
            self.assertTrue(amount >= bb)
            self.assertTrue(amount % (bb // 2) == 0)
        elif action == 'raise':
            self.assertTrue(amount >= last_bet + min_raise)
            self.assertTrue(amount % (bb // 2) == 0)
        elif action == 'all-in':
            self.assertEqual(amount, player.stack)

if __name__ == '__main__':
    unittest.main()
