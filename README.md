Olegbot is a discord bot written in py which I hope to turn into a useful tool for language study

If you wish to use olegbot, contact me (oleg#1357) via disc

# function for command listing existing commands and descriptions\n (Not updating regularly, likely inaccurate outdated until main functions complete)
@bot.command()
async def helpme(ctx):
    embed = discord.Embed(
        title="Japanese Study Bot Commands",
        description=(
            "A list of all the available commands and their brief explanations:\n\n"
            "/newn5, /newn4, /newn3, /newn2, /newn1 - Sends a word in Japanese from levels N5-N1 respectively, "
            "with a link to jisho.org\n\n "
            "/mystudybook - Displays all words added to the user's studybook\n\n"
            "/settimer - Sets a timer for initiating a review session\n\n"
            "/timerstatus - Displays the remaining time on the timer\n\n"
            "/endtimer - Ends the currently running timer\n\n"
            "/review 5, /review 4, /review 3, /review 2, /review 1 - Initiates a review session of the words in your studybook for levels N5-N1 respective\n\n"
            "/wipe - Wipes the user's studybook\n\n"
            "/masteredwords - Displays the user's mastered words\n\n"
            "/learnedwords - Displays the words the user has correctly reviewed\n\n"
            "/songn5, /songn4, /songn3, /songn2, /songn1 - Sends a random JP song with random word from specified level in title\n\n"
            "/songfromstudybook - Sends a random JP song with random word from your studybook in the title\n\n"
            "Contact oleg#1357 on Discord if you encounter any issues."

Currently planned commands and functions:

   - /createkanjibook
    {create user's dict. to store kanji characters}
    
   - /drawkanjifrom(nX, kanjibook)
    {using html.Canvas, embed canvas in chat in which user can attempt to draw a kanji character from random in N(5,4,3,2,1) , or kanjibook}
    
   - /checkstrokeorder
    {allows user to search stroke order for specified kanji or randomkanji in: (dict.)}
    
If you have any suggestions for useful commands, kindly contact me and let me know   
    
