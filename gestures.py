# gestures.py
import mediapipe as mp
import math
import cv2
import config

mp_hands = mp.solutions.hands

class HandDetector:
    def __init__(self, maxHands=1):
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=maxHands,
            model_complexity=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def process(self, frame):
        """Process BGR frame and return list of hands -> [{'raw': hand_landmarks, 'coords': [(x,y)...]}]."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)

        if not self.results or not self.results.multi_hand_landmarks:
            return None

        out = []
        for hand_landmarks in self.results.multi_hand_landmarks:
            # collect normalized (x,y) for first 21 landmarks
            coords = [(lm.x, lm.y) for lm in hand_landmarks.landmark]
            out.append({"raw": hand_landmarks, "coords": coords})

        return out

    def index_tip_pos(self, hand):
        """Return normalized (x,y) of index fingertip (landmark 8) or None."""
        try:
            nx, ny = hand["coords"][8]
            return nx, ny
        except Exception:
            return None

    def pinch_distance_pixels(self, hand):
        """Return pixel distance between thumb tip (4) and index tip (8) using config frame size."""
        try:
            thumb = hand["coords"][4]
            index = hand["coords"][8]
            # convert normalized to pixels using config dims
            tx = thumb[0] * config.FRAME_W
            ty = thumb[1] * config.FRAME_H
            ix = index[0] * config.FRAME_W
            iy = index[1] * config.FRAME_H
            return math.hypot(tx - ix, ty - iy)
        except Exception:
            return 9999

    def is_pinch_event(self, hand):
        """Return True if thumb & index are closer than threshold (in pixels)."""
        dist_px = self.pinch_distance_pixels(hand)
        return dist_px < config.PINCH_THRESHOLD_PIXELS
