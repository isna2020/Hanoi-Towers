from scene import *
import ui
import sound
import math
import random as rdm
import console
import time
import speech

size.w, size.h = get_screen_size()
all_moves = []
how_many_disc = 9

while how_many_disc > 8:
	how_many_disc = int(input('How  many discs? MAX 8 ?'))

x_shift = 1
y_shift = 1

# Tower x Cordinates
global Ax
global Bx
global Cx
Ax = 150
Bx = 300
Cx = 450
global width_scale
scale_fac = .95

global tAh
global tBh
global tCh
tAh = 80
tBh = 100
tCh = 100

global Atower
global Btower
global Ctower

Atower = []
Btower = []
Ctower = []

yStep = 34  # * scale_fac
totMoves = -1
i_count = 0

v = 0.6  # moving soeed
touch_loc = 0
t_count = 0
touch1 = touch2 = ''
#move_id = ''
hands = -1
#count_move = 0
count_wrongs = 0
score = 30
move = ''

A_touched = False
B_touched = False
C_touched = False
arrow_name = 'ARROWUP.png'


class Hanoi(Scene):
	def __init__(self, title):
		Scene.__init__(self)
		self.title = title

	class MyTextFieldDelegate(object):
		def textfield_should_begin_editing(self, textfield):
			return True

		def textfield_did_begin_editing(self, textfield):
			pass

		def textfield_did_end_editing(self, textfield):
			pass

		def textfield_should_return(self, textfield):
			textfield.end_editing()
			return True

		def textfield_should_change(self, textfield, range, replacement):
			return True

		def textfield_did_change(self, textfield):
			print(textfield.text)  #only changed this
			#pass	

	def setup(self):
		class MyTextFieldDelegate(object):
			pass

		global move
		# global tAh
		self.bg = SpriteNode(color='#008a54', parent=self)  # #004f00
		self.bg.alpha = 1
		self.bg.size = (self.size.w * 2, self.size.h * 2)

		self.background_pic = SpriteNode('BGPIC600X400.png')
		self.add_child(self.background_pic)
		#self.background_pic.scale = 1.2
		self.background_pic.position = self.size.w / 2, self.size.h / 2

		self.board = SpriteNode('BLUEBOARD.png')
		self.add_child(self.board)
		self.board.x_scale = 1
		self.board.y_scale = 1
		self.board.position = 288, 150

		self.arrow = SpriteNode('ARROWUP.png')  #R
		self.add_child(self.arrow)
		self.arrow.position = 0, 40

		self.label_score = LabelNode(
			'Touch one Disc, then touch next to move a Disc', ('futura_bold', 16),
			color='white',
			parent=self)
		self.label_score.position = (Ax + 150, 380)
		#self.label_ABC = LabelNode(' ', ('futura', 16), color='white', parent=self)
		#self.label_ABC.position = (self.board.position[0] + 15,self.board.position[1] - 95)
		#abc = 'A                        B                        C'
		#self.label_ABC.text = abc
		self.hanoi_func(how_many_disc, 'A', 'B', 'C')
		self.build_A_tower()
		# print(all_moves)

	def hanoi_func(self, n, a, b, c):
		global totMoves
		self.n, self.a = n, a
		self.b = b
		self.c = c
		#global d_index
		if n == 0:
			pass
		else:
			self.hanoi_func(n - 1, a, c, b)  # recursive call
			all_moves.append(a + c)
			self.hanoi_func(n - 1, b, a, c)  # recursive call
		totMoves = len(all_moves)

	def build_A_tower(self):
		global how_many_disc
		global scale_fac
		global Atower
		global tAh
		# global Ax
		global yStep
		width_scale = 1
		height_scale = .9

		j = how_many_disc
		for i in range(how_many_disc):
			j -= 1
			Atower.append(('DISC', j))
			#print('for j, i', i, j)
			Atower[i] = SpriteNode('GOLDDISC.png')
			self.add_child(Atower[i])
			Atower[i].scale = 0.75
			Atower[i].x_scale = width_scale
			width_scale = width_scale - 0.08
			#height_scale = height_scale - 0.05
			Atower[i].y_scale = height_scale
			#scale_fac = scale_fac - .05
			tAh += yStep
			Atower[i].position = Ax, tAh

	def update_move(self, move, tow1, tow2, dx, dh):
		self.move = move
		print(move)
		self.tow1 = tow1
		self.tow2 = tow2
		self.dx = dx
		print(move)
		if move == 'AC' or move == 'AB' or move == 'BC':
			arrow_name = 'ARROWUP.png'  # R
		if move == 'CA' or move == 'BA' or move == 'CB':
			arrow_name = 'ARROWUP.png'  # L
		self.arrow.remove_from_parent()
		self.arrow = SpriteNode(arrow_name)
		self.add_child(self.arrow)
		if dx > 75 and dx < 225:
			self.dx = Ax
			self.arrow.position = self.dx, 40
			move_action = Action.move_to(self.dx, 80, 1, TIMING_SINODIAL)  # A to B move
			#self.arrow.position = 150, 80
		elif dx > 225 and dx < 375:
			self.dx = Bx
			self.arrow.position = self.dx, 40
			move_action = Action.move_to(self.dx, 80, 1, TIMING_SINODIAL)  # A to B move
			#self.arrow.position = 300, 80
		elif dx > 375 and dx < 525:
			self.dx = Cx
			self.arrow.position = self.dx, 40
			move_action = Action.move_to(self.dx, 80, 1, TIMING_SINODIAL)  # A to B move
			#self.arrow.position = 450, 80
		self.arrow.run_action(move_action)
		self.dh = dh
		#all_moves.remove(self.move)
		self.tow2.append(self.tow1[len(self.tow1) - 1])
		self.tow1.remove(self.tow1[len(self.tow1) - 1])
		move_action = Action.move_to(self.dx, self.dh, v,
																															TIMING_SINODIAL)  # A to B move
		self.tow2[len(self.tow2) - 1].run_action(move_action)
		sound.play_effect('game:Ding_3')
		move_action = Action.move_to(self.dx, 80, 1, TIMING_SINODIAL)  # A to B move
		self.arrow.run_action(move_action)

	def narrow(self, dx):
		global arrow_name
		global move
		self.dx = dx
		if move == 'AC' or move == 'AB' or move == 'BC':
			arrow_name = 'ARROWUP.png'  #R
		if move == 'CA' or move == 'BA' or move == 'CB':
			arrow_name = 'ARROWUP.png'  #L
		self.arrow.remove_from_parent()
		self.arrow = SpriteNode(arrow_name)
		self.add_child(self.arrow)

		if dx > 75 and dx < 225:
			self.dx = Ax
			self.arrow.position = Ax, 40
		elif dx > 225 and dx < 375:
			self.dx = Bx
			self.arrow.position = Bx, 40
		elif dx > 375 and dx < 525:
			self.dx = Cx
			self.arrow.position = Cx, 40

	def touch_disc(self, tloc):
		self.tloc = tloc
		global A_touched
		global B_touched
		global C_touched
		if tloc > 75 and tloc < 225:
			A_touched = True
			B_touched = False
			C_touched = False
			return 'A'
		elif tloc > 225 and tloc < 375:
			A_touched = False
			B_touched = True
			C_touched = False
			return 'B'
		elif tloc > 375 and tloc < 525:
			A_touched = False
			B_touched = False
			C_touched = True
			return 'C'

	def wrong_move(self):
		global count_wrongs
		global score
		sound.play_effect('game:Error')
		#sound.play_effect('voice:female_wrong')
		count_wrongs += 1
		print('Wrongs: ', count_wrongs)
		self.arrow.position = 0, 70
		score -= 10

	def check_moves(self, t1, t2, m1, m2, tower1, tower2, x2, th2):
		self.t1 = t1
		self.t2 = t2
		self.m1 = m1
		self.m2 = m2
		self.tower1 = tower1
		self.tower2 = tower2
		self.x2 = x2
		self.th2 = th2
		global score
		if t1 == m1 and t2 == m2:
			all_moves.remove(m1 + m2)
			# print(all_moves)
			#self.update_move(m1+m2, Atower, Ctower, Cx, tCh) # 'AC'
			self.update_move(m1 + m2, tower1, tower2, x2, th2)  # 'AC'
			#th1 -= yStep	# tAh -= yStep
			#th2 += yStep	# tCh += yStep
			score += 5
			return True
		else:
			self.wrong_move()
			return False
			#self.wrong_move()
		#move_id = 0
		# self, t1, t2
	def move_discs(self, t1, t2):
		global tAh  # tower A upper disc height
		global tBh  # tower B upper disc height
		global tCh  # tower C upper disc height
		global yStep
		self.t1 = t1
		self.t2 = t2
		#global move_id
		global hands
		global count_wrongs
		global score
		global i_count
		global arrow_name
		hands += 1
		# print('hands', hands)
		# print(all_moves)
		print('tAh: ', tAh)
		print('tBh: ', tBh)
		print('tCh: ', tCh)

		for i in range(1):
			sound.play_effect('game:Woosh_2')
			if 'AC' == all_moves[0]:
				result = self.check_moves(t1, t2, 'A', 'C', Atower, Ctower, Cx, tCh)
				if result == True:
					#tAh -= yStep
					tAh = 115 + yStep * (len(Atower))
					print('+++++++++tAh: ', tAh)
					tCh += yStep
			elif 'AB' == all_moves[0]:
				result = self.check_moves(t1, t2, 'A', 'B', Atower, Btower, Bx, tBh)
				if result == True:
					#tAh -= yStep
					tAh = 115 + yStep * (len(Atower))
					tBh += yStep
			elif 'CB' == all_moves[0]:
				result = self.check_moves(t1, t2, 'C', 'B', Ctower, Btower, Bx, tBh)
				if result == True:
					tCh -= yStep
					tBh += yStep
			elif 'BA' == all_moves[0]:
				result = self.check_moves(t1, t2, 'B', 'A', Btower, Atower, Ax, tAh)
				if result == True:
					tBh -= yStep
					#tAh += yStep
					tAh = 115 + yStep * (len(Atower))
			elif 'BC' == all_moves[0]:
				result = self.check_moves(t1, t2, 'B', 'C', Btower, Ctower, Cx, tCh)
				if result == True:
					tBh -= yStep
					tCh += yStep
			elif 'CA' == all_moves[0]:
				result = self.check_moves(t1, t2, 'C', 'A', Ctower, Atower, Ax, tAh)
				if result == True:
					tCh -= yStep
					tAh += yStep
			elif 'CB' == all_moves[0]:
				result = self.check_moves(t1, t2, 'C', 'B', Ctower, Btower, Bx, tBh)
				if result == True:
					tCh -= yStep
					tBh += yStep

			#if score <= 0:
			#speech.say('Your score is  {}, you loose!'.format(score), 'en_US', .3)

			if len(all_moves) == 0:
				self.label_score.text = "Your Score is: {}, You did {} times wrong move, it did cost you {} points!".format(
					str(score), str(hands - totMoves + 1), str((hands - totMoves + 1) * 10))

				speech.say("Game is over, Your Score is: {}".format(score), 'en_US', .4)
				speech.say("You did {} times wrong move, it did cost you {} points!".format(
					str(hands - totMoves + 1), str((hands - totMoves + 1) * 10)), 'en_US', .4)
			else:
				self.label_score.text = "Score: {},  {} / {} ".format(
					str(score), str(hands + 1), str(totMoves))
			i_count += 1

	#count_move =0
	def touch_began(self, touch):
		global touch_loc
		global touch1
		global touch2
		global all_moves
		global i_count
		#global count_move
		global t_count
		touch_loc = self.point_from_scene(touch.location)
		if i_count == how_many_disc:
			i_count = -1
		sceneInst = Scene
		sound.play_effect('8ve:8ve-beep-timber')
		if i_count < how_many_disc:
			if len(all_moves) > 0:
				#self.count_move +=1
				if t_count == 1 or t_count == 0:
					touch1 = self.touch_disc(int(touch_loc[0]))
					self.narrow(int(touch_loc[0]))
					t_count = 1
				if t_count == 2:
					touch2 = self.touch_disc(int(touch_loc[0]))
					self.narrow(int(touch_loc[0]))
					self.move_discs(touch1, touch2)
				if t_count == 1:
					t_count += 1
				else:
					t_count = 1
				#self.label_score.text = "Score: " + str(score) + '    ****    ' + str(hands+1) + '/ ' + str(totMoves)


if __name__ == '__main__':
	# run(Hanoi('Hanoi'))
	# class ui.View([frame=(0, 0, 100, 100), flex='', background_color=None, name=None])
	main_view = ui.View(
		frame=(0, 0, 600, 400),
		flex='WH',
		background_color='blue',
		alpha=1,
		name='Hanoi Discs by: ismail.n@gmail.com')
	# main_view.add_subview(scene_view)
	# scene_view = SceneView(frame=main_view.bounds, flex='WH')
	sub_view = SceneView(
		frame=(0, 0, 600, 400), flex='BW', background_color='#4394c8')
	main_view.add_subview(sub_view)
	sub_view.scene = Hanoi('Hanoi')
	# main_view.present(hide_title_bar=False, animated=True)
	sub_view.size_to_fit()
	main_view.present('sheet')

