import discord
import asyncio
import time
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Modify for your needs -------------------------------------------------------
url = "https://my.playstation.com/profile/YourName"
dataDirectory = "C:/PSNDiscord"
twitchUrl = "https://www.twitch.tv/YourName"
userToken = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
hideChrome = False

noGameRefreshTime = 60		# WARNING - Setting below 15 seconds could violate Discord API ToS
inGameRefreshTime = 120		# WARNING
							# NOTE - Sony servers only allow ~1.3 requests per minute regardless, so setting these
							#        lower than ~50 seconds will have limited practical effect
loadTime = 5

# -----------------------------------------------------------------------------


alreadyFetched = False
gameName = ""
oldGameName = ""
imageSrc = ""
gameUrl = ""
console = ""
driver = None
client = None
clientReady = False
refreshTime = 5

async def resetNowPlaying():
	global gameName, oldGameName, imageSrc, gameUrl, console
	gameName = ""
	imageSrc = ""
	gameUrl = ""
	console = ""

	if (oldGameName != gameName):
		print("No longer playing a game")
		await updatePresence()
		oldGameName = ""


def chromeSetup():
	global driver, dataDirectory, hideChrome

	# Set up Chrome options
	chrome_opts = Options()
	chrome_opts.set_headless(headless=hideChrome)								# Set up headless
	chrome_opts.add_argument('no-sandbox')										# --
	chrome_opts.add_argument("user-data-dir=" + dataDirectory)					# Set up session saving (cookies)
	chrome_opts.add_argument("proxy-server=direct://")							# Make headless not unbearably slow
	chrome_opts.add_argument("proxy-bypass-list=*")								# --
	chrome_opts.add_argument("disable-extensions")								# --
	chrome_opts.add_argument("hide-scrollbars")									# --
	chrome_opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36")
	chrome_opts.add_argument("log-level=3")										# Hide console messages

	print("Setting up web driver...")
	driver = webdriver.Chrome(chrome_options=chrome_opts)
	print("Web driver set up")
	driver.get("http://google.com/")


async def refreshThread():
	global refreshTime

	while True:
		await fetchPage()
		await asyncio.sleep(refreshTime)		# Wait between page fetches

async def fetchPage():
	global gameName, oldGameName, imageSrc, gameUrl, console, alreadyFetched, refreshTime, noGameRefreshTime, inGameRefreshTime, loadTime

	# Fetch page, or if it has already been fetched before, simply refresh
	if (alreadyFetched):
		#driver.refresh()
		driver.find_element_by_tag_name('body').send_keys(Keys.F5)
		print("Page Refreshing " + time.strftime("%I:%M:%S", time.localtime()))
		refreshTime = noGameRefreshTime
	else:
		driver.get(url)
		print("Page Fetching " + time.strftime("%I:%M:%S", time.localtime()))

	# Wait for page to load and fetch game info
	try:
		gameNameElem = WebDriverWait(driver, loadTime).until(EC.presence_of_element_located((By.CLASS_NAME, 'now-playing__details__line1__name')))	# Name
		imageElem = WebDriverWait(driver, loadTime).until(EC.presence_of_element_located((By.CLASS_NAME, 'now-playing__thumbnail')))   			# Image
		gameUrlElem = WebDriverWait(driver, loadTime).until(EC.presence_of_element_located((By.CLASS_NAME, 'now-playing__details__store-link')))	# Url
		consoleElem = WebDriverWait(driver, loadTime).until(EC.presence_of_element_located((By.CLASS_NAME, 'now-playing__details__line1')))		# Console

		#if (gameNameElem is not None):
		gameName = gameNameElem.text

		# DOM differs between PS3/No Game and PS4 games
		try:
			imageSrc = imageElem.find_element_by_tag_name('img').get_attribute('src')	# PS4
		except:
			try:
				imageSrc = imageElem.find_element_by_tag_name('span').text 				# PS3 or no game
			except:
				print("Cannot resolve image")

		gameUrl = gameUrlElem.find_element_by_tag_name('a').get_attribute('href')
		console = consoleElem.find_element_by_tag_name('div').get_attribute('aria-label')


		# If no game is being played reset now playing status
		if (gameName == ""):
			await resetNowPlaying()

	    # If all the try statements have executed and the game name is new, update Discord's status
		elif (gameName != oldGameName):
			print("Now playing a game")
			if (alreadyFetched):
				refreshTime = inGameRefreshTime		# Wait longer between page refreshes when in-game
			await updatePresence()
			oldGameName = gameName

	except TimeoutException:
		print("Profile page timeout")
	except AttributeError:
		traceback.print_exc()
	except NoSuchElementException:
		print("Elements not found, or page has not loaded properly")
		await resetNowPlaying()

	alreadyFetched = True 							# Ensure the page simply refreshes the second time this is run


def runDiscord(client):
	global userToken

	@client.event
	async def on_ready():
		global clientReady

		print('Logged into Discord as')
		print(client.user.name)
		print(client.user.id)
		print('-----')
		clientReady = True

	client.run(userToken, bot=False)

# Called to update the "Now Playing" status in Discord
async def updatePresence():
	global gameName, gameUrl, imageSrc, console, client, clientReady, twitchUrl

	if (clientReady):
		#applicationId = ""
		timestampsDict = {"start": int(time.time()) * 1000}

		print("Updating Discord status...")
		await client.change_presence(activity=discord.Activity(#application_id=applicationId,
																name=gameName,
																#details=gameUrl,
																url=twitchUrl,
																type=discord.ActivityType.playing,
																state="In-Game (" + console + ")",
																timestamps=timestampsDict))
	else:
		print("Client not yet ready, cannot update status")
		await resetNowPlaying()


def main():
	global client

	chromeSetup()

	# Set up the thread for refreshing the webpage
	loop = asyncio.get_event_loop()
	loop.create_task(refreshThread())

	# Set up Discord
	client = discord.Client()
	runDiscord(client)

main()