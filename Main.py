import pygame, time, glob, random
from random import randrange, sample

musicstyle = 0

pygame.init()
pygame.mixer.init()
SCREEN = pygame.display.set_mode((1, 1))
currentmusicchannel = "a"

def fadeTo(newsong):
	global currentmusicchannel
	global channela
	global channelb

	if currentmusicchannel == "a":
		vola = 1
		volb = 0
		channelb = pygame.mixer.Sound(newsong).play()
		while vola > 0:
			print(vola)
			vola -= 0.1
			volb += 0.1
			channela.set_volume(vola)
			channelb.set_volume(volb)
			time.sleep(0.5)
		print("danone")
		channela.set_volume(0)
		channela.stop()
		channelb.set_volume(1)
		currentmusicchannel = "b"
	else:
		volb = 1
		vola = 0
		channela = pygame.mixer.Sound(newsong).play()
		while volb > 0:
			print(volb)
			volb -= 0.1
			vola += 0.1
			channelb.set_volume(volb)
			channela.set_volume(vola)
			time.sleep(0.5)
		print("danone")
		channelb.set_volume(0)
		channelb.stop()
		channela.set_volume(1)
		currentmusicchannel = "a"
		
def getRandomPlaylistOf(directory):
	finaldir = "./" + directory + "/*"
	playlist = []
	for result in glob.iglob(finaldir):
		playlist.insert(randrange(len(playlist)+1), result)
	return playlist

def getPlayableList(directory):
	playlist = []
	for item in directory:
		playlist.append(pygame.mixer.Sound(item))		
	return playlist
		
#sfx1 = pygame.mixer.Sound("./sfx/pew1.wav")
#sfx2 = pygame.mixer.Sound("./sfx/pew1.wav")
#sfx3 = pygame.mixer.Sound("./sfx/pew1.wav")
#sfx4 = pygame.mixer.Sound("./sfx/pew1.wav")

##pygame.mixer.music.load("./bgm/mukke1.mp3")
##muchannela = pygame.mixer.music.play()

#channela = pygame.mixer.Sound("./bgm/sonata.wav").play()
#channela.set_volume(1)
##channela.stop()
#channelb = pygame.mixer.Sound("./bgm/lullaby.wav").play()
#channelb.set_volume(0)
#channelb.stop()
#channelc = sfx3.play()
#channelc.stop()
#channeld = sfx4.play()
#channeld.stop()

alist = getPlayableList(getRandomPlaylistOf("sfx"))
print(alist)

(random.choice(alist)).play()

while True:
	if musicstyle == 0:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					fadeTo("./bgm/lullaby.wav")
#					pygame.mixer.music.load("./bgm/sonata.wav")
#					pygame.mixer.music.play()
#					musicstyle = 1
#				if event.key == pygame.K_w:
#					muchannela.stop()
				if event.key == pygame.K_r:
					fadeTo("./bgm/sonata.wav")
				if event.key == pygame.K_w:
					channelb = sfx2.play()
				if event.key == pygame.K_e:
					channelc = sfx3.play()
#					pygame.mixer.music.load("./bgm/lullaby.wav")
#					pygame.mixer.music.play()
#					musicstyle = 2	

	
#	for event in pygame.event.get():
#		if event.type == pygame.KEYDOWN:
#			if event.key == pygame.K_q:
#				channela = sfx1.play()
#			if event.key == pygame.K_w:
#				channelb = sfx2.play()
#			if event.key == pygame.K_e:
#				channelc = sfx3.play()
#			if event.key == pygame.K_r:
#				channeld = sfx4.play()
