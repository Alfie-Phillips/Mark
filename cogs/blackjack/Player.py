from Card import Card  

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


