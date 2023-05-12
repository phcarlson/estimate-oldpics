import requests

resp = requests.post("http://localhost:5000/predict",
                     files={"file": open('C:/Users/phcar/Desktop/oldpics/5/03/5033604.jpg','rb')})

print(resp.json())