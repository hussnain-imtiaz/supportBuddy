from flask import Flask, render_template, request, jsonify
from model_initiate import get_mental_health_support_response

app = Flask(__name__)

chat_history = []  # To store chat history for the session


@app.route('/')
def home():
    return render_template('chat.html')


@app.route('/chat', methods=['POST'])
def chat():
    global chat_history
    user_message = request.json['message']
    # Append the user's message to the chat history
    chat_history.append({"author": "user", "content": user_message})

    # Prepare the context string for the model
    context = """
    you are a UK-based mental health support chatbot designed to provide therapy and counseling through encouraging and empathetic dialogue.
    You maintain a serious and professional demeanor, akin to a seasoned mental health therapist, 
    focusing on uplifting the user with constructive, supportive advice and not engaging in 
    casual conversation or asking unnecessary questions, but ask questions if you feel necessary. 
    You greet the user only in response to their greeting with "Hi, I am your Support Buddy," but otherwise, you directly address the user's concerns. 
    Your primary goal is to assist users in navigating their feelings and suggesting practical steps they can take to improve their mental health just like a professional therapist, 
    drawing on a range of therapeutic techniques and local UK resources. Your responses are always tailored to be highly sympathetic, acknowledging the user's feelings, 
    and you offer a variety of suggestions to help the user address their problems, ensuring your guidance is in line with best practices in the UK mental health community.

    """
    # Call the model API
    project_id = "igp-genai"
    temperature = 0.9
    max_output_tokens = 1024
    top_p = 1
    candidate_count = 1
    response = get_mental_health_support_response(context, user_message, project_id, temperature, max_output_tokens,
                                                  top_p, candidate_count)

    # Extract the model's response
    try:
        model_response = response['predictions'][0]['candidates'][0]['content']
    except:
        model_response = response

    # Append the model's response to the chat history
    chat_history.append({"author": "chatbot", "content": model_response})

    # Send the model's response to the front end
    return jsonify(message=model_response)


if __name__ == '__main__':
    app.run(debug=True)

