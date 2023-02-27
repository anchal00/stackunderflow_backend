# Stackunderflow Backend 

Note: Requires Python v3.6.9 and Postgres v14.6 installed

### Setting up the server
1. Clone the github project on your local machine
2. (Optional) Create a virtual environment and activate it
3. Change dir to *stackunderflow_backend* 
4. Install the dependencies by running `pip install -r requirements.txt`
5. Change dir to *stackunderflow*
6. Apply Django Migrations by running `./manage.py migrate`
7. Finally run the server by running `./manage.py runserver`


###  API endpoints
- JWT tokens:
  -  POST `/stackunderflow/api/token/`
  -  POST `/stackunderflow/api/token/refresh`
- Questions 
  - GET `/stackunderflow/api/questions/{question_id}`
  - GET `/stackunderflow/api/questions/`
  - POST `/stackunderflow/api/questions/`
  - PATCH `/stackunderflow/api/questions/{question_id}`
  - DELETE `/stackunderflow/api/questions/{question_id}`
  
- Answers
  - GET `/stackunderflow/api/questions/{question_id}/answers/{answer_id}`
  - GET `/stackunderflow/api/questions/{question_id}/answers/`
  - POST `/stackunderflow/api/questions/{question_id}/answers/`
  - PATCH `/stackunderflow/api/questions/{question_id}/answers/{answer_id}`
  - DELETE `/stackunderflow/api/questions/{question_id}/answers/{answer_id}`

- Question Comments
  - GET `/stackunderflow/api/questions/{question_id}/comments/{comment_id}`
  - GET `/stackunderflow/api/questions/{question_id}/comments/`
  - POST `/stackunderflow/api/questions/{question_id}/comments/`
  - PATCH `/stackunderflow/api/questions/{question_id}/comments/{comment_id}`
  - DELETE `/stackunderflow/api/questions/{question_id}/comments/{comment_id}`

- Answer Comments
  - GET `/stackunderflow/api/answers/{answer_id}/comments/{comment_id}`
  - GET `/stackunderflow/api/answers/{answer_id}/comments/`
  - POST `/stackunderflow/api/answers/{answer_id}/comments/`
  - PATCH `/stackunderflow/api/answers/{answer_id}/comments/{comment_id}`
  - DELETE `/stackunderflow/api/answers/{answer_id}/comments/{comment_id}`
