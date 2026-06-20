# app.py
from flask import Flask, render_template, Response
import cv2
import time

from gestures import HandDetector
from menus import MenuManager
from utils import draw_hand_landmarks
import config

app = Flask(__name__)

# initialize camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_W)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_H)

# ---------- ROUTES ----------

@app.route("/")
def home():
    # THIS WILL LOAD FIRST
    return render_template("home.html")


@app.route("/airmenu")
def airmenu():
    # THIS PAGE SHOWS CAMERA + MENU
    return render_template("airmenu.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


# ---------- CAMERA STREAM ----------

def generate_frames():
    global camera

    detector = HandDetector(maxHands=1)
    menu = MenuManager(config.FRAME_W, config.FRAME_H)

    smoothing = config.CURSOR_SMOOTHING
    cursor = None

    last_pinch = 0
    pinch_gap = 0.35
    last_state = False

    while True:
        success, frame = camera.read()

        if not success:
            try:
                camera.release()
            except:
                pass
            time.sleep(0.2)
            camera = cv2.VideoCapture(0)
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_W)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_H)
            continue

        frame = cv2.flip(frame, 1)
        frame_h, frame_w = frame.shape[:2]

        hands = detector.process(frame)
        raw = None
        pinch_event = False

        if hands:
            hand = hands[0]
            raw = hand["raw"]

            pos = detector.index_tip_pos(hand)
            if pos:
                nx, ny = pos

                px = int(min(max(nx, 0.0), 1.0) * (frame_w - 1))
                py = int(min(max(ny, 0.0), 1.0) * (frame_h - 1))

                if cursor is None:
                    cursor = (px, py)
                else:
                    cursor = (
                        int(cursor[0] * (1 - smoothing) + px * smoothing),
                        int(cursor[1] * (1 - smoothing) + py * smoothing)
                    )

            now = time.time()
            state = detector.is_pinch_event(hand)

            if state and not last_state and (now - last_pinch) > pinch_gap:
                pinch_event = True
                last_pinch = now

            last_state = state

            if cursor:
                cv2.circle(frame, cursor, 10, (120, 200, 255), -1)

        else:
            cursor = None
            last_state = False

        if raw:
            draw_hand_landmarks(frame, raw, frame_w, frame_h)

        frame = menu.render(frame, cursor=cursor, pinch_event=pinch_event, hand_raw=raw)

        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )


@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True, port=5050, host="0.0.0.0")
