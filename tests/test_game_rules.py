import unittest
from src.game_rules import GameRules

class TestGameRules(unittest.TestCase):
    def test_evaluate_hand(self):
        hand = [('A', 'S'), ('A', 'H'), ('A', 'D'), ('A', 'C'), ('K', 'S')]
        self.assertEqual(GameRules.evaluate_hand(hand), ('Four of a Kind', 'AK'))

    def test_process_bet(self):
        player_stack, pot = GameRules.process_bet('bet', 50, 1000, 200)
        self.assertEqual(player_stack, 950)
        self.assertEqual(pot, 250)

    def test_determine_winner(self):
        player1 = type('Player', (object,), {'hole_cards': [('A', 'S'), ('A', 'H')]})
        player2 = type('Player', (object,), {'hole_cards': [('K', 'S'), ('K', 'H')]})
        community_cards = [('A', 'D'), ('A', 'C'), ('2', 'S'), ('3', 'H'), ('4', 'D')]
        players = [player1, player2]
        winners = GameRules.determine_winner(players, community_cards)
        self.assertEqual(winners, [player1])

if __name__ == '__main__':
    unittest.main()
