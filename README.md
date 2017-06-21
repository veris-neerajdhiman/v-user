## About

- v-user is `User` related micro-service.
- It uses `Django` default `user` module for user realted operations.
- However some changes are made in in-built `user` module by extending it.

## Prerequisites

#### Environment Variables : 

 - DATABASE_NAME_USER
 - DATABASE_USER
 - DATABASE_PASSWORD
 - DATABASE_HOST
 - DATABASE_PORT
 - SECRET_KEY
 - AM_SERVER_URL
 - ORGANIZATION_IDENTIFIER
	- value: organization
 - VRT_IDENTIFIER
	- value: runtime
 
 #### Micro-service : 

 - [AM](https://github.com/veris-neerajdhiman/v-authorization) server
 must be hosted & running and add its accessible url in above  `AM_SERVER_URL` 
 environment variable.
 
     
## Rules OR Conditions

- Some Rules or Assumptions are made here which are as follows :
 
	1 ) Email is our main primary contact (Cannot be updated normally, 
	To Update some steps must be followed which are not decided yet).
	
	2 ) A UUId will be issued to every user, which will be distributed to
	 other services in order to make any relation with user 
	(user primary key will not be disclosed)
	

## API Reference : 

- API documentation is hosted on [Swagger hub](https://app.swaggerhub.com/apis/verisadmin/v-user/0.1) 
and is public.

## Signals : 

1 ) Add User Policies on [AM](https://github.com/veris-neerajdhiman/v-authorization)
 server.
 
## Tests : 

- Run tests using 
```python
python manage.py test
```
 
 