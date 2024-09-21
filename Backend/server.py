from flask import Flask, request
from flask_cors import CORS
from main import *

GENAI = GENAI()
Comparison = Comparison()
player_names = list(GENAI.players_data)

# Initializing flask app
app = Flask(__name__)
CORS(app,origins=['*'])  # Replace with your React app's origin

 
# Route for seeing a data
@app.route('/api/test', methods=['POST'])
def test():
    req = request.get_json()
    output = GENAI.output(req["input"])
    print(req['input'],output)
    return {
          'Output':output, 
        }

@app.route('/api/comparison', methods=['POST'])
def comparison():
    req = request.get_json()
    # output = Comparison.image_retrieve(req["input"])
    output = Comparison.output(req["input"][0],req["input"][1])
    image1 = GENAI.ind_output(req["input"][0])
    image2 = GENAI.ind_output(req["input"][1])

    print(image1)
    print(image2)
    print(req['input'],output)
    print(req)
    return {
          'image1':image1, 
          'image2':image2
        }

@app.route('/api/suggestion', methods=['POST'])
def suggestion():
  req = request.get_json()
  pattern = re.compile(f'.*{re.escape(req["name"])}.*', re.IGNORECASE)
  # text = '''<option value="Objective C">Objective C</option>'''
    # Filter player names based on the regex match (original case is preserved in suggestions)
  suggestions = [player for player in player_names if pattern.search(player)]
  if(len(suggestions)<50):
    return {
      'suggestion':suggestions
    }
  else:
    player = ['Virat Kohli','Rohit Sharma']
    return {
      'suggestion': player
    }

@app.route('/submit', methods=['POST'])
def get():
  req = request.get_json()
  print(req["text"])
  return {"Msg": "All Good!"}
     
# Running app
if __name__ == '__main__':
    app.run(debug=True)
    