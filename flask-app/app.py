from flask import Flask, jsonify, render_template

app = Flask(__name__, static_folder='./build/static', template_folder='./build')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    data = {'key': 'value'}
    return jsonify(data)






if __name__ == '__main__':
    app.run(debug=True)
