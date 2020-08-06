#make a POST request
import requests
from requests.auth import HTTPBasicAuth

#dictToSend = {'password':'qet123'}

res = requests.post('http://127.0.0.1:5000/api/v1.0/opp/bundle/1', 
    json={"0": {"partNumber": "XXX123", "description": "This is a line item!", "qtyNew": 3, "qtyExi": 2, "listNRC": 10.0, "listMRC": 5.0, "discNRC": 0.05, "discMRC": 0.05, "netNRC": 3.0, "netMRC": 4.0}, "1": {"partNumber": "XXX000", "description": "This is another line item!", "qtyNew": 5, "qtyExi": 5, "listNRC": 100.0, "listMRC": 0.0, "discNRC": 0.0, "discMRC": 0.0, "netNRC": 150.0, "netMRC": 0.0}, "2": {"partNumber": "XYZ123", "description": "new item 1", "qtyNew": 0, "qtyExi": 0, "listNRC": 0, "listMRC": 0, "discNRC": 0.0, "discMRC": 0.0, "netNRC": 0.0, "netMRC": 0.0}, "3": {"partNumber": "XYZ1234", "description": "new item 2", "qtyNew": 0, "qtyExi": 0, "listNRC": 0, "listMRC": 0, "discNRC": 0.0, "discMRC": 0.0, "netNRC": 0.0, "netMRC": 0.0}}, 
    auth=HTTPBasicAuth('INT_ADMIN', 'hX82ZilTgalkpqkd6dyp'))

#print ('response from server:',res.text)

dictFromServer = res.json()
print (dictFromServer)
# for items in dictFromServer:
#     print (items, ":", dictFromServer[items])
