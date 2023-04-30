from flask import Flask, render_template, request
import funcs.chatgpt_algo as chatgpt_algo

app = Flask(__name__,template_folder='static')

# A web application which get input from the user on what type of transcript they want to summarize and then summarize it using OpenAI's GPT-3 API.
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summAIze', methods=["GET",'POST'])
def summAIze():
    if request.method == 'POST':
        data = request.form['data']
        summary_type = request.form['summary_type']

        chatgpt_algo.user_select_type(type=summary_type,data=data)

        summary = chatgpt_algo.ChatGPT()

        return render_template('index.html', summary=summary)


if __name__ == '__main__':
    app.run(host='127.0.0.1',debug=True)
