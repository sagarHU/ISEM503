# app.py
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import openai
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sk-proj-d-Pyk-RIw-1OZAcGGwKL6DEYX#####################Gxrn8LQPaElacmjM5dZ95q6arYT3BlbkFJoTrGrt4j0RSIVB6silMwXvvttunitI2xugayhUYyWH7kiiZPcx7yd0W5XfExg1GmMULXnlBIAA'
socketio = SocketIO(app)

# Set your OpenAI API key here or load it from an environment variable for security
openai.api_key = os.getenv("OPENAI_API_KEY", "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")

def generate_openai_response(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a knowledgeable and friendly virtual healthcare assistant. Provide helpful and accurate medical information based on the user's questions, focusing on self-care, preventative tips, and over-the-counter guidance."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].message['content'].strip()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_message')
def handle_send_message_event(data):
    user_message = data['message']
    bot_response = generate_openai_response(user_message)
    emit('receive_message', {'message': bot_response, 'sender': 'bot'})

if __name__ == '__main__':
    socketio.run(app, debug=True)
