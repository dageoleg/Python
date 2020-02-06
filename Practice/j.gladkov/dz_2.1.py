import tkinter
from time import sleep

width = 500
height = 400
title = "Your login"

top = tkinter.Tk()
top.minsize(width=width + 10, height=height + 10)
if title:
    top.title(title)

canvas = tkinter.Canvas(top, width=width + 2, height=height + 2)
canvas.pack()
canvas.xview_scroll(8, 'units')  # hack so (0, 0) works correctly
canvas.yview_scroll(8, 'units')  # otherwise it's clipped off

# Написать свой код сюда ----------------------

step = 3
x = 0
direction = 0 # 0 - вправо, 1 - влево
while True:
    canvas.delete("all")

    canvas.create_line(x + 150, 100, x + 330, 100, fill='red')
    canvas.create_line(x + 150, 100, x + 150, 160, fill='red')
    canvas.create_line(x + 330, 100, x + 330, 160, fill='red')

    canvas.create_line(x + 50, 160, x + 430, 160, fill='black')
    canvas.create_line(x + 50, 160, x + 50, 220, fill='black')
    canvas.create_line(x + 430, 160, x + 430, 220, fill='black')
    canvas.create_line(x + 50, 220, x + 430, 220, fill='black')

    canvas.create_oval(x + 80, 185, x + 150, 255, outline="green", width=2)
    canvas.create_oval(x + 330, 185, x + 400, 255, outline="green", width=2)

    canvas.update()
    sleep(0.1)

    if x == 20 * step:
        direction = 1
    elif x == -15 * step:
        direction = 0

    if direction == 0:
        x = x + step
    else:
        x = x - step

# Красная
#for i in range(n):
#    x = 300
#    y = 100
#    n = 100
#    y_add = (i / (n - 1)) * (height - 1)
#    x_add = (i / (n - 1)) * (height - 1)
#    canvas.create_line(x, y, x + width - 1, y + y_add, fill='red')

# Рисуем зеленые линии
#for i in range(n):
 #   x = 0
#    y = 0
 #   n = 100
 #   canvas.create_rectangle(x, y, width, height)
 #   y_add = (i / (n - 1)) * (height - 1)
 #   x_add = (i / (n - 1)) * (width - 1)

    # Зеленые линии
 #   canvas.create_line(x, y + y_add, x + x_add, y + height - 1, fill='green')

# ----------------------------------------------


if tkinter._default_root:
    tkinter._default_root.update()
    tkinter.mainloop()
