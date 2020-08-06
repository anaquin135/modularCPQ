#make a POST request
import requests
from requests.auth import HTTPBasicAuth
'''
dictToSend = {'attr1':1,
    'attr2':1,
    'attr3':1,
    'attr4':0,
    'attr5':0}
'''
res = requests.get('http://127.0.0.1:5000/api/v1.0/prod/Cloud Services/cs_staff', 
    #json=dictToSend, 
    auth=HTTPBasicAuth('INT_ADMIN', 'hX82ZilTgalkpqkd6dyp'))

#print ('response from server:',res.text)

dictFromServer = res.json()
print (dictFromServer)
# for items in dictFromServer:
#     print (items, ":", dictFromServer[items])
