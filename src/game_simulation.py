import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from card_deck import CardDeck
from game_rules import GameRules

class Player:
    def __init__(self, name):
        self.name = name
        self.hole_cards = []

def simulate_game():
    # プレイヤーの作成
    players = [Player("Player 1"), Player("Player 2")]

    # デッキの準備
    deck = CardDeck()

    # 各プレイヤーに2枚のホールカードを配布
    for player in players:
        player.hole_cards = [deck.deal_card(), deck.deal_card()]
        print(f"{player.name} hole cards: {player.hole_cards}")

    # プリフロップ（既にホールカードが配布されている）
    print("\n-- Pre-flop --")

    # フロップの配布（コミュニティカード3枚）
    community_cards = GameRules.deal_community_cards(deck, 3)
    print(f"Community cards: {community_cards}")

    # ターンの配布（コミュニティカード1枚追加）
    community_cards += GameRules.deal_community_cards(deck, 1)
    print("\n-- Turn --")
    print(f"Community cards: {community_cards}")

    # リバーの配布（コミュニティカード1枚追加）
    community_cards += GameRules.deal_community_cards(deck, 1)
    print("\n-- River --")
    print(f"Community cards: {community_cards}")

    # ショーダウン（勝者の決定）
    winners = GameRules.determine_winner(players, community_cards)
    if len(winners) == 1:
        print(f"\nWinner: {winners[0].name}")
    else:
        print("\nDraw between:")
        for winner in winners:
            print(winner.name)

if __name__ == "__main__":
    simulate_game()
