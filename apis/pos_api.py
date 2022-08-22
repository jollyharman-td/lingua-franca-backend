from services.pos import init_model, tag_sentence, clean_text
from flask import Flask, request, jsonify, Response

model, vocab_, tags = init_model()
app = Flask(__name__)
@app.route('/pos/', methods=['POST'])

def pos():
    output = []
    if request.method == "POST":
        req_json = request.json
        text = req_json['text']
        text = clean_text(text)
        data_lines = text.strip().split("\n")

        for data in data_lines:
            op = tag_sentence(model, data, vocab_, tags)
            output.append(op)

    return jsonify({"pos": output})

if __name__ == '__main__':
    app.run(debug=True, port=8002)