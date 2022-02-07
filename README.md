# Programming-Assignment

First install requirmental library.
```
pip install -r requirements.txt
```

Run the app.py to start the server.
```
python app.py
```

URL is localhost and PORT is 5000, so you could request localhost:5000 and pass parameters to get the output.
For example 
```
$curl http://127.0.0.1:5000/task -X GET -d  "UserID=e0505a0b-a50e-483c-bb5d-c4d491551134"
```
There are two GET method to extract statistical values from sales data and task data individually.\\
Btw, you could see the swagger document at http://localhost:5000/apidocs/#/.

