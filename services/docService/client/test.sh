curl -u INT_ADMIN:hX82ZilTgalkpqkd6dyp -X POST -H "Content-Type: application/json" -d '{"id":"1", "customerName":"Walmart", "desc":"This is a test deal!", "contractTerm":"36", "requestOwner":"Austin Naquin", "lastModified":"08-04-2020", "bundle":"{\"0\": {\"partNumber\": \"CSNT04\", \"description\": \"Intern\", \"qtyNew\": 1, \"qtyExi\": 0, \"listNRC\": 0.0, \"listMRC\": 12500.0, \"discNRC\": 0.0, \"discMRC\": 0.0, \"netNRC\": 0.0, \"netMRC\": 12500.0, \"extNRC\": 0.0, \"extMRC\": 12500.0}, \"1\": {\"partNumber\": \"CSNF02\", \"description\": \"Senior Functional Consultant\", \"qtyNew\": 2, \"qtyExi\": 0, \"listNRC\": 0.0, \"listMRC\": 5000.0, \"discNRC\": 0.0, \"discMRC\": 0.0, \"netNRC\": 0.0, \"netMRC\": 5000.0, \"extNRC\": 0.0, \"extMRC\": 10000.0}, \"2\": {\"partNumber\": \"CSNF02\", \"description\": \"Senior Functional Consultant\", \"qtyNew\": 2, \"qtyExi\": 0, \"listNRC\": 0.0, \"listMRC\": 5000.0, \"discNRC\": 0.0, \"discMRC\": 0.0, \"netNRC\": 0.0, \"netMRC\": 5000.0, \"extNRC\": 0.0, \"extMRC\": 10000.0}, \"3\": {\"partNumber\": \"CSNF02\", \"description\": \"Senior Functional Consultant\", \"qtyNew\": 2, \"qtyExi\": 0, \"listNRC\": 0.0, \"listMRC\": 5000.0, \"discNRC\": 0.0, \"discMRC\": 0.0, \"netNRC\": 0.0, \"netMRC\": 5000.0, \"extNRC\": 0.0, \"extMRC\": 10000.0}, \"4\": {\"partNumber\": \"CSNF02\", \"description\": \"Senior Functional Consultant\", \"qtyNew\": 2, \"qtyExi\": 0, \"listNRC\": 0.0, \"listMRC\": 5000.0, \"discNRC\": 0.0, \"discMRC\": 0.0, \"netNRC\": 0.0, \"netMRC\": 5000.0, \"extNRC\": 0.0, \"extMRC\": 10000.0}, \"5\": {\"partNumber\": \"CSNF02\", \"description\": \"Senior Functional Consultant\", \"qtyNew\": 2, \"qtyExi\": 0, \"listNRC\": 0.0, \"listMRC\": 5000.0, \"discNRC\": 0.0, \"discMRC\": 0.0, \"netNRC\": 0.0, \"netMRC\": 5000.0, \"extNRC\": 0.0, \"extMRC\": 10000.0}}"}' -i http://127.0.0.1:5000/api/v1.0/doc/1 | tail -n +8