# utils.py
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def normalized_to_pixel(nx, ny, frame_w, frame_h):
    px = int(min(max(nx, 0.0), 1.0) * (frame_w - 1))
    py = int(min(max(ny, 0.0), 1.0) * (frame_h - 1))
    return px, py

def draw_hand_landmarks(frame, raw, frame_w, frame_h, color=(90,200,255)):
    try:
        mp_drawing.draw_landmarks(frame, raw, mp_hands.HAND_CONNECTIONS)
    except Exception:
        try:
            for lm in raw.landmark:
                x = int(lm.x * frame_w)
                y = int(lm.y * frame_h)
                cv2.circle(frame, (x, y), 3, color, -1)
        except Exception:
            pass

def rounded_rect(frame, rect, color, radius=12, thickness=-1, alpha=0.45):
    x1, y1, x2, y2 = rect
    overlay = frame.copy()
    cv2.rectangle(overlay, (x1,y1), (x2,y2), color, thickness=cv2.FILLED, lineType=cv2.LINE_AA)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    if thickness != -1 and thickness > 0:
        cv2.rectangle(frame, (x1,y1), (x2,y2), (200,200,200), thickness, lineType=cv2.LINE_AA)

def draw_text_center(frame, text, center, font_scale=0.7, color=(230,230,230), thickness=2):
    font = cv2.FONT_HERSHEY_SIMPLEX
    size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    x = int(center[0] - size[0] / 2)
    y = int(center[1] + size[1] / 2)
    cv2.putText(frame, text, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)

def draw_button(frame, rect, text, fill=(40,40,50), text_color=(230,230,230), highlight=False, font_scale=0.62):
    x, y, w, h = rect
    overlay = frame.copy()
    cv2.rectangle(overlay, (x,y), (x + w, y + h), fill, -1, lineType=cv2.LINE_AA)
    cv2.addWeighted(overlay, 0.9, frame, 0.1, 0, frame)
    if highlight:
        cv2.rectangle(frame, (x-3,y-3), (x+w+3,y+h+3), (100,180,255), 2, lineType=cv2.LINE_AA)
    font = cv2.FONT_HERSHEY_SIMPLEX
    txt_x = x + 14
    txt_y = y + int(h * 0.62)
    cv2.putText(frame, str(text), (txt_x, txt_y), font, font_scale, text_color, 1, cv2.LINE_AA)
