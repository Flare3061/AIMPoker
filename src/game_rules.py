from collections import Counter

class GameRules:
    
    @staticmethod
    def evaluate_hand(hand):
        """
        ハンドを評価して、役とそのランクを返す
        """
        ranks = '23456789TJQKA'
        suits = 'SHDC'
        
        # カードのランクとスートを分ける
        rank_counts = Counter(rank for rank, suit in hand)
        suit_counts = Counter(suit for rank, suit in hand)
        sorted_ranks = ''.join(sorted(rank_counts.keys(), key=lambda x: ranks.index(x)))
        
        # 特別なケースとしてA2345のストレートを検出
        if set(rank_counts.keys()) == {'A', '2', '3', '4', '5'}:
            sorted_ranks = '5432A'

        # ストレートの判定
        is_straight = sorted_ranks in ranks or sorted_ranks == '5432A'
        
        # ストレートフラッシュ
        if len(suit_counts) == 1 and is_straight:
            return ('Straight Flush', sorted_ranks)
        
        # フォーカード
        if 4 in rank_counts.values():
            four_of_a_kind = [rank for rank, count in rank_counts.items() if count == 4][0]
            kicker = sorted([rank for rank in rank_counts.keys() if rank != four_of_a_kind], key=lambda x: ranks.index(x), reverse=True)[0]
            return ('Four of a Kind', four_of_a_kind + kicker)
        
        # フルハウス
        if sorted(rank_counts.values()) == [2, 3]:
            three_of_a_kind = [rank for rank, count in rank_counts.items() if count == 3][0]
            pair = [rank for rank, count in rank_counts.items() if count == 2][0]
            return ('Full House', three_of_a_kind + pair)
        
        # フラッシュ
        if len(suit_counts) == 1:
            return ('Flush', ''.join(sorted(rank_counts.keys(), key=lambda x: ranks.index(x), reverse=True)))
        
        # ストレート
        if is_straight:
            return ('Straight', sorted_ranks)
        
        # スリーカード
        if 3 in rank_counts.values():
            three_of_a_kind = [rank for rank, count in rank_counts.items() if count == 3][0]
            kickers = sorted([rank for rank in rank_counts.keys() if rank != three_of_a_kind], key=lambda x: ranks.index(x), reverse=True)[:2]
            return ('Three of a Kind', three_of_a_kind + ''.join(kickers))
        
        # ツーペア
        if list(rank_counts.values()).count(2) == 2:
            pairs = sorted([rank for rank, count in rank_counts.items() if count == 2], key=lambda x: ranks.index(x), reverse=True)
            kicker = sorted([rank for rank in rank_counts.keys() if rank not in pairs], key=lambda x: ranks.index(x), reverse=True)[0]
            return ('Two Pair', ''.join(pairs) + kicker)
        
        # ワンペア
        if 2 in rank_counts.values():
            pair = [rank for rank, count in rank_counts.items() if count == 2][0]
            kickers = sorted([rank for rank in rank_counts.keys() if rank != pair], key=lambda x: ranks.index(x), reverse=True)[:3]
            return ('One Pair', pair + ''.join(kickers))
        
        # ハイカード
        return ('High Card', ''.join(sorted(rank_counts.keys(), key=lambda x: ranks.index(x), reverse=True)))

    @staticmethod
    def process_bet(action, amount, player_stack, pot):
        """
        ベットアクションを処理して、プレイヤースタックとポットを更新する
        """
        if action == 'bet':
            player_stack -= amount
            pot += amount
        elif action == 'call':
            player_stack -= amount
            pot += amount
        elif action == 'raise':
            player_stack -= amount
            pot += amount
        elif action == 'fold':
            pass  # 特に処理なし

        return player_stack, pot

    @staticmethod
    def deal_community_cards(deck, num_cards):
        """
        デッキから指定枚数のコミュニティカードを配る
        """
        return [deck.deal_card() for _ in range(num_cards)]

    @staticmethod
    def determine_winner(players, community_cards):
        """
        ショーダウンでの勝者を決定する。引き分けの場合、複数の勝者を返す。
        """
        best_hands = []
        best_rank = None

        for player in players:
            hand = player.hole_cards + community_cards
            hand_rank, high_card = GameRules.evaluate_hand(hand)
            if best_rank is None or GameRules.compare_hands((hand_rank, high_card), best_rank) > 0:
                best_hands = [player]
                best_rank = (hand_rank, high_card)
            elif GameRules.compare_hands((hand_rank, high_card), best_rank) == 0:
                best_hands.append(player)
        
        return best_hands

    @staticmethod
    def compare_hands(hand1, hand2):
        """
        2つのハンドを比較して、どちらが強いかを返す。
        hand1が強ければ1、hand2が強ければ-1、引き分けなら0を返す。
        """
        hand_ranks = ['High Card', 'One Pair', 'Two Pair', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 'Four of a Kind', 'Straight Flush']
        
        rank1, high_cards1 = hand1
        rank2, high_cards2 = hand2

        # 役の比較
        if hand_ranks.index(rank1) > hand_ranks.index(rank2):
            return 1
        elif hand_ranks.index(rank1) < hand_ranks.index(rank2):
            return -1
        else:
            # 同じ役の場合は、ハイカードで比較
            for hc1, hc2 in zip(high_cards1, high_cards2):
                if hc1 != hc2:
                    return (hc1 > hc2) - (hc1 < hc2)
            return 0
