from tkinter import *
from tkinter import messagebox
from random import *
import math
import numpy



after_id = None
balls = []
animation_running = False

root = Tk()
root.title("Balls")
root.geometry('1000x1000')


control_frame = Frame(root)
control_frame.pack(side=TOP, pady=10)


canvas = Canvas(control_frame, width = 500, height = 500, bg= 'blue')
canvas.pack()

Label(control_frame, text='Starting speed of balls').pack()
speed = Entry(control_frame, width=30, bg="lightgray")
speed.pack()

Label(control_frame, text='balls').pack()
n_balls = Entry(control_frame, width=30, bg="lightgray")
n_balls.pack()

Label(control_frame, text='FPS').pack()
fps = Entry(control_frame, width=30, bg="lightgray")
fps.pack()

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
    global balls, animation_running, after_id, speed_true, fps_true, vel
    balls.clear()
    canvas.delete('balls')

    if after_id:
        canvas.after_cancel(after_id)
        after_id = None
    
    try:
        balls_true = int(n_balls.get())
        speed_true = int(speed.get())
        fps_true = int(fps.get())
        for i in range(balls_true):
            x1 = randint(0, 500 - BALL_SIZE)
            y1 = randint(0, 500 - BALL_SIZE)
            x2 = x1 + BALL_SIZE
            y2 = y1 + BALL_SIZE
            velx = choice([-1, 1]) * speed_true
            vely = choice([-1, 1]) * speed_true
            vel = numpy.array([velx, vely])
            
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
        
        if coords[0] + velx < 0 or coords[2] + velx > 500:
            velx = choice([-1, 1]) * speed_true
        if coords[1] +vely < 0 or coords[3] + vely > 500:
            vely = choice([-1, 1]) * speed_true

        canvas.move(ball_id, velx,vely)
        balls[i] = (ball_id, velx,vely)


        ball1_coords = canvas.coords(ball_id)

        # Check collisions with other balls
        for j in range(i + 1, len(balls)):
            ball2_id, velx2, vely2 = balls[j]
            ball2_coords = canvas.coords(ball2_id)
            
            
            if balls_touch(ball1_coords, ball2_coords):
                

                coordx1 = (ball1_coords[0] + ball1_coords[2]) / 2
                coordy1 = (ball1_coords[1] + ball1_coords[3]) / 2
                coordx2 = (ball2_coords[0] + ball2_coords[2]) / 2
                coordy2 = (ball2_coords[1] + ball2_coords[3]) / 2

                coord1 = numpy.array([coordx1, coordy1])
                coord2 = numpy.array([coordx2, coordy2])
                vel2 = numpy.array([velx2, vely2])
                
                vel_new1 = vel + (numpy.dot((vel2-vel),(coord2 - coord1))/(abs(coord2-coord1)**2))*(coord2 - coord1)
                vel_new2 = vel2 + (numpy.dot((vel-vel2),(coord1-coord2))/(abs(coord1-coord2)**2))*(coord1-coord2)
                
                balls[i] = (ball_id, vel_new1[0], vel_new1[1])
                
                balls[j] = (ball2_id, vel_new2[0], vel_new2[1])

    after_id = canvas.after(int(1000/fps_true), move_balls)
    
    
def balls_touch(ball1_coords, ball2_coords):
    
    # center of balls coordinates
    x1 = (ball1_coords[0] + ball1_coords[2]) / 2
    y1 = (ball1_coords[1] + ball1_coords[3]) / 2
    x2 = (ball2_coords[0] + ball2_coords[2]) / 2
    y2 = (ball2_coords[1] + ball2_coords[3]) / 2

    if math.sqrt((x2 - x1)**2 + (y2 - y1)**2) < 30:
        return True
    else:
        return False



start = Button(control_frame, text='start', command=starting)
start.pack()

stop = Button(control_frame,text='Stop' ,command=stopping)
stop.pack()




root.mainloop()