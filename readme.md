
POST CMD
curl -X POST http://0.0.0.0:8000/members/rest/employee/ -d "first_name=joston&last_name=salanda&address=bandlore&emp_id=1&mobile=915263890&department=OPERATIONS&salary=1000"



GET CMD
curl -X GET http://0.0.0.0:8000/members/rest/employee/id/1



PATCH CMD
curl -X PATCH http://0.0.0.0:8000/members/rest/employee/id/1 -H "Content-Type: application/json" -d '{"salary": 75000}'



DELETE CMD
curl -X DELETE http://0.0.0.0:8000/members/rest/employee/id/1


DATABASE NAME
emp_db

HOW TO LOGIN TO DATABASE AND SEE THE DATA?

 docker exec -it psql-db sh
 psql -U postgres
 \c emp_db
 \dt

 select * from members_employee;

 




