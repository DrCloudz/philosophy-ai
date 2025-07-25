import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

# Load the env file
load_dotenv()

# Initialize Flask app and cors
app = Flask(__name__)
CORS(app)
CORS(app, origins=["https://philosophy-ai-1.onrender.com"])

# Creating a client using the OpenAI api key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Serve the frontend index.html from the static folder, basically setting up my homepage route and all the files within the static folder
@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')
# This serves file sin my static folder when requested
@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('styles.css','script.js')

# This is an endpoint that handles user responses
# Gets the user response and sends to the api(gpt 3.5 turbo) for analysis in the form of a prompt
# Grabs the AI response and send it back as a json object
# Error handling is included to catch any problems with the OpenAI api call
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    user_response = data.get('response', '')

    prompt = f"""
    A user wrote the following response to an ethical dilemma:

    "{user_response}"

    Analyze which of these philosophers would agree and disagree, and why:
    - Socrates
    - Immanuel Kant
    - Friedrich Nietzsche
    - John Stuart Mill
    - Plato
    - Aristotle
    - Confucius
    - Julius Nyerere

    Give each a score from 0 to 100 on agreement. Be sure to explore reasoning annd make it seem like the user is actually reading a response from said philosophers. 
    """

    try:
        chat = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a philosophy professor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )
        result = chat.choices[0].message.content
        return jsonify({"analysis": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
     
     # This GET endpoint generates a dilemma itself.
    @app.route('/generate-dilemma', methonds=['GET'])
    def generate_dilemma():
        try:
            chat = client.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a philosophy professor."},
                    {"role": "user", "content": "Generate a philosophical dilemma for students to discuss."}
                ],
                temperature=0.6
            )
            dilemma = chat.choices[0].message.content.strip()

            return jsonify({"dilemma": dilemma})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)