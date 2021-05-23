from random import randint

class Card:
    SUITES = ["Hearts", "Clubs", "Spades", "Diamonds"]

    CARDS = ['Ace', 'Two', 'Three', 'Four',
             'Five', 'Six', 'Seven', 'Eight',
             'Nine', 'Ten', 'Jack', 'Queen', 'King']

    deck = list()

    def __init__(self, value, suite, card):
        self.value = value
        self.suite = suite
        self.name = f"{card} of {suite}"

    def __str__(self):
        return self.name

    @staticmethod
    def create_deck():
        Card.clear_deck()
        for suite in Card.SUITES:
            value = 1
            for card in Card.CARDS:
                Card.deck.append(Card(value, suite, card))
                if value < 10:
                    value += 1

    @staticmethod
    def clear_deck():
        Card.deck.clear()

    @staticmethod
    def draw_card():
        if len(Card.deck) == 0:
            Card.create_deck()
        return Card.deck.pop(randint(0, len(Card.deck)-1))