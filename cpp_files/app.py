from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

decisions = ["Offside", "Foul", "Goal", "No Violation"]

@app.route('/')
def home():
    return render_template("index.html")  # يعرض واجهة الموقع

@app.route('/decision', methods=['GET'])
def get_decision():
    decision = random.choice(decisions)  # اختيار قرار عشوائي
    return jsonify({"decision": decision})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)