#make a POST request
import requests
from requests.auth import HTTPBasicAuth
    
dictToSend = {
    'id':1,
    'customerName':'Walmart',
    'desc':'This is a test deal!',
    'contractTerm':36,
    'requestOwner':'Austin Naquin',
    'lastModified':'08-04-2020',
    'bundle':''
}
    
res = requests.post('http://127.0.0.1:5000/api/v1.0/doc/1', 
    json=dictToSend, 
    auth=HTTPBasicAuth('INT_ADMIN', 'hX82ZilTgalkpqkd6dyp'))

print (res)
#print ('response from server:',res.text)
# dictFromServer = res.content
# print (dictFromServer)
# # for items in dictFromServer:
# #     print (items, ":", dictFromServer[items])
