




import requests
TOKEN = '8120146889:AAF8we4pr6rhiMGJcUFidpI4l-fM0Khnc68'
ids = '5563890177'

message='second message'
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ids}&parse_mode=Markdown&text={message}"
print(requests.get(url).json())