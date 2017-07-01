from __future__ import division, print_function
from keras.models import load_model
from keras.optimizers import Adam
from scipy.misc import imresize
import numpy as np
import os
import wrapped_game

def preprocess_images(images):
	
	if images.shape[0] < 4:
		# single image case
		x_t = images[0]
		x_t = imresize(x_t,(62,80))
		x_t = x_t.astype('float')
		x_t /= 255.0
		s_t = np.stack((x_t,x_t,x_t,x_t),axis=2)
	
	else:
		# 4 images
		xt_list = []
		for i in range(images.shape[0]):
			x_t = imresize(images[i],(62,80))
			x_t = x_t.astype('float')
			x_t /= 255.0
			xt_list.append(x_t)
		s_t = np.stack((xt_list[0],xt_list[1],xt_list[2],xt_list[3]),axis=2)

	s_t = np.expand_dims(s_t,axis=0)
	return s_t


# load the AI model
DATA_DIR = 'data'
model = load_model(os.path.join(DATA_DIR,'RL_SAVE_ME_GAME_AI_MODEL.h5'))
model.compile(optimizer=Adam(lr=1e-6),loss='mse')

game = wrapped_game.save_me()

num_games, num_wins = 0,0

for e in range(100):
	game.reset()

	# get first state
	a_0 = 1 
	x_t, r_0, game_over = game.step(a_0)
	s_t = preprocess_images(x_t)

	while not game_over:
		s_tm1 = s_t

		# next action
		q = model.predict(s_t)[0]
		a_t = np.argmax(q)

		# apply action, get reward
		x_t,r_t,game_over = game.step(a_t)
		s_t = preprocess_images(x_t)
		print(r_t)
		# if reward, increment num_wins
		if r_t == 1:
			num_wins += 1
	num_games+=1
	print("Total Games : %d | Total Wins : %d"%(num_games,num_wins))
