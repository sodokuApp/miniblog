from flask import Flask, jsonify,abort,request
#-*- coding:utf-8 -*-
app = Flask(__name__)

chapters = [
    {
        "id": 1,
        "title": "software architecture",
        "author":"group 3",
        "context": "blog ",
        "tag":"tech"
    },
    {
        "id": 2,
        "title": "software network",
        "author": "group 3",
        "context": "hate",
        "tag": "tech"
    }
]


@app.route('/', methods=['GET'])
def allchapter():
    return jsonify({'chapters': chapters})

@app.route('/chapter/<int:chapter_id>',methods=['GET'])
def specchapter(chapter_id):
    chapter = list(filter(lambda t:t["id"]==chapter_id,chapters))
    if len(chapter)==0:
        abort(404)
    return jsonify({'chapters':chapter[0]})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error':'Not found'}),404


@app.route('/', methods=['POST'])
def add_chapter():
    if not request.json or not "title" in request.json:
        abort(404)

    chapter = {
        "id": chapters[-1]["id"] + 1,
        "title": request.json["title"],
        "author":request.json.get("author",""),
        "context": request.json.get("context", ""),
        "tag": request.json.get("tag", "")
    }

    chapters.append(chapter)
    return jsonify({'chapter': chapter}), 201


@app.route('/chapter/<int:chapter_id>', methods=['PUT'])
def update_chapter(chapter_id):
    chapter = list(filter(lambda t: t['id'] == chapter_id, chapters))
    if len(chapter) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if "title" in request.json and not isinstance(request.json["title"], str):
        abort(400)
    if "context" in request.json and not isinstance(request.json["context"],str):
        abort(400)
    chapter[0]["title"] = request.json.get("title", chapter[0]["title"])
    chapter[0]["author"] = request.json.get("author", chapter[0]["author"])
    chapter[0]["context"] = request.json.get("context", chapter[0]["context"])
    chapter[0]["tag"] = request.json.get("tag", chapter[0]["tag"])
    return jsonify({'chapters': chapter[0]})



@app.route('/chapter/<int:chapter_id>', methods=['DELETE'])
def delete_chapter(chapter_id):
    chapter = list(filter(lambda t: t["id"] == chapter_id, chapters))
    if len(chapter) == 0:
        abort(404)
    chapters.remove(chapter[0])  #
    return jsonify({'delete': True})

if __name__ == '__main__':
    app.run(debug=True)