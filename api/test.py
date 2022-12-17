import requests
payload = {
  "title": "This is my great blog title",
   "content": "This is the body of my article",
   "Author": "Jaskier"
}
r = requests.post("http://localhost:4000/predict", json={
  "YearsExperience": 0
})
print(r.content)