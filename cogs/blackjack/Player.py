from .Card import Card  

class Player:
    def __init__(self, member):
        self.member = member
        self.hand = list()
        self.is_playing = True
        self.has_played = False
        self.is_busted = False

    def deal(self):
        self.is_playing = True
        for _ in range(2):
            self.hand.append(Card.draw_card())

    def hand_str(self, num_cards=0):
        hand = ""
        if num_cards == 0:
            num_cards = len(self.hand)
        for index in range(num_cards):
            hand += f"    " + self.hand[index].__str__() + "\n"

        return hand

    def reset_hand(self):
        return self.hand.clear()

    def reset(self):
        """
        Resets the player to initial state
        """
        self.reset_hand()
        self.is_playing = True
        self.has_played = False
        self.is_busted = False

    def hit(self):
        """
        Adds a card to the players hand
        :return: True if successful hit, False if not
        """
        if self.is_playing and not self.has_played and not self.is_bust():
            self.hand.append(Card.draw_card())
            self.has_played = True
            return True
        return False

    def hold(self):
        """
        Holds the players current hand, preventing them from hitting more cards
        :return: True if a successful hold, False if not
        """
        if self.is_playing and not self.has_played:
            self.is_playing = False
            self.has_played = True
            return True
        return False

    def get_hand_values(self):
        """
        Determines the possible values of the current players hand
        This is useful when a player has an Ace in their hand, as it can be of value 1 or 11.
        :return: list of possible integer values of the players current hand
        """
        values = list()
        has_ace = False
        hand_value = 0
        for c in self.hand:
            if isinstance(c, Card):
                if c.value == 1:
                    has_ace = True
                else:
                    hand_value += c.value
        if has_ace:  # append the current hand value with the two values of an Ace
            values.append(hand_value + 1)
            values.append(hand_value + 11)
        else:
            values.append(hand_value)
        return values

    def is_bust(self):
        """
        Determines if the current player is busted (has a hand value of over 21).
        If the hand has multiple values, both must be a value over 21 in order to be considered busted.
        :return: Boolean stating if busted
        """
        for value in self.get_hand_values():
            if value <= 21:
                return False
        return True

    def has_blackjack(self):
        """
        Determines if the player has blackjack, a hand of value 21.
        :return: Boolean stating if the player has 21
        """
        for value in self.get_hand_values():
            if value == 21:
                return True
        return False

    def bust(self):
        """
        Sets the player's state to that of a player that cannot play anymore.
        """
        self.is_playing = False
        self.has_played = True
        self.is_busted = True
