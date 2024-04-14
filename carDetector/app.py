from flask import Flask
 
app = Flask(__name__)

@app.route("/health")
def health():
    return "OK"

@app.route("/")
def home():
    return "Hello, this is the home page of Car Detector app! 🎉🔬🚀✨🎈🔭🧪🎉"
 
if __name__ == '__main__':  
   app.run(host="0.0.0.0", port=5000)
   
