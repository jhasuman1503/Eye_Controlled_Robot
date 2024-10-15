import cv2

from gaze_tracking import GazeTracking
import requests

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
changed = 0


while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
        requests.get("https://blynkserver.tech:9443/glWLwPguODMfakDoqFcW_Bu06zzO8ACX/update/V1?value=0",verify=False)
        requests.get("https://blynkserver.tech:9443/glWLwPguODMfakDoqFcW_Bu06zzO8ACX/update/V2?value=0",verify=False)
        requests.get("https://blynkserver.tech:9443/glWLwPguODMfakDoqFcW_Bu06zzO8ACX/update/V3?value=0",verify=False)
    elif gaze.is_right():
        changed = 1
        text = "right"
        requests.get("https://blynkserver.tech:9443/glWLwPguODMfakDoqFcW_Bu06zzO8ACX/update/V3?value=1",verify=False)
        requests.get("https://blynkserver.tech:9443/glWLwPguODMfakDoqFcW_Bu06zzO8ACX/update/V1?value=0",verify=False)
        requests.get("https://blynkserver.tech:9443/glWLwPguODMfakDoqFcW_Bu06zzO8ACX/update/V2?value=0",verify=False)
        
    elif gaze.is_left():
        changed = 1
        text = "left"
        requests.get("https://blynkserver.tech:9443/glWLwPguODMfakDoqFcW_Bu06zzO8ACX/update/V2?value=1",verify=False)
        requests.get("https://blynkserver.tech:9443/glWLwPguODMfakDoqFcW_Bu06zzO8ACX/update/V1?value=0",verify=False)
        requests.get("https://blynkserver.tech:9443/glWLwPguODMfakDoqFcW_Bu06zzO8ACX/update/V3?value=0",verify=False)
        #ser.write(b'3\n')
    elif gaze.is_center():
        text = "center"
        requests.get("https://blynkserver.tech:9443/glWLwPguODMfakDoqFcW_Bu06zzO8ACX/update/V1?value=1",verify=False)
        requests.get("https://blynkserver.tech:9443/glWLwPguODMfakDoqFcW_Bu06zzO8ACX/update/V2?value=0",verify=False)
        requests.get("https://blynkserver.tech:9443/glWLwPguODMfakDoqFcW_Bu06zzO8ACX/update/V3?value=0",verify=False)
        
        #ser.write(b'2\n')
    else:
        text = "Calibrating"
        if changed:
            requests.get("https://blynkserver.website:9443/QvFMWN162u6gfrMtV4SoF-k0IaYXumJh/update/V1?value=1",verify=False)
            requests.get("https://blynkserver.website:9443/QvFMWN162u6gfrMtV4SoF-k0IaYXumJh/update/V2?value=0",verify=False)
            requests.get("https://blynkserver.website:9443/QvFMWN162u6gfrMtV4SoF-k0IaYXumJh/update/V3?value=0",verify=False)
            changed = 1

    cv2.putText(frame, text, (0, 60), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,255), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.imshow("Eye Gaze", frame)

    if cv2.waitKey(1) == 27:
        break
webcam.release()
cv2.destroyAllWindows()
