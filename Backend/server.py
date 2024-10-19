from flask import Flask, request, jsonify,send_file
from flask_cors import CORS
from main import *
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import logging
from rule import rule
from speech import Speech
import base64


load_dotenv('API.env')

logging.basicConfig(filename='requests.log', level=logging.INFO, format='%(asctime)s - %(message)s')
speech = Speech()
GENAI = GENAI()
rules=rule()
Comparison = Comparison()
player_names = list(GENAI.players_data)

# Initializing flask app
app = Flask(__name__)
CORS(app,origins=['*'])  # Replace with your React app's origin

# Rate Limiter initialization
limiter = Limiter(
    get_remote_address,  # To get the client's IP address
    app=app,
    default_limits=["100 per day", "10 per hour"],  # Default limit for all routes
)

def log_request(req):
    client_ip = request.remote_addr
    endpoint = request.path
    payload = req.get_json() if req.is_json else None
    log_data = f"IP: {client_ip}, Endpoint: {endpoint}, Payload: {payload}"
    logging.info(log_data)

# Route for seeing a data
@app.route('/api/test', methods=['POST'])
def test():
    req = request.get_json()
    output = GENAI.output(req["input"])
    # print(req['input'],output)
    return {
          'Output':output, 
        }

@app.route('/api/rule', methods=['POST'])
def rule():
    req = request.get_json()
    # output = rules.groq_output(req["input"])
    output = GENAI.output(req["input"])

    # print(req['input'],output)
    # output = ''.join(output)
    print(req['input'],output)
    return {
          'Output':output, 
        }

@app.route('/api/ruleaudio', methods=['POST'])
def ruleaudio():
    log_request(request) 
    if 'audio' not in request.files:
        return jsonify({'message': 'No audio file found in the request'}), 400
    audio = request.files['audio']
    audio_path = 'recording.wav'
    audio.save(audio_path)
    text = speech.translation()    
    print(text)
    # output = rules.groq_output(text+'?')
    output = GENAI.output(text+'?')
    print(output)
    audio_data = speech.speech_gen(''.join(output))
    audio_path='audio.wav'
    # print(output)
    print("successfully")
    with open(audio_path, 'rb') as f:
            audio_data = base64.b64encode(f.read()).decode('utf-8')
    return {
            'Output': output,
            'audio': audio_data  # Base64 encoded audio data
          }

@app.route('/api/comparison', methods=['POST'])
def comparison():
    req = request.get_json()
    # output = Comparison.image_retrieve(req["input"])
    output1,output2 = Comparison.output(req["input"][0],req["input"][1])
    image1 = GENAI.ind_output(req["input"][0])
    image2 = GENAI.ind_output(req["input"][1])

    # print(image1)
    # print(image2)
    # print(req)
    return {
          'image1':image1, 
          'image2':image2,
          'img1':output1,
          'img2':output2
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

@app.route('/submit', methods=['POST','GET'])
def get():
  req = request.get_json()
  log_request(request)  # Log the request
  # print(req["text"])
  return {"Msg": "All Good!"}
     
# Running app
if __name__ == '__main__':
    app.run(port=5000)
    