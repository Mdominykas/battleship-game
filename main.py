import tkinter as tk
import enum
import random

class CellState(enum.Enum):
	empty_not_hit = 1
	empty_hit = 2
	ship_not_hit = 3
	ship_hit = 4


class BoardState:
	def __init__(self, width, height, can_see_ships):
		self.width = width
		self.height = height
		self.state = [[0] * self.width] * self.height
		self.state = []
		self.can_see_ships = can_see_ships
		for i in range(0, self.width):
			self.state.append([])
			for j in range(0, self.height):
				self.state[-1].append(CellState.empty_not_hit)
	def cell_state(self, x, y):
		assert((0 <= x) and (x < GameConstants.BOARD_WIDTH) and (0 <= y) and (y < GameConstants.BOARD_HEIGHT))
		return self.state[y][x]
	def set_cell_state(self, x, y, new_state):
		self.state[y][x] = new_state
	def can_shoot(self, x, y):
		state = self.cell_state(x, y)
		return (state == CellState.ship_not_hit) or (state == CellState.empty_not_hit)
	def shoot(self, x, y):
		state = self.cell_state(x, y)
		if(state == CellState.ship_not_hit):
			self.set_cell_state(x, y, CellState.ship_hit)
		elif(state == CellState.empty_not_hit):
			self.set_cell_state(x, y, CellState.empty_hit)
		else:
			assert(False)
	# def hitted_battleship()

	def get_color(self, x, y):
		state = self.cell_state(x, y)
		if (state == CellState.empty_not_hit):
			return ''
		elif (state == CellState.empty_hit):
			return 'blue'
		elif (state == CellState.ship_not_hit):
			return 'black' if self.can_see_ships else ''
		elif (state == CellState.ship_hit):
			return 'red'
		else:
			assert(False)

	def can_place(self, x0, y0, length, is_vertical=False):
		if(is_vertical):
			dx = 0
			dy = 1
		else:
			dx = 1
			dy = 0
		if((x0 < 0) or (y0 < 0) or (x0 >= self.width) or (y0 >= self.height)):
			return False
		x1 = x0 + (length - 1) * dx
		y1 = y0 + (length - 1) * dy
		if((x1 >= self.width) or (y1 >= self.height)):
			return False
		while((x0 <= x1) and (y0 <= y1)):
			state = self.cell_state(x0, y0)
			if(state != CellState.empty_not_hit):
				return False
			x0 += dx
			y0 += dy
		return True

	def place_ship(self, x0, y0, length, is_vertical):
		assert(self.can_place(x0, y0, length, is_vertical))
		if(is_vertical):
			dx = 0
			dy = 1
		else:
			dx = 1
			dy = 0
		x1 = x0 + (length - 1) * dx
		y1 = y0 + (length - 1) * dy

		while((x0 <= x1) and (y0 <= y1)):
			self.set_cell_state(x0, y0, CellState.ship_not_hit)
			x0 += dx
			y0 += dy


class ComputerShipPlacement:
	def __init__(self, place_for_ships):
		self.place_for_ships = place_for_ships
	def place_ships(self, ships):
		i = 0
		while i < len(ships):
			length = ships[i]
			x = random.randint(0, self.place_for_ships.width)
			y = random.randint(0, self.place_for_ships.height)
			direction = bool(random.getrandbits(1))
			if(self.place_for_ships.can_place(x, y, length, direction)):
				self.place_for_ships.place_ship(x, y, length, direction)
				i += 1



class BattleshipMap:
	def __init__(self, canvas, x0, y0, x_max, y_max, height, width, border_width = 3, can_see_ships = True):
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
		self.can_see_ships = can_see_ships
		self.map =  [ [ [0] * width ] * height ]
		self.state = BoardState(width, height, can_see_ships)
	def draw_board(self):
		x_len, y_len = self.compute_lens()
		for i in range(0, self.height):
			for j in range(0, self.width):
				top_left = (self.x0 + j * x_len, self.y0 + i * y_len)
				bot_right = (self.x0 + (j + 1) * x_len, self.y0 + (i + 1) * y_len)
				color = self.state.get_color(j, i)
				self.canvas.create_rectangle((top_left, bot_right), width = self.border_width, fill=color)
	def compute_lens(self):
		x_len = (self.x_max - self.x0) / self.width
		y_len = (self.y_max - self.y0) / self.height
		return (x_len, y_len)

	def find_cell(self, x, y):
		if((x < self.x0) or (self.x_max < x) or (y < self.y0) or (self.y_max < y)):
			return (-1, -1)
		x_len, y_len = self.compute_lens()
		x_num = (x - self.x0) / x_len
		y_num = (y - self.y0) / y_len
		return int(x_num), int(y_num)

	def can_shoot(self, x, y):
		return self.state.can_shoot(x, y)

	def shoot(self, x, y):
		self.state.shoot(x, y)

	def can_place(self, x0, y0, length, vertical):
		return self.state.can_place(x0, y0, length, vertical)

	def place_ship(self, x0, y0, length, vertical):
		self.state.place_ship(x0, y0, length, vertical)


class GameConstants:
	# BOARD_HEIGHT = 500
	# BOARD_WIDTH = 500
	BOARD_DISPLAY_WIDTH = 500
	BOARD_DISPLAY_HEIGHT = 500
	BOARD_DISPLAY_GAP = 100
	CANVAS_WIDTH = 2 * BOARD_DISPLAY_WIDTH + BOARD_DISPLAY_GAP
	BOARD_WIDTH = 10
	BOARD_HEIGHT = 10
	SHIP_LENGTHS = [5, 4, 3, 3, 2]


class Turn(enum.Enum):
	PLAYER = 0
	COMPUTER = 1


class Gameplay:
	def __init__(self, player_map, computer_map, starting_turn = Turn.PLAYER):
		self.current_turn = starting_turn
		self.player_map = player_map
		self.computer_map = computer_map
		computer_ship_placing = ComputerShipPlacement(computer_map)
		computer_ship_placing.place_ships(GameConstants.SHIP_LENGTHS)
		player_ship_placement = ComputerShipPlacement(player_map)
		player_ship_placement.place_ships(GameConstants.SHIP_LENGTHS)
		self.player_map.draw_board()
		self.computer_map.draw_board()

	def process_player_shot(self, x, y):
		# TODO: patikrinti, kad zaidimas prasidejes
		assert((x != -1) and (y != -1))
		if(self.current_turn != Turn.PLAYER):
			return
		if(not self.computer_map.can_shoot(x, y)):
			return
		self.computer_map.shoot(x, y)
		self.computer_map.draw_board()
		self.current_turn = Turn.COMPUTER
		
		shot_x = random.randint(0, self.player_map.width - 1)
		shot_y = random.randint(0, self.player_map.height - 1)
		while(not self.player_map.can_shoot(shot_x, shot_y)):
			shot_x = random.randint(0, self.player_map.width - 1)
			shot_y = random.randint(0, self.player_map.height - 1)
		self.player_map.shoot(shot_x, shot_y)
		self.current_turn = Turn.PLAYER
		self.player_map.draw_board()



class GameGraphics:
	def __init__(self, window):
		self.canvas = tk.Canvas(window, bg="white", width=GameConstants.CANVAS_WIDTH, height=GameConstants.BOARD_DISPLAY_WIDTH)
		self.canvas.pack()

		self.player_map = BattleshipMap(self.canvas, 0, 0, GameConstants.BOARD_DISPLAY_WIDTH, 
			GameConstants.BOARD_DISPLAY_HEIGHT, GameConstants.BOARD_WIDTH, GameConstants.BOARD_HEIGHT, 
			can_see_ships=True)

		self.computer_map = BattleshipMap(self.canvas, GameConstants.BOARD_DISPLAY_WIDTH + GameConstants.BOARD_DISPLAY_GAP, 
			0, 2 * GameConstants.BOARD_DISPLAY_WIDTH + GameConstants.BOARD_DISPLAY_GAP, GameConstants.BOARD_DISPLAY_HEIGHT,
			GameConstants.BOARD_WIDTH, GameConstants.BOARD_HEIGHT, can_see_ships=False)

		self.gameplay = Gameplay(self.player_map, self.computer_map)

	def process_mouse_click(self, event):
		x, y = event.x, event.y
		if (not ((x >= 0) and (x < GameConstants.CANVAS_WIDTH) and (y >= 0) and (y < GameConstants.BOARD_DISPLAY_HEIGHT))):
			return 
		if((GameConstants.BOARD_DISPLAY_WIDTH < x) and (x < GameConstants.BOARD_WIDTH + GameConstants.BOARD_DISPLAY_GAP)):
			return
		if(x <= GameConstants.BOARD_DISPLAY_WIDTH):
			# no gameplay implemented yet
			return 
		else:
			(cellx, celly) = self.computer_map.find_cell(x, y)
			self.gameplay.process_player_shot(cellx, celly)





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

graphics = GameGraphics(window)

# rect = canvas.create_rectangle(((0, 0), (30, 70)), width = 3)
# draw_board(canvas, 0, 0, 500, 600, 8, 8)

def action(event):
    print(dir(event))
    print(event.num)
    print(event.type)
    print(event.x)
    print(event.y)
    print()

window.bind("<ButtonPress-1>", graphics.process_mouse_click)
window.mainloop()
