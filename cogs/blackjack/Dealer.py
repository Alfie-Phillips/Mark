from .Player import Player

class Dealer(Player):
    def __init__(self, member):
        super().__init__(member)

    def str_with_hand(self):
        """
        Only shows the first card in the hand, like in a real blackjack game.
        :return: str depicting the dealer and the first card in it's hand
        """
        return "Dealer: (only shows one card)\n" + self.hand_str(1)

    def final_str_with_hand(self):
        """
        Shows all of the dealer's hand, for post game printing to players.
        :return: str depicting the dealer and i's entire hand
        """
        return "Dealer's final hand:\n" + self.hand_str()

    def hit_until_hold(self):
        """
        Keeps on adding cards to the hand until the lowest value of the hand is above 16, then holds.
        This method assumes that the dealer has already been dealt cards, and is to be used after all players are done
        playing.
        """
        while min(value for value in self.get_hand_values()) < 17:
            self.hit()
        self.hold()