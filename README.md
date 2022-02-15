## TeleBotTotal
A python tool that makes it easy to build a telegram bot.

I am a big fan of telegram bots and that is why I wrote that tool, hoping that it helps other programmers to built their own bots in whatever language they prefer.

My idea is to call tbt.py via command line with the Bot_Token as an argument and it returns the update weather it's text,voice,document or photo.

It can also send a text messages or a documents to a specific Chat ID.

Here is the help menu :

              -h or --help                             Show help menu.
              
              <BotToken>                               Gets the next update.
              
              <BotToken> msg <ChatID> <TextMessage>    Sends a text message to a specific Chat ID.
              
              <BotToken> doc <ChatID> <FilePath>       Sends a document to a specific Chat ID.
              
                
To use the script for the first time, run it without any arguments as it will check for needed modules and download anything that is missing. Then you can comment lines 10,11,12 and 13.

The tool will always return the update in the following form:
 
             DataType#ChatID@Content

Content will be the file name saved in the same directory if the DataType is [photo,document or voice].

Content will be the actual text message if the DataType is [text].

Incase the recieved text contains a unicode character the returned update will look like that:

            DataType#ChatID@Bot_Token[ASCII1,ASCII2,ASCII3,....]
            
then some string manipulation will be needed to retrieve the unicode message.

I wrote another script using tbt.py to recieve all updates recieved by a telegram bot. I also explained step by step how to retrieve a unicode message (You can do the same algorithm with your prefered programming language).

I hope this tool makes it eazier for everyone to built their own Telegram bots. Enjoy!!

        
