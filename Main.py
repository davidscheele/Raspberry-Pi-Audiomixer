import pygame, time, glob, random
from random import randrange, sample
from threading import Timer

currentMusicStyle = 0
musicStyleDict = {'1':'mysterium','2':'jarhead','3':'symphony'}

standardSfxPath = "./sfx/pew1.wav"

pygame.init()
pygame.mixer.init()
SCREEN = pygame.display.set_mode((1, 1))
CurrentMusicChannel = "a"
MusicChannelA = pygame.mixer.Sound("./sound/silence-1-second.wav").play()
MusicChannelB = pygame.mixer.Sound("./sound/silence-1-second.wav").play()
currentPlaylist = []

#sfx_q = pygame.mixer.Sound(standardSfxPath)
#sfx_w = pygame.mixer.Sound(standardSfxPath)
#sfx_e = pygame.mixer.Sound(standardSfxPath)
#sfx_r = pygame.mixer.Sound(standardSfxPath)
#sfx_t = pygame.mixer.Sound(standardSfxPath)
#sfx_z = pygame.mixer.Sound(standardSfxPath)
#sfx_u = pygame.mixer.Sound(standardSfxPath)
#sfx_i = pygame.mixer.Sound(standardSfxPath)
#sfx_o = pygame.mixer.Sound(standardSfxPath)
#sfx_p = pygame.mixer.Sound(standardSfxPath)
#sfx_a = pygame.mixer.Sound(standardSfxPath)
#sfx_s = pygame.mixer.Sound(standardSfxPath)
#sfx_d = pygame.mixer.Sound(standardSfxPath)
#sfx_f = pygame.mixer.Sound(standardSfxPath)
#sfx_g = pygame.mixer.Sound(standardSfxPath)
#sfx_h = pygame.mixer.Sound(standardSfxPath)
#sfx_j = pygame.mixer.Sound(standardSfxPath)
#sfx_k = pygame.mixer.Sound(standardSfxPath)
#sfx_l = pygame.mixer.Sound(standardSfxPath)

sfxDict = {'1':pygame.mixer.Sound("./sound/jarhead/sfx/rewind.wav"),
		  '2':pygame.mixer.Sound(standardSfxPath),
		  '3':pygame.mixer.Sound(standardSfxPath),
		  '4':pygame.mixer.Sound(standardSfxPath),
		  '5':pygame.mixer.Sound(standardSfxPath),
		  '6':pygame.mixer.Sound(standardSfxPath),
		  '7':pygame.mixer.Sound(standardSfxPath),
		  '8':pygame.mixer.Sound(standardSfxPath),
		  '9':pygame.mixer.Sound(standardSfxPath),
		  '10':pygame.mixer.Sound(standardSfxPath),
		  '11':pygame.mixer.Sound(standardSfxPath),
		  '12':pygame.mixer.Sound(standardSfxPath),
		  '13':pygame.mixer.Sound(standardSfxPath),
		  '14':pygame.mixer.Sound(standardSfxPath),
		  '15':pygame.mixer.Sound(standardSfxPath),
		  '16':pygame.mixer.Sound(standardSfxPath),
		  '17':pygame.mixer.Sound(standardSfxPath),
		  '18':pygame.mixer.Sound(standardSfxPath),
		  '19':pygame.mixer.Sound(standardSfxPath)}

#sfxDict = {'1':sfx_q,'2':sfx_w,'3':sfx_e,'4':sfx_r,'5':sfx_t,'6':sfx_z,'7':sfx_u,'8':sfx_i,'9':sfx_o,'10':sfx_p,'11':sfx_a,'12':sfx_s,'13':sfx_d,'14':sfx_f,'15':sfx_g,'16':sfx_h,'17':sfx_j,'18':sfx_k,'19':sfx_l}

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
	global CurrentMusicChannel
	global MusicChannelA
	global MusicChannelB
	
	loadSoundEffects(musicStyleDict[newDirection])
	currentPlaylist = getRandomPlaylistOf(musicStyleDict[newDirection])
	
	if CurrentMusicChannel == "a":
		CurrentMusicChannel = "b"
		print "Switching to B channel"
		vola = 1
		volb = 0
		MusicChannelB = pygame.mixer.Sound(getNextSongFromPlaylist()).play()
		checkTheQueue()
		while vola > 0:
			print(vola)
			vola -= 0.01
			volb += 0.01
			MusicChannelA.set_volume(vola)
			MusicChannelB.set_volume(volb)
			time.sleep(0.05)
		MusicChannelB.set_volume(1)
	else:
		CurrentMusicChannel = "a"
		print "Switching to A channel"
		volb = 1
		vola = 0
		MusicChannelA = pygame.mixer.Sound(getNextSongFromPlaylist()).play()
		checkTheQueue()
		while volb > 0:
			print(volb)
			volb -= 0.01
			vola += 0.01
			MusicChannelB.set_volume(volb)
			MusicChannelA.set_volume(vola)
			time.sleep(0.05)
		MusicChannelA.set_volume(1)
	currentMusicStyle = newDirection

def loadSoundEffects(directory):
	global sfxDict
	finaldir = "./sound/" + directory + "/sfx/*"
	counter = 1
	for result in sorted(glob.iglob(finaldir)):
		sfxDict[str(counter)] = pygame.mixer.Sound(result)
		counter += 1

def checkTheQueue():
	global currentPlaylist
	global currentMusicStyle
	if CurrentMusicChannel == "a":
		if MusicChannelA.get_queue() is None:
			print("queue empty!")
			if len(currentPlaylist) == 0:
				print("playlist was empty, makin a new one")
				currentPlaylist = getRandomPlaylistOf(musicStyleDict[currentMusicStyle])
			MusicChannelA.queue(pygame.mixer.Sound(currentPlaylist[0]))
			currentPlaylist.remove(currentPlaylist[0])
			print("done!")
	else:
		if MusicChannelB.get_queue() is None:
			print("queue empty!")
			if len(currentPlaylist) == 0:
				print("playlist was empty, makin a new one")
				currentPlaylist = getRandomPlaylistOf(musicStyleDict[currentMusicStyle])
			MusicChannelB.queue(pygame.mixer.Sound(currentPlaylist[0]))
			currentPlaylist.remove(currentPlaylist[0])
			print("done!")

while True:
	if currentMusicStyle == 0:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					fadeTo("1")
				if event.key == pygame.K_2:
					fadeTo("2")
				if event.key == pygame.K_3:
					fadeTo("3")
				if event.key == pygame.K_q:
					sfxDict['1'].play()
				if event.key == pygame.K_w:
					sfxDict['2'].play()
				if event.key == pygame.K_e:
					sfxDict['3'].play()
				if event.key == pygame.K_r:
					sfxDict['4'].play()
				if event.key == pygame.K_t:
					sfxDict['5'].play()
				if event.key == pygame.K_z:
					sfxDict['6'].play()
				if event.key == pygame.K_u:
					sfxDict['7'].play()
				if event.key == pygame.K_i:
					sfxDict['8'].play()
				if event.key == pygame.K_o:
					sfxDict['9'].play()
				if event.key == pygame.K_p:
					sfxDict['10'].play()
				if event.key == pygame.K_a:
					sfxDict['11'].play()
				if event.key == pygame.K_s:
					sfxDict['12'].play()
				if event.key == pygame.K_d:
					sfxDict['13'].play()
				if event.key == pygame.K_f:
					sfxDict['14'].play()
				if event.key == pygame.K_g:
					sfxDict['15'].play()
				if event.key == pygame.K_h:
					sfxDict['16'].play()
				if event.key == pygame.K_j:
					sfxDict['17'].play()
				if event.key == pygame.K_k:
					sfxDict['18'].play()
				if event.key == pygame.K_l:
					sfxDict['19'].play()
				if event.key == pygame.K_ESCAPE:
					breaker = True
					while breaker:
						print("Really quit?")
						for event in pygame.event.get():
							if event.type == pygame.KEYDOWN:
								if event.key == pygame.K_RETURN:
									pygame.quit()
								else:
									print("I'll break, then")
									breaker = False
									break