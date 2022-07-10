import telebot
import requests

# changes made on 10/7 3.32pm to mask out telegram API key
TELEGRAM_API_KEY="YOUR API KEY"
OCR_SPACE_API_KEY="YOUR OCR KEY"

bot = telebot.TeleBot(f'{TELEGRAM_API_KEY}', parse_mode=None) 

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Kindly send your receipt and we will extract out the relevant food items for you:)")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Try sending me an image with text in it.")

@bot.message_handler(content_types=['photo'])
def handle_image(message):
    # Get the file_id of the uploaded photo
    file_id=message.photo[-1].file_id
    new_file=bot.get_file(file_id)

    # find the full path to the image
    file_path=new_file.file_path
    file_path=f"https://api.telegram.org/file/bot{TELEGRAM_API_KEY}/{file_path}"

    # Determine the API call to api.ocr.space for it to download the image for processing
    url=f"https://api.ocr.space/parse/imageurl?apikey={OCR_SPACE_API_KEY}&url={file_path}&language=eng&detectOrientation=True&filetype=JPG&OCREngine=1&isTable=True&scale=True"

#    Uncomment the line below for testing
#    bot.reply_to(message, f"{url}")

    # Make the API call to api.ocr.space
    data=requests.get(f"https://api.ocr.space/parse/imageurl?apikey={OCR_SPACE_API_KEY}&url={file_path}&language=eng&detectOrientation=True&filetype=JPG&OCREngine=1&isTable=True&scale=True")
    # The extracted text is within the "data" returned
    data=data.json()
    
    if data['IsErroredOnProcessing']==False:
        # Display the text extracted from the image
        parsed_data = data['ParsedResults'][0]['ParsedText']
        parsed_split = parsed_data.split("\t")[7:]
        
        parsed_text = ''
         
        for i in parsed_split:
            if "TOTAL" in i:
                break
                 
            parsed_text += i
            parsed_text += "\\"
            
                
        #parsed_text_splitted = parsed_text.split("\\")
        #index = [x for x, s in enumerate(parsed_text_splitted) if "TOTAL" in s][0]
    
        bot.reply_to(message, parsed_text)

bot.infinity_polling()

