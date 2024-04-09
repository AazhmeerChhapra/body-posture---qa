from flask import Flask, request, jsonify, g ,render_template
import json
from dotenv import dotenv_values
from hugchat import hugchat
from hugchat.login import Login
COOKIE_FILE = 'cookies.json'
Q_FILE = 'question.json'
A_FILE = 'answer.json'

app = Flask(__name__)


    # Return the HTML file located in 'templates/index.html'
@app.route('/')
def hello_world():
    secrets = dotenv_values('hf.env')
    hf_email = secrets['EMAIL']
    hf_pass = secrets['PASS']
    sign = Login(hf_email, hf_pass)
    cookies = sign.login()
    # Write cookies to file (assuming COOKIE_FILE is defined)
    with open(COOKIE_FILE, 'w') as f:
        json.dump(cookies.get_dict(), f)
    return render_template('index.html')


@app.route('/question_generation/<string:domain>')
def question_generation(domain):
    # Read cookies from file
    try:
        with open(COOKIE_FILE, 'r') as f:
            cookies = json.load(f)
    except FileNotFoundError:
        return jsonify({"error": "Cookies not found. Please log in first."}), 401

    # Create ChatBot using stored cookies
    chatbot = hugchat.ChatBot(cookies=cookies)
    questions = f"Create the {domain} interview questions and do not write anything except question especially Sure, I can help you create some data science interview questions! Here are a few examples: "
    response = chatbot.chat(questions)
    response_questions_multiline = '"""' + response + '"""'
    response_qlist = response_questions_multiline.strip().split('\n')
    with open(Q_FILE, 'w') as f:
        json.dump(response_qlist, f)
    

    result = {
        "response": response_qlist
    }
    return jsonify(result)

@app.route('/answer_generation')
def answer_generation():

    try:
        with open(COOKIE_FILE, 'r') as f:
            cookies = json.load(f)
    except FileNotFoundError:
        return jsonify({"error": "Cookies not found. Please log in first."}), 401
    # Create ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies)

    try:
        with open(Q_FILE, 'r') as f:
            questions = json.load(f)
    except FileNotFoundError:
        return jsonify({"error": "questions not found. Please generate questions in first."}), 401
    
    questions = json.dumps(questions)

    answers = "Give answers for the following questions " + questions + " and do not write anything except answers especially Sure, I can help you create some data science interview questions! Here are a few examples: or questions themselves "
    response2 = chatbot.chat(answers)
    response_answers_multiline = '"""' + response2 + '"""'
    response_anslist = response_answers_multiline.strip().split('\n')
    with open(A_FILE, 'w') as f:
        json.dump(response_anslist, f)
    
    result = {
        "response": response_anslist
    }
    return jsonify(result)

@app.route('/answer_comparison')
def answer_comparison():
    user_answer = request.json.get("user_answers")
    try:
        with open(A_FILE, 'r') as f:
            answers = json.load(f)
    except FileNotFoundError:
        return jsonify({"error": "answers not found. Please generate answers in first."}), 401
    
    answers = json.dumps(answers)
    try:
        with open(COOKIE_FILE, 'r') as f:
            cookies = json.load(f)
    except FileNotFoundError:
        return jsonify({"error": "Cookies not found. Please log in first."}), 401
    chatbot = hugchat.ChatBot(cookies=cookies)
    evaluation = "compare answers in this " + user_answer + "with " + answers+ " and just provide the matching score, no need to write an other line"
    response2 = chatbot.chat(evaluation)
    result = {
        "response": "Your evaluation score is "+response2
    }


    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True,port=5001)
