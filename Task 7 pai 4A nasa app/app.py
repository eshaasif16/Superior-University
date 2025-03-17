from flask import Flask , render_template 
import requests 

app =Flask(__name__)

nasa_api="F6AMZN2yeARRKTRWhWhUQxC4ryyjLVu4bMil5x8C"
APOD_URL ="https://api.nasa.gov/planetary/apod"

@app.route ("/", methods=["GET"])   #get will show us info pause wont show us info like username password
def index():
   
    params = {"api_key": nasa_api}
    response = requests.get(APOD_URL, params=params) #if u want values use get if u want to put values use put 
    apod_data = response.json()
    # params = {"api_key": nasa_api, "date": "2023-05-15"}
    # params = {"api_key": nasa_api, "count": 1}

    return render_template("index.html", apod =apod_data)

if __name__ == "__main__":
    app.run(debug=True)
    
    
    
