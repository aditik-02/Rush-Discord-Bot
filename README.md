Rush — Discord Cafe Bot  
========================

Rush is a Python-based Discord bot that helps users discover cafes using the Yelp Academic Dataset. It supports smart search, real-time availability, and personalized features like saving favorite spots. Built with `discord.py`, it offers a friendly command interface for city-based suggestions, mood-based recommendations, and geolocation-based discovery.

Features  
--------

- Search cafes by city, price, vibe, or location  
- Show currently open cafes based on system time  
- Save and view your personal list of favorite cafes  
- Display top-rated cafes in a city  
- Quick lookup by cafe name or coordinates  

Commands  
--------

| Command                    | Who Can Use It | Description                                                   |
|---------------------------|----------------|---------------------------------------------------------------|
| !cafe <city>              | Any user       | Suggest a random cafe in the given city                       |
| !topcafes <city>          | Any user       | Show top-rated cafes in the specified city                    |
| !recommend <city> <mood>  | Any user       | Recommend a cafe by mood (e.g. casual, romantic, trendy)      |
| !cafebyprice <city> <1-4> | Any user       | List cafes by price level (1 = cheap, 4 = expensive)          |
| !opennow <city>           | Any user       | Display currently open cafes in the given city                |
| !search <name>            | Any user       | Find a cafe by name                                           |
| !nearby <lat> <lon>       | Any user       | Find cafes near a specific geographic location                |
| !savecafe <name>          | Any user       | Save a cafe to your personal favorites list                   |
| !mycafes                  | Any user       | View your saved cafes                                         |
| !help                     | Any user       | View the help menu                                            |

Setup Instructions  
------------------

1. **Clone the Repository**  
   git clone https://github.com/aditik-02/Rush-Discord-Bot.git
   `cd Rush-Discord-Bot`

2. **Install Dependencies**  
   Ensure Python 3.10+ is installed. Then run:  
   `pip install -r requirements.txt`

3. **Set Up Your Environment**  
   Create a `.env` file in the root directory and add your Discord bot token:  
   DISCORD_TOKEN=bot-token-here

4. **Load Dataset**  
   Make sure the `data/` directory contains `yelp_academic_dataset_business.json` with valid cafe data (ideally under 100 MB).

5. **Run the Bot**  
   `python main.py`

Logging & Storage  
-----------------

- User favorites are saved in `data/saved_cafes.json`.  
- The dataset is filtered to only include cafes that are open and contain valid metadata.  
- Google Maps links are embedded in responses for easy access from Discord.  

Notes  
-----

- Built using `discord.py`, `python-dotenv`, and Python standard libraries.  
- `!opennow` uses system time to suggest currently open cafes.  
- `!recommend` supports mood-based filtering using Yelp’s Ambience attributes.  
- All commands return clean and easy-to-read suggestions via Discord messages.
