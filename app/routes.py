from flask import render_template, flash, request, url_for
from app import app, silatra
from os import system
import base64, numpy as np, cv2, io

@app.route('/')
def hello():
    return render_template('silatra.html')

@app.route('/hand-pose-recognition', methods=['GET', 'POST'])
def hand_pose_ask():
    result = ''
    
    # User input image
    if request.method == 'POST':
        img_file = request.files['img']
        in_memory_file = io.BytesIO()
        img_file.save(in_memory_file)
        data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        img = cv2.imdecode(data, color_image_flag)

        # An image with high resolution is not good enough for a t2.micro AWS instance. Need to resize it
        width, height, _ = img.shape
        while height > 1500 or width > 1500:
            img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            height = height/2
            width = width/2
        
        # That's the API call to the Hand pose recognition.
        result = 'Did you make the "' + silatra.recognise_hand_pose(img) + '" sign?'

    # Direct image input from samples.html    
    elif request.args.get('image'):
        img = cv2.imread('app/static/'+request.args.get('image'))
        try:
            img_copy = img.copy()
            del(img_copy)
            result = 'Did you make the "' + silatra.recognise_hand_pose(img) + '" sign?'
        except AttributeError as ae:
            import time
            with open('error_log.txt', 'a') as f:
                f.write(time.gmtime())
                f.write("IMG NOT FOUND: app/static/"+request.args.get('image'))
    
    return render_template('hpr.html', result=result)

@app.route('/samples')
def show_samples():
    return render_template('samples.html')