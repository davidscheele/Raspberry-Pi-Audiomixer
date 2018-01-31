import pygame, time, glob, random, os
from random import randrange, sample
from collections import defaultdict

currentMusicStyle = "0"

def loadMusicStyles():	
	with open('./musicstyleorder') as file:
		musicStyleDict = {}
		counter = 1
		for line in file:
			if line[0] != "#":
				line = line.replace("\n", "")
				musicStyleDict[str(counter)] = line
				counter += 1
	print(musicStyleDict)
	return musicStyleDict

musicStyleDict = loadMusicStyles()
maxMusicVolume = 0.5

warnSound = "./warning.ogg"

pygame.init()
pygame.display.set_caption('super-mc-audiomix')
pygame.mixer.init()
SCREEN = pygame.display.set_mode((1, 1))
currentMusicChannel = "a"
musicChannelA = pygame.mixer.Sound("./silence-1-second.wav").play()
musicChannelB = pygame.mixer.Sound("./silence-1-second.wav").play()
currentPlaylist = []
sfxDict = defaultdict(list)

def getRandomPlaylistOf(directory):
	finaldir = "./sound/" + directory + "/bgm/*"
	playlist = []
	for result in glob.iglob(finaldir):
		playlist.insert(randrange(len(playlist)+1), result)
	return playlist

def getNextSongFromPlaylist():
	global currentPlaylist
	chosenTitle = currentPlaylist[0]
	currentPlaylist.remove(currentPlaylist[0])
	return chosenTitle

def fadeTo(newDirection):
	global currentPlaylist
	global currentMusicChannel
	global musicChannelA
	global musicChannelB
	global currentMusicStyle
	
	print("getting all the stuff")
	
	loadSoundEffects(musicStyleDict[newDirection])
	currentPlaylist = getRandomPlaylistOf(musicStyleDict[newDirection])
	
	print("here we fade...")
	
	if currentMusicChannel == "a":
		currentMusicChannel = "b"
		print "Switching to B channel"
		vola = maxMusicVolume
		volb = 0
		musicChannelB = pygame.mixer.Sound(getNextSongFromPlaylist()).play()
		musicChannelB.pause()
		checkTheQueue()
		musicChannelB.unpause()
		while vola > 0:
			print(vola)
			vola -= 0.01
			volb += 0.01
			musicChannelA.set_volume(vola)
			musicChannelB.set_volume(volb)
			time.sleep(0.03)
		musicChannelB.set_volume(maxMusicVolume)
	else:
		currentMusicChannel = "a"
		print "Switching to A channel"
		volb = maxMusicVolume
		vola = 0
		musicChannelA = pygame.mixer.Sound(getNextSongFromPlaylist()).play()
		musicChannelA.pause()
		checkTheQueue()
		musicChannelA.unpause()
		while volb > 0:
			print(volb)
			volb -= 0.01
			vola += 0.01
			musicChannelB.set_volume(volb)
			musicChannelA.set_volume(vola)
			time.sleep(0.05)
		musicChannelA.set_volume(maxMusicVolume)
	currentMusicStyle = newDirection

def loadSoundEffects(directory):
	global sfxDict
	print("loading sfx for ")
	print(directory)
	sfxDict = defaultdict(list)
	finaldir = "./sound/" + directory + "/sfx/"
	for item in glob.iglob(finaldir + "*"):
		item = item.replace(finaldir, "")
		print(item)
		sfxDict[item[0]].append(item)

def checkTheQueue():
	global currentPlaylist
	global currentMusicStyle
	if currentMusicChannel == "a":
		if musicChannelA.get_queue() is None:
			print("queue empty!")
			if len(currentPlaylist) == 0:
				print("playlist was empty, makin a new one")
				currentPlaylist = getRandomPlaylistOf(musicStyleDict[currentMusicStyle])
			musicChannelA.queue(pygame.mixer.Sound(currentPlaylist[0]))
			currentPlaylist.remove(currentPlaylist[0])
			print("done!")
	else:
		if musicChannelB.get_queue() is None:
			print("queue empty!")
			if len(currentPlaylist) == 0:
				print("playlist was empty, makin a new one")
				currentPlaylist = getRandomPlaylistOf(musicStyleDict[currentMusicStyle])
			musicChannelB.queue(pygame.mixer.Sound(currentPlaylist[0]))
			currentPlaylist.remove(currentPlaylist[0])
			print("done!")

def playByKey(key):
	global sfxDict
	global musicStyleDict
	global currentMusicStyle
	if currentMusicStyle != "0":
		if key in sfxDict:
			sfxToPlay = "./sound/" + musicStyleDict[currentMusicStyle] + "/sfx/" + random.choice(sfxDict[key])
			print("I'll play...")
			print(sfxToPlay)
			pygame.mixer.Sound(sfxToPlay).play()
		else:
			pygame.mixer.Sound(warnSound).play()
			print("I have nothing for this key...")
			print(key)
	else:
		pygame.mixer.Sound(warnSound).play()
		print("No soundeffects before you switch to some music!")
		
def turnMusicUp():
	global maxMusicVolume
	global currentMusicChannel
	global musicChannelA
	global musicChannelB
	if maxMusicVolume < 0.99:
		vol = maxMusicVolume
		maxMusicVolume += 0.1		
		if currentMusicChannel == "a":
			while vol < maxMusicVolume:
				print(vol)
				vol += 0.01
				musicChannelA.set_volume(vol)
				time.sleep(0.03)
		else:
			while vol < maxMusicVolume:
				print(vol)
				vol += 0.01
				musicChannelB.set_volume(vol)
				time.sleep(0.03)
		print("setting to" + str(maxMusicVolume))
		musicChannelA.set_volume(maxMusicVolume)
	else:
		print("Volume is already at 100%!")
		
def turnMusicDown():
	global maxMusicVolume
	global currentMusicChannel
	global musicChannelA
	global musicChannelB
	if maxMusicVolume > 0.01:
		vol = maxMusicVolume
		maxMusicVolume -= 0.1		
		if currentMusicChannel == "a":
			while vol > maxMusicVolume:
				print(vol)
				vol -= 0.01
				musicChannelA.set_volume(vol)
				time.sleep(0.03)
		else:
			while vol > maxMusicVolume:
				print(vol)
				vol -= 0.01
				musicChannelB.set_volume(vol)
				time.sleep(0.03)
		musicChannelA.set_volume(maxMusicVolume)
	else:
		print("Volume is already at 0%!")

while True:
	os.system("wmctrl -a super-mc-audiomix")
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if pygame.key.name(event.key) in musicStyleDict:
				fadeTo(pygame.key.name(event.key))
			elif event.key == pygame.K_MINUS:
				turnMusicDown()
			elif event.key == pygame.K_PLUS:
				turnMusicUp()
			elif event.key == pygame.K_ESCAPE:
				breaker = True
				print("Really quit? Enter to quit!")
				while breaker:
					for event in pygame.event.get():
						if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_RETURN:
								pygame.quit()
							else:
								print("I'll break, then")
								breaker = False
								break
			else:
				playByKey(pygame.key.name(event.key))