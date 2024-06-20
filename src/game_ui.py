import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout

# sys.pathにsrcディレクトリを追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.card_deck import CardDeck
from src.game_rules import GameRules
from src.ai import AIPlayer

class GameUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('AIM Poker')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel('Welcome to AIM Poker', self)
        self.layout.addWidget(self.label)

        self.start_button = QPushButton('Start Game', self)
        self.start_button.clicked.connect(self.start_game)
        self.layout.addWidget(self.start_button)

        self.action_label = QLabel('', self)
        self.layout.addWidget(self.action_label)

        # アクションボタンを追加
        self.action_buttons = QHBoxLayout()
        self.fold_button = QPushButton('Fold', self)
        self.fold_button.clicked.connect(lambda: self.player_action('fold'))
        self.action_buttons.addWidget(self.fold_button)

        self.call_button = QPushButton('Call', self)
        self.call_button.clicked.connect(lambda: self.player_action('call'))
        self.action_buttons.addWidget(self.call_button)

        self.bet_button = QPushButton('Bet', self)
        self.bet_button.clicked.connect(lambda: self.player_action('bet'))
        self.action_buttons.addWidget(self.bet_button)

        self.raise_button = QPushButton('Raise', self)
        self.raise_button.clicked.connect(lambda: self.player_action('raise'))
        self.action_buttons.addWidget(self.raise_button)

        self.layout.addLayout(self.action_buttons)
        self.disable_action_buttons()

    def disable_action_buttons(self):
        self.fold_button.setEnabled(False)
        self.call_button.setEnabled(False)
        self.bet_button.setEnabled(False)
        self.raise_button.setEnabled(False)

    def enable_action_buttons(self):
        self.fold_button.setEnabled(True)
        self.call_button.setEnabled(True)
        self.bet_button.setEnabled(True)
        self.raise_button.setEnabled(True)

    def player_action(self, action):
        # プレイヤーのアクションを処理
        self.disable_action_buttons()
        print(f"Player decided to {action}")

    def start_game(self):
        deck = CardDeck()
        community_cards = GameRules.deal_community_cards(deck, 5)
        self.label.setText(f'Community Cards: {community_cards}')

        players = [AIPlayer("AI Player 1"), AIPlayer("AI Player 2")]
        pot = 0
        bb = 10
        last_bet = 0
        min_raise = bb

        actions_text = ""

        for player in players:
            player.hole_cards = [deck.deal_card(), deck.deal_card()]
            action, amount = player.decide_action(community_cards, pot, bb, last_bet, min_raise)
            actions_text += f"{player.name} decided to {action} with amount {amount}\n"
            if action in ['bet', 'raise', 'all-in']:
                pot += amount
                last_bet = amount
                min_raise = last_bet

        self.action_label.setText(actions_text)
        self.enable_action_buttons()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_ui = GameUI()
    game_ui.show()
    sys.exit(app.exec_())
