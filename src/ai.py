import random
from src.card_deck import CardDeck
from src.game_rules import GameRules

class AIPlayer:
    def __init__(self, name):
        self.name = name
        self.hole_cards = []
        self.stack = 1000  # プレイヤーの初期スタック

    def evaluate_hand_strength(self, community_cards):
        # 簡単なハンド評価（後で改善）
        hand = self.hole_cards + community_cards
        rank, _ = GameRules.evaluate_hand(hand)
        return rank

    def decide_action(self, community_cards, pot, bb, last_bet, min_raise):
        hand_strength = self.evaluate_hand_strength(community_cards)
        actions = ['fold', 'check', 'call', 'bet', 'raise']
        
        if hand_strength in ['High Card', 'One Pair']:
            action = 'fold' if random.random() < 0.5 else 'call'
        elif hand_strength in ['Two Pair', 'Three of a Kind']:
            action = 'call' if random.random() < 0.7 else 'raise'
        else:
            action = 'raise'

        amount = 0

        if action == 'bet':
            amount = random.randint(bb, self.stack)
            amount = max(bb, amount - amount % (bb // 2))  # BBの0.5倍刻みに丸める

        elif action == 'raise':
            min_amount = last_bet + min_raise
            if min_amount > self.stack:
                action = 'all-in'
                amount = self.stack
            else:
                amount = random.randint(min_amount, self.stack)
                amount = max(min_amount, amount - amount % (bb // 2))  # BBの0.5倍刻みに丸める

        elif action == 'all-in':
            amount = self.stack

        return action, amount

def simulate_game_with_ai():
    # プレイヤーの作成
    players = [AIPlayer("AI Player 1"), AIPlayer("AI Player 2")]

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

    # 各ラウンドでAIプレイヤーのアクションをシミュレート
    pot = 0
    bb = 10  # ビッグブラインド
    last_bet = 0
    min_raise = bb

    for player in players:
        action, amount = player.decide_action(community_cards, pot, bb, last_bet, min_raise)
        print(f"{player.name} decided to {action} with amount {amount}")
        if action in ['bet', 'raise', 'all-in']:
            pot += amount
            last_bet = amount
            min_raise = last_bet

    # ショーダウン（勝者の決定）
    winners = GameRules.determine_winner(players, community_cards)
    if len(winners) == 1:
        print(f"\nWinner: {winners[0].name}")
    else:
        print("\nDraw between:")
        for winner in winners:
            print(winner.name)

if __name__ == "__main__":
    simulate_game_with_ai()
