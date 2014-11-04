# implementation of card game - Memory

import simplegui
import random

CARD_WIDTH = 50
CARD_HEIGHT = 100
cards = []
exposed = []
state = 0
old_card_ind = -1
curr_card_ind = -1
clicks = 0
# helper function to initialize globals
def new_game():
    global cards
    global exposed
    global clicks
    
    cards = range(0, 8)
    cards.extend(range(0, 8))
    random.shuffle(cards)
    print cards

    exposed = list(cards)
    for i in range(0, 16):
        exposed[i] = False
    
    clicks = 0
   
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, clicks
    global old_card_ind, curr_card_ind    
    
    if pos[1] >=0 and pos[1] <= CARD_HEIGHT - 1:
        ind = pos[0] / CARD_WIDTH
        assert (ind >= 0 and ind <16), "Wrong card index!"        
        
        if state == 0:              
            if exposed[ind] == False:
                exposed[ind] = True
                state = 1
                old_card_ind = ind
                clicks += 1
                print clicks
                
                
        elif state == 1:       
            if exposed[ind] == False:
                exposed[ind] = True
                state = 2
                curr_card_ind = ind
                #clicks += 1
                #print clicks
                
        elif state == 2:
            if exposed[ind] == False:
                if not cards[old_card_ind] == cards[curr_card_ind]:
                        exposed[curr_card_ind] = False
                        exposed[old_card_ind] = False          
                
            
                exposed[ind] = True
                state = 1
                clicks += 1
                old_card_ind = ind
                print clicks
            
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cards
    global exposed   
  
    
    label.set_text("Turns = " + str(clicks))
    for i in range(0, len(cards)):        
        if exposed[i] == True:
            card = cards[i]
            canvas.draw_text(str(card), (i * CARD_WIDTH + 20, CARD_HEIGHT / 2), 40, "White")
        else:
            x = [i * CARD_WIDTH, 0]
            y = [x[0] + CARD_WIDTH, 0]
            w = [x[0] + CARD_WIDTH,  CARD_HEIGHT]
            z = [i * CARD_WIDTH,  CARD_HEIGHT]
            canvas.draw_polygon([x, y, w, z], 4, "Black", "Green")
            
        i += 1


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
