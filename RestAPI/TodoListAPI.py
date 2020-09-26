from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
FILE = 'todo_list.csv'

@app.route('/todoList', methods=['GET'])
def getList():
    data = pd.read_csv(FILE)
    items=[]
    for i, row in data.iterrows():
        items.append({'id':row.id, 'text':row.text} )

    return jsonify(items), 200

@app.route('/todoList', methods=['POST'])
def insertItem():
    request_data = request.get_json()
    data = pd.read_csv(FILE)
    auto_incremente = int(data.iloc[[-1]].id) + 1
    data = data.append({'id': str(auto_incremente), 'text': request_data['text']},ignore_index=True)
    data.to_csv(FILE, index=False)
    return jsonify(data.to_dict()), 200

@app.route('/todoList/<int:id>', methods=['DELETE'])
def deleteItem(id):
    data = pd.read_csv(FILE)
    data = data[data.id != id]
    data.to_csv(FILE, index=False)
    return jsonify(data.to_dict()), 200

if __name__ == '__main__':
    app.run(debug=True)