import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

# Load the env file
load_dotenv()

# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app)

# Create a client using the OpenAI key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Serve the frontend index.html from the static folder
@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')

@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('static', filename)

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

    Give each a score from 0 to 100 on agreement.
    """

    try:
        chat = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a philosophy professor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        result = chat.choices[0].message.content
        return jsonify({"analysis": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
