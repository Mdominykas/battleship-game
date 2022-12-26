import tkinter as tk

class BattleshipMap:
	def __init__(self, canvas, x0, y0, x_max, y_max, height, width, border_width = 3):
		assert((x0 < x_max) and (y0 < y_max))
		assert((height > 0) and (width > 0))
		self.canvas = canvas
		self.x0 = x0
		self.y0 = y0
		self.x_max = x_max
		self.y_max = y_max
		self.height = height
		self.width = width
		self.border_width = border_width
	def draw_board(self):
		x_len = (self.x_max - self.x0) / self.width
		y_len = (self.y_max - self.y0) / self.height
		for i in range(0, self.height):
			for j in range(0, self.width):
				top_left = (self.x0 + j * x_len, self.y0 + i * y_len)
				bot_right = (self.x0 + (j + 1) * x_len, self.y0 + (i + 1) * y_len)
				canvas.create_rectangle((top_left, bot_right), width = self.border_width)


# def draw_board(canvas, x0, y0, x_max, y_max, height, width, border_width = 3):
# 	x_len = (x_max - x0) / width
# 	y_len = (y_max - y0) / height
# 	for i in range(0, height):
# 		for j in range(0, width):
# 			top_left = (x0 + j * x_len, y0 + i * y_len)
# 			bot_right = (x0 + (j + 1) * x_len, y0 + (i + 1) * y_len)
# 			canvas.create_rectangle((top_left, bot_right), width = border_width)

window = tk.Tk()

greeting = tk.Label(text="Battleship")
greeting.pack()

canvas = tk.Canvas(window, bg="white", width=500, height=600)
canvas.pack()

battleship_map = BattleshipMap(canvas, 0, 0, 500, 600, 8, 8)
battleship_map.draw_board()

# rect = canvas.create_rectangle(((0, 0), (30, 70)), width = 3)
# draw_board(canvas, 0, 0, 500, 600, 8, 8)

def action(event):
    print(dir(event))
    print(event.num)
    print(event.type)
    print(event.x)
    print(event.y)
    print()

window.bind("<ButtonPress-1>", action)
window.mainloop()
