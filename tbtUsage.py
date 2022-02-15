import subprocess
Bot_Token = 'You Telegram Bot Token Here'

while True:
    out = subprocess.check_output("python tbt.py {}".format(Bot_Token), shell=True)#calling BotTotal.py from command line with the BotToken as an argument
    if out.decode() == '': #ignoring empty responses        
        pass
    else:
        data = out.decode() #Converting recieved data fromByte to String
        DataType = data[:data.find("#")] #Extracting DataType from recieved data
        ChatID = data[data.find("#") + 1:data.find("@")] #Extracting ChatID from recieved data
        Content = data[data.find("@") + 1:-2] #Extracting Content from recieved data
        ####for unicode msgs:
        if Content.startswith(Bot_Token): #Checking that Content Starts with the Bot_Token
            unicode = Content[len(Bot_Token)+1:-1] #Extracting the ASCII values of the unicode characters
            unicodelis = unicode.split(",") #Splittling ASCII values in a list
            Content = ""
            for items in unicodelis: #Converting ASCII to unicode characters
                Content = Content + chr(int(items))
        #Data output
        print(DataType)
        print(ChatID)
        print(Content)
        print()
        print()
