#make a POST request
import requests
from requests.auth import HTTPBasicAuth

dictToSend = {'email':'austinjnaquin@gmail.com', 'password':'qet123'}

res = requests.post('http://localhost:5000/api/v1.0/users/session', json=dictToSend, auth=HTTPBasicAuth('INT_ADMIN', 'hX82ZilTgalkpqkd6dyp'))

#print ('response from server:',res.text)

dictFromServer = res.json()

for items in dictFromServer:
    print (items, ":", dictFromServer[items])
