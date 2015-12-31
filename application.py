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
from util.tif_tools import tif2other

PWD = os.getcwd()
UPLOAD_FOLDER = PWD + '/static/upload'
SEGMENTED_FOLDER = PWD + '/static/segment'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'tif', 'TIF'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEGMENTED_FOLDER'] = SEGMENTED_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def processTif(uploadedImage, filename):
    if filename.rsplit('.', 1)[1] in {'tif', 'TIF'}:
        uploadedImageNew = uploadedImage.rsplit('.', 1)[0]+'.png'
        newFileName = filename.rsplit('.', 1)[0]+'.png'
        print('#@app.route(segmentation) processTif:  {} to {}'.format(filename, newFileName))
        tif2other(uploadedImage, uploadedImageNew, 'png')
        return newFileName;
    else:
        return filename

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
        print('#@app.route(segmentation) file:  {}'.format(file))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uploadedImage = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(uploadedImage)
            # segment the imgage uploaded and save it to DstImage location
            DstImage = os.path.join(app.config['SEGMENTED_FOLDER'], filename)
            # segment(uploadedImage, DstImage)

            # if it is tif format, transfer it to png and save
            filename = processTif(uploadedImage, filename)
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

@app.route('/upload_multifiles', methods=['GET', 'POST'])
def upload_multifiles():
    if request.method == 'POST':
        # corresponding to the "name" attribute of "input" from web client
        # import pdb; pdb.set_trace()

        uploaded_files = request.files.getlist('file')
        originalImagesForClient = []
        detectedImagesForClient = []
        for file in uploaded_files:
            print('file:  {}'.format(file))
            # filter the empty filenames
            if file.filename=='':
                continue
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                uploadedImage = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(uploadedImage)
                # segment the imgage uploaded and save it to DstImage location
                DstImage = os.path.join(app.config['SEGMENTED_FOLDER'], filename)
                # segment(uploadedImage, DstImage)

                originalImagesForClient.append('static/upload/'+filename)
                detectedImagesForClient.append('static/detect/'+filename)

                # return render_template('UploadSuccessed.html', uploaded_file_name=filename)
            else:
                return jsonify(msg='不允许上传的文件类型')
        return jsonify(originalImage=originalImagesForClient, detectedImage=detectedImagesForClient)
    return 'Something wrong with Upload'

if __name__=="__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=4000)
