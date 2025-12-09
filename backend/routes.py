from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((p for p in data if p.get("id") == id), None)
    if picture is None:
        return jsonify({"Message": "Not Found"}), 404
    return jsonify(picture), 200


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    global data

    picture = request.get_json()

    if not picture or "id" not in picture or "pic_url" not in picture:
        return jsonify({"Message": "Bad Request"}), 400

    existing = next((p for p in data if p.get("id") == picture["id"]), None)
    if existing:
        return (
            jsonify({"Message": f"picture with id {picture['id']} already present"}),
            302,
        )

    data.append(picture)

    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    global data

    body = request.get_json()
    if not body:
        return jsonify({"Message": "Bad Request"}), 400

    for idx, pic in enumerate(data):
        if pic.get("id") == id:
            body["id"] = id
            data[idx] = body
            return jsonify(body), 200

    return jsonify({"Message": "Picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    global data

    for idx, pic in enumerate(data):
        if pic.get("id") == id:
            del data[idx]
            return "", 204

    return jsonify({"Message": "Picture not found"}), 404
