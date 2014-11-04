# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

HIT_STAND = "Hit or Stand?"
NEW_DEAL = "New deal?"
# initialize some useful global variables
in_play = False
outcome = ""
choice = ""
dealer_score = 0
player_score = 0

deck = None
player_hand = None
dealer_hand = None

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos, back_card):
        if back_card:
            card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
        
            canvas.draw_image(card_back, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        else:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
    
            
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        s = "Hand contains "
        for card in self.cards:
            s = s + " " + str(card)
        return s

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hand_value = 0
        ace_present = False
        for card in self.cards:
            hand_value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                ace_present = True
         
        if ace_present and hand_value + 10 <= 21:
            return hand_value + 10
        else:
            return hand_value
        
        
    def draw(self, canvas, pos, dealer_hand):
        loc = pos
        if dealer_hand and in_play:
            self.cards[0].draw(canvas, loc, True)
            i = 1
        else:
            i = 0       
        
        while i < 5 and i < len(self.cards): 
            #print i
            loc[0] = 50 + i * CARD_SIZE[0] 
            #print pos[0], i, loc[0]  
            self.cards[i].draw(canvas, loc, False)
            i += 1
            
        
 
        
# define deck class 
class Deck:
    def __init__(self):
       self.deck = []
       for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deck.append(card)

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        s = "Deck contains "
        for card in self.deck:
            s += str(card) + " "
        return s



#define event handlers for buttons
def deal():
    global outcome, in_play, dealer_score, player_score, choice
    global deck, player_hand, dealer_hand
    
    outcome = ""
    if in_play:
        dealer_score += 1
        outcome = "Player looses"
        
    deck = player_hand = dealer_hand = None
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()

    deck.shuffle()
    card = deck.deal_card()
    player_hand.add_card(card)
    
    card = deck.deal_card()
    dealer_hand.add_card(card)
    
    card = deck.deal_card()
    player_hand.add_card(card)
    
    card = deck.deal_card()
    dealer_hand.add_card(card)
    
    # your code goes here
    print "Dealer ", dealer_hand, dealer_hand.get_value()
    print "Player ", player_hand, player_hand.get_value()

    if player_hand.get_value() > 21:    
        in_play = False
        dealer_score  += 1
        outcome = "You went bust and lose"
    else:
        in_play = True
        choice = HIT_STAND
        

def hit():
    global player_hand, deck, in_play, dealer_score, player_score, outcome
    
    if in_play:
        card = deck.deal_card()
        player_hand.add_card(card)
        value = player_hand.get_value()
    
        print "Player hand ", value
        if value > 21:
            outcome =  "You went bust and loose"
            in_play = False
            dealer_score += 1
    
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global dealer_hand, deck, in_play, outcome
    global dealer_score, player_score, choice
    
    if not in_play:
        outcome =  "Player went bust and loose"
        return
    
    while dealer_hand.get_value() < 17:
        card = deck.deal_card()
        dealer_hand.add_card(card)
        print "Dealer hand ", dealer_hand.get_value()
   
    in_play = False
    if dealer_hand.get_value() > 21:
        outcome =  "Dealer went bust and player wins"        
        player_score += 1
    elif dealer_hand.get_value() >= player_hand.get_value():
        outcome = "Dealer wins"
        dealer_score += 1        
    else:
        outcome = "Player wins"
        player_score += 1
    choice = NEW_DEAL
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player_hand, dealer_hand, choice, outcome
    global dealer_score, player_score, in_play
    
    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])
    
    dealer_hand.draw(canvas, [50, 200], True)
        
    canvas.draw_text("Blackjack", [40, 80], 40, "Blue")
    canvas.draw_text("Dealer Score " + str(dealer_score), [340, 80], 25, "Black")
    canvas.draw_text("Player Score " + str(player_score), [340, 120], 25, "Black")
    canvas.draw_text("Dealer", [50, 180], 25, "Black")
    canvas.draw_text("Player", [50, 380], 25, "Black")
    canvas.draw_text(choice, [250, 380], 25, "Black")
    canvas.draw_text(outcome, [250, 180], 25, "Black")
    player_hand.draw(canvas, [50, 400], False)

#init globals

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
