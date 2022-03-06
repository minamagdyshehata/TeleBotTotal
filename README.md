## TeleBotTotal
A python module that makes it easy to build a telegram bot.

I am a big fan of telegram bots and that is why I wrote that module, hoping that it helps other programmers to built their own bots.

tbt.py can be imported to any python script to use it's functions as shown in tbtUsage.py.

it returns the update whether it's text,contact,voice,video,audio,location,document or photo.

It can also send a text messages, Qop or a documents to a specific Chat ID.

Here are the functions :

              
              GetUpdates(Bot_Token)                                 Gets the next update.
              
              SendMsg(Bot_Token,Chat_Id,message)                    Sends a text message to a specific Chat ID.
              
              SendQop(Bot_Token,Chat_Id,qop)                        Sends a question with options to a specific Chat ID. qop is in the form of "Q?,OP1,OP2,.."    
              
              SendFile(Bot_Token,Chat_Id,file_path,file_caption)    Sends a document to a specific Chat ID.
              
                

The module will always return the update in the following form:
 
             DataType#ChatID@Content

Content will be the file name saved in the same directory if the DataType is [photo,contact,video,audio,document or voice].

Content will be in the form of lat,lon if the DataType is [location].

Content will be the actual text message if the DataType is [text].

I also wrote the same module in VB.net as tbt.dll, with the same functions. tbt.dll can be added as a reference in visual studio to be used.

In visual studio you might need to install Newtonsoft.Json by going to Tools>>NuGet Package Manager>>Package Manager Console then type:

             install-package Newtonsoft.Json
             
then hit Enter, this package is needed to allow tbt.dll to deal with data in JSON format.

You will also find a VB.net project of my version of a Telegram Bot interface that uses tbt.dll on the following link, feel free to modify as per your needs.

  [MyTeleBotVB.NET on GoogleDrive](https://drive.google.com/file/d/1ym0Utu9UKmrwzkKgIEbjsghkJVdj2Fc3/view?usp=sharing)
  
Inside the VB.net project folder you will find a folder named "FinalPublish" that contains a standalone version of the EXE file.

If you find this project helpful, i will really appreciate you donation on my PayPal:
  
  [![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/donate?hosted_button_id=29JX5NN5E6BAS)


Happy Programming :):)

        
