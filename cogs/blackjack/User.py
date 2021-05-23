from .Player import Player

class User(Player):
    def __init__(self, member):
        super().__init__(member)

        self.id = member.id
        self.bank = 5000
        self.current_bet = 0

    def str_with_hand(self):
        return self.mention_user() + ":\n" + self.hand_str()

    def str_with_bet(self):
        return "{0} bet {1} memes".format(self.mention_user(), str(self.current_bet))

    def str_with_bank(self):
        return "{0} has {1} memes".format(self.mention_user(), str(self.bank))

    def bet(self, amount):
        """
        Bets a certain amount of money during a round of blackjack.
        :param amount: integer number of money user wants to bet
        :return bool stating if the bet was valid or not
        """
        if isinstance(amount, int):
            if amount > self.bank or amount < 100 or amount > 500:
                return False
            else:
                self.current_bet = amount
                return True
        else:
            return False

    def reset(self):
        """
        Resets the user to initial values
        """
        super().reset()
        self.current_bet = 0

    def mention_user(self):
        if self.member.nick:
            return '<@!{}>'.format(self.id)
        return '<@{}>'.format(self.id)

    def gain_bet(self):
        if self.has_blackjack():
            self.bank += int(self.current_bet * 1.5)
            return int(self.current_bet * 1.5)
        self.bank += self.current_bet
        return self.current_bet

    def lose_bet(self):
        self.bank -= self.current_bet
        return self.current_bet

    def set_bank(self, new):
        """
        Sets the user's bank to the passed amount
        :param new: int value of new bank
        """
        self.bank = new