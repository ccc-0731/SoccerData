from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('slider.html')

@app.route('/update', methods=['POST'])
def update_value():
    # Get slider value sent by JS
    value = request.json['value']
    # Example: maybe calculate something
    result = int(value) ** 2
    return jsonify({'result': result})  # Send it back to frontend

if __name__ == '__main__':
    app.run(debug=True)
