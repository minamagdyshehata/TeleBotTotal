import os,sys,subprocess
try:
    import requests
except: #Downloading requests module if not found
    subprocess.call("pip install --upgrade pip",shell=True)
    subprocess.call("pip install requests",shell=True)
    import requests

##Comment the next 4 lines (select then Alt+3) after running it for the first time    
##print("All required modules sucessfully downloaded")
##dummy=input("Press any key to exit..")
##sys.stdout.close()
##os._exit(0)

def Telegram_Notify(bot_message,bot_token,bot_chatID): #Sending a text msg through a telegram bot
    bot_message = bot_message.replace('+',"(PlusSign)")
    send_text = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=Markdown&text={}'.format(bot_token,bot_chatID,bot_message)
    response = requests.get(send_text)
    print(response.status_code)

def Telegram_QO(bot_message,bot_token,bot_chatID): #Sending a Question with preset answers msg through a telegram bot
    bot_message = bot_message.replace('+',"(PlusSign)")
    qolist = bot_message.split(",")
    Buttons = ''
    reply_markup = '{"keyboard":[['
    for items in qolist[1:]:
        Buttons = Buttons + '"' + items + '",'
    reply_markup = reply_markup + Buttons[:-1] + ']]}'
    send_text = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=Markdown&text={}&one_time_keyboard=False&resize_keyboard=False&reply_markup={}'.format(bot_token,bot_chatID,qolist[0],reply_markup)
    response = requests.get(send_text)
    print(response.status_code)

def Telegram_file(file,caption,bot_token,bot_chatID): #Sending a document through a telegram bot
    files = {"document":open(file,"rb")}
    file_request = 'https://api.telegram.org/bot{}/sendDocument?chat_id={}&caption={}'.format(bot_token,bot_chatID,caption)
    response = requests.post(file_request,files=files)
    print(response.status_code)

def Telegram_getfile(bot_token,file_id): #Recieving a file from a telegram bot
    PathUrl = "https://api.telegram.org/bot{}/getFile?file_id={}".format(bot_token,file_id)
    GetfileUrl = "https://api.telegram.org/file/bot{}/".format(bot_token)
    resp_PathUrl = requests.get(PathUrl)
    data_PathUrl = resp_PathUrl.json()
    Path = data_PathUrl["result"]["file_path"]
    file_name = Path[Path.find("/") + 1:]
    resp_GetfileUrl = requests.get(GetfileUrl + Path,allow_redirects=True)
    open(file_name, 'wb').write(resp_GetfileUrl.content)
    return file_name
    
Bot_token = ''
if len(sys.argv) == 2:
    if sys.argv[1] == "-h" or sys.argv[1] == "--help" or sys.argv[1] == "/?": #Showing help menu
        print("{}-h or --help                                              Show help menu.{}".format(chr(10),chr(10))+
              "<BotToken>                                                Gets the next update.{}".format(chr(10))+
              "<BotToken> msg <ChatID> <TextMessage>                     Sends a text message to a specific Chat ID.{}".format(chr(10))+
              "<BotToken> qop <ChatID> <Question,Option1,Option2,..>     Sends a question with options for answers to a specific Chat ID.{}".format(chr(10))+
              "<BotToken> doc <ChatID> <FilePath>                        Sends a document to a specific Chat ID.{}".format(chr(10)))
        sys.stdout.close()
        os._exit(0)
    else:
        Bot_token = sys.argv[1] #assigning the BotToken to a string variable
if len(sys.argv) > 2:
    try: #Checking if the user want to send a text msg or a document
        Bot_token = sys.argv[1]
        if sys.argv[2] == "msg": #Text msg
            ChatID = sys.argv[3]
            message = ''
            for item in sys.argv[4:]:
                message = message + item + " "
            Telegram_Notify(message,Bot_token,ChatID)
            sys.stdout.close()
            os._exit(0)
        elif sys.argv[2] == "qop": #Question with options
            ChatID = sys.argv[3]
            message = ''
            for item in sys.argv[4:]:
                message = message + item + " "
            Telegram_QO(message,Bot_token,ChatID)
            sys.stdout.close()
            os._exit(0)
        elif sys.argv[2] == "doc": #Document
            ChatID = sys.argv[3]
            FilePath = sys.argv[4]
            Telegram_file(FilePath,"",Bot_token,ChatID)
            sys.stdout.close()
            os._exit(0)
        else:
            print("Unrecognized command!!{}Please check the help menu..{}{}".format(chr(10),chr(10),chr(10))) #Unrecognized command error msg
            sys.stdout.close()
            os._exit(0)
    except Exception as error:
        print (error)
        print("Something went wrong!!{}Please check the help menu..{}{}".format(chr(10),chr(10),chr(10))) #Something went wrong error msg (request failed due to wrong Token for example)
        sys.stdout.close()
        os._exit(0)

getUpdates_url = 'https://api.telegram.org/bot{}/getUpdates'.format(Bot_token) #getupdates URL

try:
    DataType = ""
    resp_getUpdates = requests.get(getUpdates_url)
    data_getUpdates = resp_getUpdates.json()
    for item in data_getUpdates["result"]: #offset request (offset=update_id+1)
        offset = item["update_id"]
        offset += 1
        offset_url = 'https://api.telegram.org/bot{}/getUpdates?offset={}'.format(Bot_token,offset)
        offset_adjust_resp = requests.get(offset_url)

        chat_id = str(item["message"]["chat"]["id"]) #Getting the ChatID (each person contacting the bot has a unique ChatID)

        try:
                if DataType == "":
                    file_id = item["message"]["voice"]["file_id"] #Checking if voice msg recieved
                    DataType = "voice"
                    print("{}#{}@{}".format(DataType,chat_id,Telegram_getfile(Bot_token,file_id))) #Downloading the voice msg file and getting its name
        except:
            pass

        try:
                if DataType == "":
                    file_id = item["message"]["photo"][3]["file_id"] #Checking if photo recieved
                    DataType = "photo"
                    print("{}#{}@{}".format(DataType,chat_id,Telegram_getfile(Bot_token,file_id))) #Downloading the photo file and getting its name
        except:
            pass

        try:
                if DataType == "":
                    file_id = item["message"]["video"]["file_id"] #Checking if video recieved
                    DataType = "video"
                    print("{}#{}@{}".format(DataType,chat_id,Telegram_getfile(Bot_token,file_id))) #Downloading the video file and getting its name
        except:
            pass

        try:
                if DataType == "":
                    file_id = item["message"]["audio"]["file_id"] #Checking if audio recieved
                    DataType = "audio"
                    print("{}#{}@{}".format(DataType,chat_id,Telegram_getfile(Bot_token,file_id))) #Downloading the audio file and getting its name
        except:
            pass

        try:
                if DataType == "":
                    file_id = item["message"]["document"]["file_id"] #Checking if document recieved
                    DataType = "document"
                    print("{}#{}@{}".format(DataType,chat_id,Telegram_getfile(Bot_token,file_id))) #Downloading the document file and getting its name
        except:
            pass

        try:
                if DataType == "":
                    lat = item["message"]["location"]["latitude"] #Checking if latitude recieved
                    lon = item["message"]["location"]["longitude"] #Checking if longitude recieved
                    DataType = "location"
                    print("{}#{}@{},{}".format(DataType,chat_id,lat,lon))
        except:
            pass

        try:
                UNICODE = False
                if DataType == "":
                    message = item["message"]["text"] #Recieving a text msg
                    for letters in message: #Checking if the msg is in Unicode
                        if ord(letters) >= 127:
                            UNICODE = True
                            break
                    if UNICODE: #Formatting the msg if in Unicode in the form of <BotToken>[ASCII1,ASCII2,....]
                        UNICODEmsg = Bot_token + "["
                        for letter in message:
                            if ord(letter) >= 1632 and ord(letter) <= 1641:
                                UNICODEmsg = UNICODEmsg + str(ord(letter) - 1584) + ","
                            else:
                                UNICODEmsg = UNICODEmsg + str(ord(letter)) + ","
                        UNICODEmsg = UNICODEmsg [:-1] + "]"
                        message = UNICODEmsg
                    DataType = "text"
                    print("{}#{}@{}".format(DataType,chat_id,message))
        except:
            pass
except Exception as error:
    print(error)
    pass

sys.stdout.close()
os._exit(0)
