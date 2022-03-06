import os,sys,subprocess
try:
    import requests
except: #Downloading requests module if not found
    subprocess.call("pip install --upgrade pip",shell=True)
    subprocess.call("pip install requests",shell=True)
    import requests

def SendMsg(bot_token,bot_chatID,bot_message): #Sending a text msg through a telegram bot
    bot_message = bot_message.replace('+',"(PlusSign)")
    send_text = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=Markdown&text={}'.format(bot_token,bot_chatID,bot_message)
    response = requests.get(send_text)
    if response.status_code == 200:
        return "Message sent to ChatID: {}".format(bot_chatID)
    else:
        return "failed"

def SendQop(bot_token,bot_chatID,bot_message): #Sending a Question with preset answers msg through a telegram bot
    bot_message = bot_message.replace('+',"(PlusSign)")
    qolist = bot_message.split(",")
    Buttons = ''
    reply_markup = '{"keyboard":[['
    for items in qolist[1:]:
        Buttons = Buttons + '"' + items + '",'
    reply_markup = reply_markup + Buttons[:-1] + ']]}'
    send_text = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=Markdown&text={}&one_time_keyboard=False&resize_keyboard=False&reply_markup={}'.format(bot_token,bot_chatID,qolist[0],reply_markup)
    response = requests.get(send_text)
    if response.status_code ==200:
        return "Qop sent to ChatID: {}".format(bot_chatID)
    else:
        return "failed"

def SendFile(bot_token,bot_chatID,file,caption): #Sending a document through a telegram bot
    try:
        files = {"document":open(file,"rb")}
    except:
        return "file not found"
    file_request = 'https://api.telegram.org/bot{}/sendDocument?chat_id={}&caption={}'.format(bot_token,bot_chatID,caption)
    response = requests.post(file_request,files=files)
    if response.status_code == 200:
        return "File sent to ChatID: {}".format(bot_chatID)
    else:
        return "failed"

def GetFile(bot_token,file_id): #Recieving a file from a telegram bot
    PathUrl = "https://api.telegram.org/bot{}/getFile?file_id={}".format(bot_token,file_id)
    GetfileUrl = "https://api.telegram.org/file/bot{}/".format(bot_token)
    resp_PathUrl = requests.get(PathUrl)
    data_PathUrl = resp_PathUrl.json()
    Path = data_PathUrl["result"]["file_path"]
    file_name = Path[Path.find("/") + 1:]
    resp_GetfileUrl = requests.get(GetfileUrl + Path,allow_redirects=True)
    open(file_name, 'wb').write(resp_GetfileUrl.content)
    return file_name
       
def GetUpdates(Bot_token):
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
                        return "{}#{}@{}".format(DataType,chat_id,GetFile(Bot_token,file_id)) #Downloading the voice msg file and getting its name
            except:
                pass

            try:
                    if DataType == "":
                        file_id = item["message"]["photo"][3]["file_id"] #Checking if photo recieved
                        DataType = "photo"
                        return "{}#{}@{}".format(DataType,chat_id,GetFile(Bot_token,file_id)) #Downloading the photo file and getting its name
            except:
                pass

            try:
                    if DataType == "":
                        file_id = item["message"]["video"]["file_id"] #Checking if video recieved
                        DataType = "video"
                        return "{}#{}@{}".format(DataType,chat_id,GetFile(Bot_token,file_id)) #Downloading the video file and getting its name
            except:
                pass

            try:
                    if DataType == "":
                        file_id = item["message"]["audio"]["file_id"] #Checking if audio recieved
                        DataType = "audio"
                        return "{}#{}@{}".format(DataType,chat_id,GetFile(Bot_token,file_id)) #Downloading the audio file and getting its name
            except:
                pass

            try:
                    if DataType == "":
                        file_id = item["message"]["document"]["file_id"] #Checking if document recieved
                        DataType = "document"
                        return "{}#{}@{}".format(DataType,chat_id,GetFile(Bot_token,file_id)) #Downloading the document file and getting its name
            except:
                pass

            try:
                    if DataType == "":
                        lat = item["message"]["location"]["latitude"] #Checking if latitude recieved
                        lon = item["message"]["location"]["longitude"] #Checking if longitude recieved
                        DataType = "location"
                        return "{}#{}@{},{}".format(DataType,chat_id,lat,lon)
            except:
                pass

            try:
                    if DataType == "":
                        first_name = ""
                        last_name = ""
                        try:
                            first_name = item["message"]["contact"]["first_name"] #Checking if first_name recieved
                        except:
                            pass
                        try:
                            last_name = item["message"]["contact"]["last_name"] #Checking if last_name recieved
                        except:
                            pass
                        vcard = item["message"]["contact"]["vcard"] #Checking if vcard recieved
                        vcf_file = first_name.replace(" ","") + last_name.replace(" ","") + ".vcf"
                        f = open(vcf_file, "w")
                        f.write(vcard)
                        f.close()
                        DataType = "contact"
                        return "{}#{}@{}".format(DataType,chat_id,vcf_file)
            except:
                pass

            try:
                    UNICODE = False
                    if DataType == "":
                        message = item["message"]["text"] #Recieving a text msg
                        for letters in message: #Checking if the msg is in Unicode
                            if ord(letters) > 127:
                                UNICODE = True
                                break
                        if UNICODE: 
                            UNICODEmsg = ""
                            for letter in message:
                                if ord(letter) >= 1632 and ord(letter) <= 1641:
                                    UNICODEmsg = UNICODEmsg + chr(ord(letter) - 1584)
                                else:
                                    UNICODEmsg = UNICODEmsg + letter
                            message = UNICODEmsg
                        DataType = "text"
                        return "{}#{}@{}".format(DataType,chat_id,message)
            except:
                pass
    except Exception as error:
        return str(error)
        pass


