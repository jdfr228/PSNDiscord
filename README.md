# PSNDiscord

This is a simple web-scraping script that scrapes my.playstation.com in order to update your Discord "Now Playing" status when playing a game on PSN.

# DISCLAIMER

Usage of this script with your personal (non-bot) Discord account is technically considered "Self-botting", as it externally uses the API to update your profile. Self-botting is against Discord ToS, though some examples show that Discord is generally lenient against this (see [here](https://github.com/Favna/Discord-Self-Bot/wiki) or [here](https://github.com/discordapp/discord-api-docs/issues/69#issuecomment-223898291)).

I am not liable for any administrative or disciplinary action Discord takes against you or your account for using this script. **_USE AT YOUR OWN RISK!_**

# Installing

- Requires [Python 3.5.2](https://www.python.org/downloads/) or higher

Run the following command to install the Discord.py API wrapper

```
python -m pip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip#egg=discord.py
```

**For Windows users**: If Python is not in your system PATH, look [here](https://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/) for information on adding it.

---

Run the following command to install the Selenium webdriver for Python

```
python -m pip install -U selenium
```

---

[Download chromedriver version 2.40](https://chromedriver.storage.googleapis.com/index.html?path=2.40/) for your operating system and ensure the extracted file is in your system PATH.

- For Windows, you should be able to place it in C:/Windows, or look [here](https://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/) for instructions on how to add chromedriver's location to your PATH.

---

Modify the PSNDiscord.py script to include the necessary information:

1. **url**- The URL for your my.playstation.com user profile.  Replace "YourName" with your PSN username or simply copy the full url from a browser.

2. **dataDirectory**- Modify where you'd like to store session data for Chrome. e.g. "C:/Python/PSNDiscord/"

3. **twitchUrl**- Enter a twitch.tv profile URL if you have one.  This link will appear when in-game if someone right-clicks on your profile in Discord.

4. **userToken**- In Discord, press Ctrl+Shift+i to open the developer console.  Navigate to the "Application" tab, then under the Storage section click Local Storage -> https://discordapp.com.  Copy the value of the "token" variable under this section and paste it into the script between the quotes, replacing all x's.

   **_WARNING_: THIS TOKEN IS ESSENTIALLY YOUR DISCORD LOGIN AND PASSWORD COMBINED. DO NOT SHARE THIS TOKEN WITH ANYONE FOR ANY REASON, AND BE SURE NOT TO SHARE A VERSION OF THIS SCRIPT WITH YOUR TOKEN ALREADY ENTERED.**
   
5. hideChrome- This should be set to False on the first run so you can properly log in to Sony's website.  After successfully logging in, for future runs you can set this to True to completely hide Chrome's window.

# Usage

Windows users can simply run the included PSNDiscord.bat file.

Exit the script with a keyboard interrupt for now (Ctrl+C).

# Other parameters

- **noGameRefreshTime**- Time in seconds between each page refresh when not playing a game on PSN.  Setting this higher will reduce system usage but of course make your playing status change less frequently.
- **inGameRefreshTime**- Time in seconds between refreshes when playing a game.

  **NOTE**: Setting these two parameters lower than 50 seconds will have virtually no effect due to my.playstation.com rate limiting.  **_SETTING THEM BELOW 15 SECONDS COULD VIOLATE DISCORD API TERMS OF SERVICE AND IS NOT RECOMMENDED_**.
- **loadTime**- How long in seconds the script will wait for your profile page to load.  Slower internet connections may require a higher loadTime setting.
