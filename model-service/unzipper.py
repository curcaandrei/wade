from zipfile import ZipFile
from flask import jsonify
def unzip_model():
    with ZipFile('static/als_model.zip', 'r') as zObject:
        zObject.extractall(path="static")
        return jsonify('Model was unzipped succesfully'),200