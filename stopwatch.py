# template for "Stopwatch: The Game"


import simplegui
# define global variables
counter = 0
attempts = 0
success = 0
stop = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
 #   global time
    mins = t / 600
    tmp = t % 600
    sec = tmp / 10
    tenths_of_sec = tmp % 10
    
    if sec < 10:
        f_sec = "0"
    else:
        f_sec = ""
    time = str(mins) + ":" + f_sec + str(sec) + "." +  str(tenths_of_sec)
    return time
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    global stop
    
    stop = False
    timer.start()
    
def stop_handler():    
    global attempts
    global success
    global counter
    global stop
    
    if stop == False:        
        if (counter % 600) % 10 == 0:
            success += 1
        attempts += 1        
        timer.stop()
        stop = True

def reset_handler():
    global counter
    global attempts
    global success
    global stop
    
    timer.stop()
    counter = 0
    attempts = 0
    success = 0
    stop = True


# define event handler for timer with 0.1 sec interval
def timer_handler():
    global counter
    counter += 1
    #print counter
    


# define draw handler
def draw(canvas):
    global counter
    global attempts
    global success    
    
    canvas.draw_text(format(counter), [60, 100], 40, "White")
    tries = str(success) + "/" + str(attempts)
    canvas.draw_text(tries, [130, 40], 30, "Red")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 200, 200)
start_button = frame.add_button("Start", start_handler, 100)
stop_button = frame.add_button("Stop", stop_handler, 100)
reset_button = frame.add_button("Reset", reset_handler, 100)

frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, timer_handler)
#timer.start()

# register event handlers


# start frame
frame.start()



