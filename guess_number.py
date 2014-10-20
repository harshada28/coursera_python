# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random


num_guesses = 7
current_max_guesses = 7


# helper function to start and restart the game
def new_game():
    global secret_number
    global num_guesses        
    global current_max_guesses
    
    print ""
    
    if current_max_guesses == 7:
        print "New game. Range is from 0 to 100"
        secret_number = random.randrange(0, 100)
    else:
        print "New game. Range is from 0 to 1000"
        secret_number = random.randrange (0, 1000)
    
    num_guesses = current_max_guesses
    print "Number of remaining guesses is", num_guesses

# define event handlers for control panel
def range100():
    global current_max_guesses
    current_max_guesses = 7
    new_game()
    
    
def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global current_max_guesses
    current_max_guesses = 10
    new_game()
    
    
def input_guess(guess):
    global num_guesses
    num = int(guess)
    print ""
    print "Guess was", num
    num_guesses = num_guesses - 1;
    print "Number of remaining guesses is", num_guesses
    if num == secret_number:
        print "Correct!"
        new_game()        
    elif secret_number < num:
        if (num_guesses):
            print "Lower!"
        else:
            print "You ran out of guesses. The number was ", secret_number
            new_game()    
    else:
        if (num_guesses):
            print "Higher!"
        else:
            print "You ran out of guesses. The number was ", secret_number
            new_game()    
    
      
    

    
# create frame
frame = simplegui.create_frame("Guess_the_number", 200, 200, 200)
button1 = frame.add_button("Range: [0, 100)", range100)
button2 = frame.add_button("Range: [0, 1000)", range1000)
label = frame.add_input("Enter a guess", input_guess, 100)


# register event handlers for control elements and start frame


# call new_game 
new_game()



