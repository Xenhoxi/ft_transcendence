
class Player:

	def __init__(self, id, name):
		if id == 1:
			self.set_pos(0, (1080 - 233) / 2)
		else:
			self.set_pos(2040 - 77, (1080 - 233) / 2)
		self.id = id
		self.name = name
		self.up_pressed = False
		self.down_pressed = False
		self.score = 0

	def set_pos(self, x, y):
		self.y = y
		self.x = x
		self.speed = 1000

	def move(self, up_pressed, down_pressed):
		if up_pressed:
			self.y -= self.speed * 0.01667
		if down_pressed:
			self.y += self.speed * 0.01667
		if self.y < 0:
			self.y = 0
		elif self.y > 1080 - 233:
			self.y = 1080 - 233

	def scored(self):
		self.score += 1

	def get_class(self):
		return self
