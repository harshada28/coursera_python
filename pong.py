# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

paddle1_pos =  HEIGHT / 2
paddle2_pos =  HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    h = random.randrange(120, 240) / 60;
    v = random.randrange(60, 180) / 60;
    if direction == "RIGHT":
        ball_vel = [h, -1 * v]
    else:
        ball_vel = [-1 * h, -1 * v]    

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    score1 = score2 = 0
    spawn_ball(LEFT)

def restart_handler():
    new_game()
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel    
    
    direction = ""
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
   
    if (ball_pos[1] <= BALL_RADIUS) or (HEIGHT - 1 - BALL_RADIUS <= ball_pos[1]):
        ball_vel[1] = -ball_vel[1]
    
    if (ball_pos[0] - PAD_WIDTH <= BALL_RADIUS):
        a = (ball_pos[1] + BALL_RADIUS >= paddle1_pos - PAD_HEIGHT/2)
        b = (ball_pos[1] - BALL_RADIUS <= paddle1_pos + PAD_HEIGHT/2)
        if a and b:
            ball_vel[0] = -1.1 * ball_vel[0]            
        else:
            direction = "RIGHT"
            score2 += 1            
    elif (ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH):
        a = (ball_pos[1] + BALL_RADIUS >= paddle2_pos - PAD_HEIGHT/2)
        b = (ball_pos[1] - BALL_RADIUS <= paddle2_pos + PAD_HEIGHT/2)
        if a and b:
            ball_vel[0] = -1.1 * ball_vel[0]            
        else:
            score1 += 1
            direction = "LEFT"  
        
    # update ball   
    if not direction == "":        
        spawn_ball(direction)       
    else:
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]

        # draw ball        
    canvas.draw_circle([ball_pos[0], ball_pos[1]], BALL_RADIUS, 2, "Black", "White")                           
    
    # update paddle's vertical position, keep paddle on the screen
    x = paddle1_pos + paddle1_vel
    if x >= PAD_HEIGHT/2 and x <= HEIGHT - PAD_HEIGHT/2 - 1:
        paddle1_pos += paddle1_vel
        
    x = paddle2_pos + paddle2_vel
    if x >= PAD_HEIGHT/2 and x <= HEIGHT - PAD_HEIGHT/2 - 1:
        paddle2_pos += paddle2_vel    
    
    # draw paddles    
    a = [0, paddle1_pos - PAD_HEIGHT / 2]
    b = [PAD_WIDTH, paddle1_pos - PAD_HEIGHT / 2]    
    c = [PAD_WIDTH, paddle1_pos + PAD_HEIGHT / 2]
    d = [0, paddle1_pos + PAD_HEIGHT / 2]
    
    canvas.draw_polygon([a, b, c, d], 2, "white", "white") 
    
    a = [WIDTH - PAD_WIDTH, paddle2_pos - PAD_HEIGHT / 2]
    b = [WIDTH, paddle2_pos - PAD_HEIGHT / 2]
    c = [WIDTH, paddle2_pos + PAD_HEIGHT / 2]
    d = [WIDTH - PAD_WIDTH, paddle2_pos + PAD_HEIGHT / 2]
    
    canvas.draw_polygon([a, b, c, d], 2, "white", "white")     
    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH / 4, HEIGHT / 8], 40, "White")
    canvas.draw_text(str(score2), [WIDTH / 2 + WIDTH / 4, HEIGHT / 8], 40, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -4
        
    if key == simplegui.KEY_MAP["s"]:
       paddle1_vel = 4
    
    if key == simplegui.KEY_MAP["up"]:        
       paddle2_vel = -4
        
    if key == simplegui.KEY_MAP["down"]:
       paddle2_vel = 4
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
       paddle1_vel = 0
        
    if key == simplegui.KEY_MAP["s"]:        
       paddle1_vel = 0
    
    if key == simplegui.KEY_MAP["up"]:
       paddle2_vel = 0
        
    if key == simplegui.KEY_MAP["down"]:        
       paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Restart", restart_handler, 100)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()

