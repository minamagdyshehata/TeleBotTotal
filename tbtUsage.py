import tbt as bot

Bot_Token = 'Your BotToken'
Chat_Id = "Your ChatID"
message = "This is a test message"
qop = "Q?,OP1,OP2,OP3"
file_path = "test.txt"
file_caption = "This is the file caption"

print(bot.SendQop(Bot_Token,Chat_Id,qop))
print(bot.SendMsg(Bot_Token,Chat_Id,message))
print(bot.SendFile(Bot_Token,Chat_Id,file_path,file_caption))

while True:
    update = bot.GetUpdates(Bot_Token)
    if update == None: #ignoring empty responses        
        pass
    else:
        DataType = update[:update.find("#")] #Extracting DataType from recieved data
        ChatID = update[update.find("#") + 1:update.find("@")] #Extracting ChatID from recieved data
        Content = update[update.find("@") + 1:] #Extracting Content from recieved update
        print(DataType)
        print(ChatID)
        print(Content)
        print()
        print()
        #BOT LOGIC HERE
