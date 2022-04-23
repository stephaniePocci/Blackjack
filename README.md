# Blackjack
## This is a simple in-console Blackjack game I developed for my game development class.
### <p> How To Download This Repository: </p>
1) Download the repository to your local files:
- Click the green-highlighted button that says **Code**
- From the drop-down, copy & paste the URL given.
- In your command terminal, navigate to the location you desire to download it.
> - Type **ls** to see which folders you can access.
> - Type **cd <FolderName>** without the <> to access the folder.
> - Type **cd ..** to go back a folder.
- Use the command **git clone <URL here>** without the <>.
- If you are getting an error, you may have to download the git clone command first.
> - To do so, navigate to the folder you would like to download it to and type **$ sudo apt-get update**.
> - Then, type **$ sudo apt-get install git**.
> - To verify it has been downloaded, type **$ git --version** to view the version type you have downloaded.
> - If the download was unsuccessful, you will instead get an error saying it was unable to be found.
2) Navigate into the project folder:
- In the command terminal, use **cd <FolderName>** without the <> to access the Blackjack folder.
- You should see a file labeled blackjack.py.
3) Run the game: 
- If the blackjack.py file is not bolded, you will need to compile it.
> - You can compile this by typing **chmod u+x blackjack.py**.
> - If it is already bolded, you may now run the game by typing **./blackjack.py** in your command terminal.
### <p> How To Run Blackjack: </p>
##### In your command terminal, type './blackjack.py' after navigating into the Blackjack repository folder.
### <p> Rules: </p>
- You must use a keyboard to play.
- There is at least one player playing.
- All players start with $10,000 in their bank balance.
- You may double-down, get insurance, and split on both hands.
### <p> About This Project: </p>
This is a simple Blackjack simulator I made in approximately 40 hours for a game development class. The program runs in-console and is entirely made with Python. This Blackjack game has an AI dealer (HAL9000) and can be used in both single-player and multi-player mode. At the end of each mode (if you decide to not continue playing), each of the player's data is saved in the database file (pickle_database.pckl). You can get your player data back by simply typing the same name again when inputting players during a new game.
