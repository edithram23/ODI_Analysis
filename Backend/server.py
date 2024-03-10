from flask import Flask, request
from flask_cors import CORS
from main import GENAI

GENAI = GENAI()
 
# Initializing flask app
app = Flask(__name__)
CORS(app,origins=["http://127.0.0.1:5000/"])  # Replace with your React app's origin

 
# Route for seeing a data
@app.route('/api/test', methods=['POST'])
def test():
    req = request.get_json()
    output = GENAI.output(req["input"])
    print(req['input'],output)
    return {
          'Output':output, 
        }

@app.route('/submit', methods=['POST'])
def get():
  req = request.get_json()
  print(req["text"])
  return {"Msg": "All Good!"}
     
# Running app
if __name__ == '__main__':
    app.run(debug=True)