from tkinter import *
from tkinter import messagebox
from random import *
import math



after_id = None


root = Tk()
root.title("Chicken and Balls")
root.geometry('1000x1000')


control_frame = Frame(root)
control_frame.pack(side=TOP, pady=10)


canvas = Canvas(control_frame, width = 500, height = 500, bg= 'blue')
canvas.pack()

Label(control_frame, text='speed').pack()
speed = Entry(control_frame, width=30, bg="lightgray")
speed.pack()

Label(control_frame, text='balls').pack()
n_balls = Entry(control_frame, width=30, bg="lightgray")
n_balls.pack()




balls = []
animation_running = False

def stopping():
    global balls, animation_running, after_id
    canvas.delete('balls')
    animation_running = False
    balls.clear()
    if after_id:
        canvas.after_cancel(after_id)
        after_id = None
    

def starting():
    BALL_SIZE = 30
    global balls, animation_running, after_id, speed_true
    balls.clear()
    canvas.delete('balls')

    if after_id:
        canvas.after_cancel(after_id)
        after_id = None
    
    try:
        balls_true = int(n_balls.get())
        speed_true = int(speed.get())
        for i in range(balls_true):
            x1 = randint(0, 500 - BALL_SIZE)
            y1 = randint(0, 500 - BALL_SIZE)
            x2 = x1 + BALL_SIZE
            y2 = y1 + BALL_SIZE
            velx = choice([-1, 1]) * speed_true
            vely = choice([-1, 1]) * speed_true
            ball_id = canvas.create_oval(x1, y1, x2, y2, fill="red", tags='balls')
            balls.append((ball_id, velx,vely))
    except ValueError:
        messagebox.showerror('Error', 'Try actually typing a number')
    
    animation_running = True
    move_balls()


def move_balls():
    global after_id, speed_true
    if not animation_running:
        return
    
    for i in range(len(balls)):
        ball_id, velx, vely = balls[i]
        coords = canvas.coords(ball_id)
        x1, y1, x2, y2 = coords

        
        if x1 + velx < 0 or x2 + velx > 500:
            velx = choice([-1, 1]) * randint(1, speed_true)
        if y1 +vely < 0 or y2 + vely > 500:
            vely = choice([-1, 1]) * randint(1, speed_true)

        canvas.move(ball_id, velx,vely)
        balls[i] = (ball_id, velx,vely)

    after_id = canvas.after(20, move_balls)
    
    
    


start = Button(control_frame, text='start', command=starting)
start.pack()

stop = Button(control_frame,text='Stop' ,command=stopping)
stop.pack()




root.mainloop()