from flask import Flask, request
app = Flask(__name__)
@app.route('/<name>')
def hello_world(name):
    user_agent = request.headers.get('User-Agent')
    return 'Hello Worldi %s!\n' % user_agent
if __name__ =='__main__':
    app.run(debug=True, host='0.0.0.0')
