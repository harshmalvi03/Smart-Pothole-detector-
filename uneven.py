import cv2
import numpy as np
import webbrowser
from datetime import datetime

# --------- EMAIL FUNCTION ----------
def open_email():
    recipient = "harshmalviyaexample@gmail.com"   # change this if needed
    subject = "Pothole Complaint On Road"
    body = "We have got Pothole object near Ring Road.\n\nDate & Time: " + str(datetime.now())

    url = f"https://mail.google.com/mail/?view=cm&fs=1&to={recipient}&su={subject}&body={body}"
    webbrowser.open(url)

# --------- CAMERA ----------
cap = cv2.VideoCapture("http://192.0.0.4:8080/video")  # change YOUR_IP ccording to IP WEBCAME 

if not cap.isOpened():
    print("Camera not working")
    exit()

waiting_for_response = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # --------- RED COLOR RANGE ----------
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 + mask2

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    red_detected = False

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 5000:
            red_detected = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
            cv2.putText(frame, "RED OBJECT DETECTED", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # If detected, ask user
    if red_detected and not waiting_for_response:
        waiting_for_response = True

    if waiting_for_response:
        cv2.putText(frame, "Send Complaint? Press Y = Yes | N = No",
                    (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        key = cv2.waitKey(1)

        if key == ord('y') or key == ord('Y'):
            open_email()
            waiting_for_response = False

        elif key == ord('n') or key == ord('N'):
            waiting_for_response = False

    cv2.imshow("Smart Pothole Detection System", frame)
    cv2.imshow("Red Mask", mask)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()