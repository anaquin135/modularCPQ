#make a POST request
import requests
from requests.auth import HTTPBasicAuth

res = requests.get('http://localhost:5000/api/v1.0/users', auth=HTTPBasicAuth('INT_ADMIN', 'hX82ZilTgalkpqkd6dyp'))

# print ('response from server:',res.text)

dictFromServer = res.json()

for items in dictFromServer:
    for users in dictFromServer['users']:
        for x in users:
            if x == "firstName" or x == "lastName":
                print (users[x])
