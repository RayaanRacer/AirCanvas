from flask import request,session, redirect, url_for
import numpy as np
import cv2
from collections import deque
import os
import requests

# Global variable to keep track of the screenshot count
screenshot_count = 0

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)
app.secret_key = 'aabrakadaabra'

def getImages(userID,name):
        response = requests.get('http://localhost:8080/user/api/v1/sendImage', json={'userID': userID})
        if response.status_code == 200:
            # Login successful, redirect to video_feed
            data = response.json()
            if 'img' not in session:
                session['img'] = []
            for item in data['imageURL']:
                session['img'].append(item)
        else:
            # Login failed, show an error message
            return render_template('index.html', error='Invalid email or password')


@app.route("/main")
def main():
    return render_template("main.html")

# added from me
@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('userID', None)
    return redirect(url_for('login'))

@app.route('/create-order',methods=['GET', 'POST'])
def create_order():
    if 'userID' in session:
        userId = session['userID']

        # Make a request to the REST API
        response = requests.post('http://localhost:8080/user/api/v1/create-order', json={'userId': userId, 'amount': '50'})

        if response.status_code == 200:
            # Login successful, redirect to video_feed
            data = response.json()
            session['razorpayKeyId'] = data['data']['razorpayKeyId']
            session['orderId'] = data['data']['id']
            return render_template('Payment.html', name=session['name'], id =session['userID'], razorpayKeyId = session['razorpayKeyId'], orderId=session['orderId'])
        else:
            # Login failed, show an error message
            return render_template('index.html', error='Invalid email or password')


@app.route('/payments')
def payments():
    if 'userID' in session:
        # return redirect(url_for('userDashboard',email=session['email']))
        # getImages(session['userID'], session['name'])
        return render_template('Payment.html', name=session['name'], id =session['userID'] )
    else:
        # Login failed, show an error message
        return render_template('index.html', error='Invalid email or password')
    
@app.route('/userDashboard')
def userDashboard():
    if 'userID' in session:
        # return redirect(url_for('userDashboard',email=session['email']))
        getImages(session['userID'], session['name'])
        return render_template('userDashboard.html',img=session['img'], name=session['name'], id =session['userID'] )
    else:
        # Login failed, show an error message
        return render_template('index.html', error='Invalid email or password')

@app.route('/myCreativity')
def myCreativity():
    if 'userID' in session:
        # return redirect(url_for('userDashboard',email=session['email']))
        getImages(session['userID'], session['name'])
        return render_template('myCreativity.html',img=session['img'], name=session['name'], id =session['userID'] )
    else:
        # Login failed, show an error message
        return render_template('index.html', error='Invalid email or password')

@app.route("/admin-login", methods=['GET', 'POST'])
def admin_login():
    if 'adminId' in session:
        return render_template('adminDashboard.html', name=session['admin_name'], id =session['adminId'],email=session['admin_email'] )
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Make a request to the REST API
        response = requests.post('http://localhost:8080/admin/api/v1/admin-login', json={'email': email, 'password': password})

        if response.status_code == 200:
            # Login successful, redirect to video_feed
            data = response.json()
            session['admin_name'] = data['data']['name']
            session['adminId'] = data['data']['_id']
            session['admin_email'] = data['data']['email']
            return render_template('adminDashboard.html', name=session['admin_name'], id =session['adminId'],email=session['admin_email'] )
        else:
            # Login failed, show an error message
            return render_template('index.html', error='Invalid email or password')
    return render_template('index.html', error=None)

@app.route("/adminDeleteUserPage")
def admin_delete_list():
    if 'adminId' in session:
        if request.method == 'GET':
            response = requests.get('http://localhost:8080/admin/api/v1/user-list', json={'adminId':session['adminId']} )
            data = response.json()
            if response.status_code == 200:
                print(data['data'])
                session['user_list'] = []
                for item in data['data']:
                    key_object_pair = {
                    "name": item['name'],
                    "_id": item["_id"],
                    "email": item["email"],
                    "phone": item["phone"]
                    }
                    session['user_list'].append(key_object_pair)
                print(session['user_list'])
                return render_template('adminDeleteUserPage.html', users=session['user_list'], name=session['admin_name'])
    else:
        return render_template('index.html', error=None)



@app.route("/user-list")
def user_list():
    if 'adminId' in session:
        if request.method == 'GET':
            response = requests.get('http://localhost:8080/admin/api/v1/user-list', json={'adminId':session['adminId']} )
            data = response.json()
            if response.status_code == 200:
                print(data['data'])
                session['user_list'] = []
                for item in data['data']:
                    key_object_pair = {
                    "name": item['name'],
                    "_id": item["_id"],
                    "email": item["email"],
                    "phone": item["phone"]
                    }
                    session['user_list'].append(key_object_pair)
                print(session['user_list'])
                return render_template('adminUserList.html', users=session['user_list'], name=session['admin_name'])
    else:
        return render_template('index.html', error=None)
    
  

@app.route("/payment-list")
def payment_list():
    if 'adminId' in session:
        if request.method == 'GET':
            response = requests.get('http://localhost:8080/admin/api/v1/payment-list', json={'adminId':session['adminId']})
            data = response.json()
            if response.status_code == 200:
                session['payment-list'] = []
                for item in data['data']:
                    key_object_pair = {
                    "user": item['userId'],
                    "_id": item["_id"],
                    "totalAmount": item['totalAmount'],
                    "paymentStatus":item['paymentStatus'],
                    }
                    session['payment-list'].append(key_object_pair)
                print(session['payment-list'])
                return render_template('paymentList.html', name=session['admin_name'], payment_list=session['payment-list'])
    else:
        return render_template('index.html', error=None)
    
@app.route("/delete-user", methods=['GET',"POST"])
def user_delete():
    if 'adminId' in session:
        if request.method == 'POST':
            userId = request.form['userId']
            response = requests.delete('http://localhost:8080/admin/api/v1/delete-user', json={'adminId':session['adminId'], 'userId':userId})
            if response.status_code == 200:
                print("deleted")
                response = requests.get('http://localhost:8080/admin/api/v1/user-list', json={'adminId':session['adminId']} )
                data = response.json()
                if response.status_code == 200:
                    print(data['data'])
                    session['user_list'] = []
                    for item in data['data']:
                        key_object_pair = {
                        "name": item['name'],
                        "_id": item["_id"],
                        "email": item["email"],
                        "phone": item["phone"]
                        }
                        session['user_list'].append(key_object_pair)
                    print(session['user_list'])
                    return render_template('adminDeleteUserPage.html', users=session['user_list'], name=session['admin_name'])
                else:
                    return render_template('index.html', error=None)
            else:
                print(response['message'])

                
    else:
        return render_template('index.html', error=None)




@app.route('/', methods=['GET', 'POST'])
def login():
    if 'userID' in session:
        # return redirect(url_for('userDashboard',email=session['email']))
        getImages(session['userID'], session['name'])
        return render_template('userDashboard.html',img=session['img'], name=session['name'], id =session['userID'] )
        # return render_template('userDashboard.html', email=session['email'], id = session['userID'])
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Make a request to the REST API
        response = requests.post('http://localhost:8080/user/api/v1/login', json={'email': email, 'password': password})

        if response.status_code == 200:
            # Login successful, redirect to video_feed
            data = response.json()
            session['name'] = data['name']
            session['userID'] = data['userID']
            return render_template('userDashboard.html', name=session['name'], id =session['userID'] )
        else:
            # Login failed, show an error message
            return render_template('index.html', error='Invalid email or password')

    return render_template('index.html', error=None)

# till here

# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/login")
# def login():
#     return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')

        # Prepare data for API request
        data = {
            'name': name,
            'phone': phone,
            'email': email,
            'password': password
        }

        # Make a request to the API
        response = requests.post('http://localhost:8080/user/api/v1/register', json=data)

        if response.status_code == 200:
            data = response.json()
            print(data)
            session['name'] = data['data']['name']
            session['email'] = data['data']['email']
            session['phone'] = data['data']['phone']
            session['userID'] = data['data']['_id']

            # session['userID'] = response.data['userID']
            return render_template('userDashboard.html', email=session['email'], name=session['name'], id=session['userID'] )
        else:
            return render_template('index.html', error='Some Error Exists.')

    return render_template('register.html')

# @app.route("/register")
# def register():
#     return render_template("register.html")

@app.route('/video_feed')
def video_feed():
#default called trackbar function 
    def take_screenshot(frame):
            global screenshot_count
            screenshot_count += 1
            filename = f"screenshot_{screenshot_count}.png"
            cv2.imwrite(filename, frame)
            print(f"Screenshot saved as '{filename}'")
            print(session['userID'])
            # Send the screenshot to a REST API endpoint
            api_endpoint = "http://localhost:8080/user/api/v1/uploadImage"
            files = {"img": open(filename, "rb"), "userID":(None,session['userID'])}
            response = requests.post(api_endpoint,files = files)

            # Check if the request was successful
            if response.status_code == 200:
                print("Screenshot uploaded successfully")
            else:
                print(f"Failed to upload screenshot: {response.status_code} - {response.reason}")

            # Delete the local screenshot file after uploading
            # os.remove(filename)
    
    def setValues(x):
        print("")


    # Creating the trackbars needed for adjusting the marker colour
    cv2.namedWindow("Color detectors")
    cv2.createTrackbar("Upper Hue", "Color detectors", 153, 180,setValues)
    cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255,setValues)
    cv2.createTrackbar("Upper Value", "Color detectors", 255, 255,setValues)
    cv2.createTrackbar("Lower Hue", "Color detectors", 64, 180,setValues)
    cv2.createTrackbar("Lower Saturation", "Color detectors", 72, 255,setValues)
    cv2.createTrackbar("Lower Value", "Color detectors", 49, 255,setValues)


    # Giving different arrays to handle colour points of different colour
    bpoints = [deque(maxlen=1024)]
    gpoints = [deque(maxlen=1024)]
    rpoints = [deque(maxlen=1024)]
    ypoints = [deque(maxlen=1024)]

    # These indexes will be used to mark the points in particular arrays of specific colour
    blue_index = 0
    green_index = 0
    red_index = 0
    yellow_index = 0

    #The kernel to be used for dilation purpose 
    kernel = np.ones((5,5),np.uint8)

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
    colorIndex = 0

    # Here is code for Canvas setup
    paintWindow = np.zeros((471,636,3)) + 255
    paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
    paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), colors[0], -1)
    paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), colors[1], -1)
    paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), colors[2], -1)
    paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), colors[3], -1)

    cv2.putText(paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)
    cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)


    # Loading the default webcam of PC.
    cap = cv2.VideoCapture(0)
    
    # Keep looping
    while True:
        
# Reading the frame from the camera
        ret, frame = cap.read()
        #Flipping the frame to see same side of yours
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
        u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
        u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
        l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
        l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
        l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")
        Upper_hsv = np.array([u_hue,u_saturation,u_value])
        Lower_hsv = np.array([l_hue,l_saturation,l_value])


        # Adding the colour buttons to the live frame for colour access
        frame = cv2.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
        frame = cv2.rectangle(frame, (160,1), (255,65), colors[0], -1)
        frame = cv2.rectangle(frame, (275,1), (370,65), colors[1], -1)
        frame = cv2.rectangle(frame, (390,1), (485,65), colors[2], -1)
        frame = cv2.rectangle(frame, (505,1), (600,65), colors[3], -1)
        cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)


        # Identifying the pointer by making its mask
        Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
        Mask = cv2.erode(Mask, kernel, iterations=1)
        Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
        Mask = cv2.dilate(Mask, kernel, iterations=1)
        # Find contours for the pointer after idetifying it
        cnts,_ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        center = None

        # Ifthe contours are formed
        if len(cnts) > 0:
# sorting the contours to find biggest 
            cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
            # Get the radius of the enclosing circle around the found contour
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            # Draw the circle around the contour
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            # Calculating the center of the detected contour
            M = cv2.moments(cnt)
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

             # Now checking if the user wants to click on any button above the screen 
            if center[1] <= 65:
                if 40 <= center[0] <= 140: # Clear Button
                    bpoints = [deque(maxlen=512)]
                    gpoints = [deque(maxlen=512)]
                    rpoints = [deque(maxlen=512)]
                    ypoints = [deque(maxlen=512)]

                    blue_index = 0
                    green_index = 0
                    red_index = 0
                    yellow_index = 0
                    paintWindow[67:,:,:] = 255
                elif 160 <= center[0] <= 255:
                        colorIndex = 0 # Blue
                elif 275 <= center[0] <= 370:
                        colorIndex = 1 # Green
                elif 390 <= center[0] <= 485:
                        colorIndex = 2 # Red
                elif 505 <= center[0] <= 600:
                        colorIndex = 3 # Yellow
            else :
                if colorIndex == 0:
                    bpoints[blue_index].appendleft(center)
                elif colorIndex == 1:
                    gpoints[green_index].appendleft(center)
                elif colorIndex == 2:
                    rpoints[red_index].appendleft(center)
                elif colorIndex == 3:
                    ypoints[yellow_index].appendleft(center)
        # Append the next deques when nothing is detected to avois messing up
        else:
            bpoints.append(deque(maxlen=512))
            blue_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1
         # Draw lines of all the colors on the canvas and frame 
        points = [bpoints, gpoints, rpoints, ypoints]
        for i in range(len(points)):
             for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue
                    cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                    cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)
        # Show all the windows
        cv2.imshow("Tracking", frame)
        cv2.imshow("Paint", paintWindow)
        cv2.imshow("mask",Mask)

        # If the 'q' key is pressed then stop the application 
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            take_screenshot(paintWindow)
        elif key == ord('q'):
            break
    # Release the camera and all resources
    cap.release()
    cv2.destroyAllWindows()
    return render_template('/userDashboard.html')

@app.route('/drawing_app')
def drawing_app():
    return render_template('drawing_app.html')

if __name__ == "__main__":
    app.run(debug=True)