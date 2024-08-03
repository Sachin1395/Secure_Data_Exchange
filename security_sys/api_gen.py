from flask import Flask,jsonify
import json
import base64

# get random password pf length 8 with letters, digits, and symbols
'''
characters = string.ascii_letters + string.digits
password = ''.join(random.choice(characters) for i in range(16))
print("Random password is:", password)
'''
from main import Login
from encryption import Encryption

print("* * * SENDER SIDE * * *\n")

user=Login().login()

data={
    "Household ID":"",
    "Timestamp":"",
    "Energy Consumption":"",
    "Peak Demand":"",
    "Substation ID":"",
}



#access_token="qfst53602h11WWwG"

if user==True:
    en = Encryption()
    aes = en.generate_aes_key()
    print("Enter the relevant data :\n")

    for key in data:
        encrypted_data = en.encrypt_data(input(f"enter {key} : "), aes)
        data[key]=encrypted_data
    encrypted_aes_key = en.encrypt_aes_key(aes)
    data["aes"]=encrypted_aes_key
    print("\nData is successfully encrypted and posted as an api on the server.\n ")
    print("api url : http://127.0.0.1:5000/your_acces_token\n")
    api = data




encoded_dict = {key: base64.b64encode(value).decode('utf-8') for key, value in api.items()}

# Convert the dictionary to a JSON string
json_str = json.dumps(encoded_dict)



app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>IOT api</p>"



@app.route("/<p>",methods=["GET"])
def get__(p):
    if  p=="qfst53602h11WWwG":
        return jsonify(json_str)
    else:
        return jsonify("401 Unauthorized")





if __name__=="__main__":
    app.run()