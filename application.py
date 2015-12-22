# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 10:27:14 2015

@author: joe
"""

import os
from flask import Flask, request, url_for, render_template
from werkzeug import secure_filename

UPLOAD_FOLDER = '/home/joe/Python/flask/fileupload/static/upload'
SEGMENTED_FOLDER = '/home/joe/Python/flask/fileupload/static/segment'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEGMENTED_FOLDER'] = SEGMENTED_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def segment(sourceImage, DstImage):
    import sys
    sys.path.insert(0,'/home/joe/github/caffe-with_crop/python')
    import numpy as np
    from PIL import Image
    import matplotlib.pyplot as plt
    import caffe
    # caffe.set_mode_gpu()
    # caffe.set_device(0)
    # load image, switch to BGR, subtract mean, and make dims C x H x W for Caffe
    im = Image.open(sourceImage)
    in_ = np.array(im, dtype=np.float32)
    in_ = in_[:,:,::-1]
    in_ -= np.array((104.00698793,116.66876762,122.67891434))
    in_ = in_.transpose((2,0,1))

    # load net
    net = caffe.Net('/home/joe/github/caffe-with_crop/examples/fcn-32s-pascal-context/deploy.prototxt', '/home/joe/github/caffe-with_crop/examples/fcn-32s-pascal-context/fcn-32s-pascalcontext.caffemodel', caffe.TEST)
    # shape for input (data blob is N x C x H x W), set data
    net.blobs['data'].reshape(1, *in_.shape)
    net.blobs['data'].data[...] = in_
    # run net and take argmax for prediction
    net.forward()
    out = net.blobs['score'].data[0].argmax(axis=0)
#    plt.imshow(out)
    plt.imsave(DstImage, out)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uploadedImage = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(uploadedImage)
            # segment the imgage uploaded and save it to DstImage location
            DstImage = os.path.join(app.config['SEGMENTED_FOLDER'], filename)
            segment(uploadedImage, DstImage)
            return render_template('UploadSuccessed.html', uploaded_file_name=filename)
    return render_template('fileUpload.html')

if __name__=="__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=4000)
