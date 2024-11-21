import requests
link = input("Enter Your URl: ")
r= requests.get(link)
print(r)