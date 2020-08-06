#curl -u INT_ADMIN:hX82ZilTgalkpqkd6dyp -i -H "Content-Type: application/json" -X POST -d '{"firstName":"bob", "lastName":"dobbs", "email":"dobbs@austinnaquin.com", "password":"dobbies", "jobTitle":"CEO"}' http://localhost:5000/api/v1.0/users/add | less
curl -u INT_ADMIN:hX82ZilTgalkpqkd6dyp -i -H "Content-Type: application/json" -X POST -d '{"firstName":"bobby", "lastName":"dobby", "email":"dobbie@austinnaquin.com", "password":"dobbies", "jobTitle":"CEO", "deactivateDate":"20-07-20"}' http://localhost:5000/api/v1.0/users/add | less

            