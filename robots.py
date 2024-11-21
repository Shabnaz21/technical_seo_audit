import requests
link = input("Enter Your URl: ")
response= requests.get(link)
if response.status_code == 200:
    print('✅ robots.txt file exists')
else:
    print("❌ robots.txt file does not exist.") https://skillupwithshamim.com/