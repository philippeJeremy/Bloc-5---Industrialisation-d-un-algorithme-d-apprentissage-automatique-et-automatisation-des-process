import requests

response = requests.post("https://api-getaround.herokuapp.com/predict", json={
    'model_key': "Citroën", 
    'mileage': 140411, 
    'engine_power': 900, 
    'fuel': "diesel", 
    'paint_color': "black",
    'car_type': "convertible", 
    'private_parking_available': True, 
    'has_gps': True,
    'has_air_conditioning': False, 
    'automatic_car': False, 
    'has_getaround_connect': True,
    'has_speed_regulator': True,
    'winter_tires': True
})

print(response.json())