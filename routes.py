from flask import render_template, flash, request, url_for
from app import app, silatra
import base64, numpy as np, cv2, io

@app.route('/')
def hello():
    return render_template('silatra.html')

@app.route('/hand-pose-recognition', methods=['GET', 'POST'])
def hand_pose_ask():
    result = ''
    
    if request.method == 'POST':
        img_file = request.files['img']
        in_memory_file = io.BytesIO()
        img_file.save(in_memory_file)
        data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        img = cv2.imdecode(data, color_image_flag)
        result = 'The recognized pose is -> ' + silatra.recognise_hand_pose(img)
        
    return render_template('hpr.html', result=result)

@app.route('/samples')
def show_samples():
    return render_template('samples.html')