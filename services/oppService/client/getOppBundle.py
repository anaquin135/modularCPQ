#make a POST request
import requests
from requests.auth import HTTPBasicAuth
import json

res = requests.get('http://localhost:602/api/v1.0/opp/bundle/1', auth=HTTPBasicAuth('INT_ADMIN', 'hX82ZilTgalkpqkd6dyp'))

# print ('response from server:',res.text)

dictFromServer = res.json()
print (dictFromServer)

#print ("---------")
'''
parent = {}
arrLines = [] 

# Current Inventory Loop #
for lines in dictFromServer:
    # This specific Line
    child = dictFromServer[lines]
    childDict = {}

    # Loop every attribute #
    for attr in child:
        childDict[attr] = child[attr]
''''''
    # Append to the master list #
    arrLines.append(childDict)
''''''    
# Items We're Adding #
newItem1 = {
        'partNumber':'XYZ123',
        'description':'new item 1',
        'qtyNew':0,
        'qtyExi':0,
        'listNRC':0,
        'listMRC':0,
        'discNRC':0.0,
        'discMRC':0.0,
        'netNRC':0.0,
        'netMRC':0.0
}
newItem2 = {
        'partNumber':'XYZ1234',
        'description':'new item 2',
        'qtyNew':0,
        'qtyExi':0,
        'listNRC':0,
        'listMRC':0,
        'discNRC':0.0,
        'discMRC':0.0,
        'netNRC':0.0,
        'netMRC':0.0
}
newParent = {
    0:newItem1,
    1:newItem2
}
newJson = json.dumps(newParent)

# Loop New Items #
# Current Inventory Loop #
for lines in newParent:
    # This specific Line
    child = newParent[lines]
    childDict = {}

    # Loop every attribute #
    for attr in child:
        childDict[attr] = child[attr]

    # Append to the master list #
    arrLines.append(childDict)
    

# Process Master List Into The Proper Structure #
x = 0
for line in arrLines:
    parent[x] = arrLines[x]
    x = x + 1

# Make JSON #
invJson = json.dumps(parent)
print("--------")
print (invJson)

'''
