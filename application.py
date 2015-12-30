# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 10:27:14 2015

@author: joe
"""

import os
from flask import Flask, request, url_for, jsonify, render_template
from werkzeug import secure_filename
from util.segmentation import segment
from util.detection import detect

UPLOAD_FOLDER = '/home/joe/Python/flask/fileupload/static/upload'
SEGMENTED_FOLDER = '/home/joe/Python/flask/fileupload/static/segment'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'tif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEGMENTED_FOLDER'] = SEGMENTED_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/segmentationView')
def segmentationView():
    return render_template('segmentation.html')

@app.route('/detectionView')
def detectionView():
    return render_template('detection.html')

@app.route('/segmentation', methods=['GET', 'POST'])
def segmentation():
    if request.method == 'POST':
        file = request.files['file']
        print('file:  {}'.format(file))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uploadedImage = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(uploadedImage)
            # segment the imgage uploaded and save it to DstImage location
            DstImage = os.path.join(app.config['SEGMENTED_FOLDER'], filename)
            # segment(uploadedImage, DstImage)
            return jsonify(originalImage='static/upload/'+filename, segmentedImage='static/segment/'+filename)
            # return render_template('UploadSuccessed.html', uploaded_file_name=filename)
        else:
            return jsonify(msg='不允许上传的文件类型')
    return 'Something wrong with Upload'

@app.route('/detection', methods=['GET', 'POST'])
def detection():
    # if request.method == 'POST':
    #     file = request.files['file']
    #     print('file:  {}'.format(file))
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         uploadedImage = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #         file.save(uploadedImage)
    #         # segment the imgage uploaded and save it to DstImage location
    #         DstImage = os.path.join(app.config['SEGMENTED_FOLDER'], filename)
    #         # segment(uploadedImage, DstImage)
    #         return jsonify(originalImage='static/upload/'+filename, segmentedImage='static/segment/'+filename)
    #         # return render_template('UploadSuccessed.html', uploaded_file_name=filename)
    #     else:
    #         return jsonify(msg='不允许上传的文件类型')
    return 'Detection is building'



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        print('file:  {}'.format(file))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uploadedImage = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(uploadedImage)
            # segment the imgage uploaded and save it to DstImage location
            DstImage = os.path.join(app.config['SEGMENTED_FOLDER'], filename)
            # segment(uploadedImage, DstImage)
            return jsonify(originalImage='static/upload/'+filename, segmentedImage='static/segment/'+filename)
            # return render_template('UploadSuccessed.html', uploaded_file_name=filename)
        else:
            return jsonify(msg='不允许上传的文件类型')
    return 'Something wrong with Upload'

if __name__=="__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=4000)
