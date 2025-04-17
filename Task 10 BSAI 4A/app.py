from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'library-secret-key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('chat.html')

@socketio.on('connect')
def handle_connect():
    emit('message', {'user': 'Library Bot', 'message': 'Hello! I\'m the Library Assistant. How can I help you today?'})

@socketio.on('message')
def handle_message(data):
    user_message = data['message'].lower()
    response = get_bot_response(user_message)
    emit('message', {'user': 'Library Bot', 'message': response})

def get_bot_response(message):
    if "hours" in message or "timing" in message:
        return "The library is open Monday to Friday from 9 AM to 8 PM, and on weekends from 10 AM to 6 PM."
    elif "borrow" in message or "loan" in message or "check out" in message:
        return "You can borrow up to 5 books at a time for a period of 2 weeks. You'll need your library card to check out books."
    elif "return" in message:
        return "Books can be returned at the front desk during library hours or through the book drop box available 24/7 outside the main entrance."
    elif "fine" in message or "fee" in message:
        return "Late returns incur a fine of $0.50 per day per book. The maximum fine per book is $10."
    elif "card" in message or "membership" in message:
        return "To get a library card, please visit the front desk with a valid ID and proof of address. The membership is free for residents."
    elif "book" in message and ("find" in message or "search" in message or "where" in message):
        return "You can search for books using our online catalog or ask a librarian for assistance. Books are organized by subject and author's last name."
    elif "reserve" in message or "hold" in message:
        return "You can place a hold on a book through our online portal or by calling the library. We'll notify you when it's available."
    elif "renew" in message:
        return "Books can be renewed online, by phone, or in person, as long as no one else has requested them. You can renew a book up to 2 times."
    elif "hello" in message or "hi" in message or "hey" in message:
        return "Hello! How can I assist you with the library services today?"
    elif "thank" in message:
        return "You're welcome! Feel free to ask if you have any other questions about our library services."
    elif "bye" in message or "goodbye" in message:
        return "Goodbye! Have a great day. Come back if you have more questions!"
    else:
        return "I'm not sure I understand. Could you rephrase your question? You can ask about library hours, borrowing books, returns, fines, or finding specific resources."

if __name__ == '__main__':
    socketio.run(app, debug=True, port=8000)