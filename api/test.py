import requests
payload = {
  "title": "This is my great blog title",
   "content": "This is the body of my article",
   "Author": "Jaskier"
}
r = requests.post("http://localhost:4000/predict", json={
    "marque": "Citroën",
    "kilometrage": 27920,
    "puissance": 110,
    "energie": "diesel",
    "car_type": "convertible",
    "parking_private": False, 
    "gps": True,
    "air_conditionning": True, 
    "automatic": False,
    "getaround_connect": False, 
    "speed_regulator": True, 
    "winter_tires": False 
})
print(r.content)