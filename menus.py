# menus.py
import time
import cv2
import config
from utils import draw_button, rounded_rect, draw_text_center

class MenuManager:
    def __init__(self, frame_w, frame_h):
        self.frame_w = frame_w
        self.frame_h = frame_h

        self.categories = [
            "Veg Starter", "Non-Veg Starter", "Veg Main Course", "Non-Veg Main Course",
            "Rice & Chowmein", "Dessert", "Drinks", "Thali",
            "Ice Cream", "Specials"
        ]

        self.menu = {
            "Veg Starter": [("Paneer Tikka",120),("Crispy Corn",90),("Spring Roll",99),("Veg Samosa",40)],
            "Non-Veg Starter": [("Chicken Pakora",140),("Fish Fry",180),("Chicken Lollipop",160)],
            "Veg Main Course": [("Paneer Butter Masala",150),("Mix Veg",110),("Dal Tadka",99),("Palak Paneer",170)],
            "Non-Veg Main Course": [("Chicken Curry",160),("Mutton Kasa",220),("Egg Curry",120)],
            "Rice & Chowmein": [("Fried Rice",90),("Chowmein",80),("Veg Biryani",170),("Chicken Biryani",250)],
            "Dessert": [("Gulab Jamun",50),("Rasmalai",70),("Brownie",119),("Ice Pudding",89)],
            "Drinks": [("Coke",40),("Lassi",60),("Masala Chai",35),("Cold Coffee",99)],
            "Thali": [("Veg Thali",150),("Non-Veg Thali",230),("Special Thali",349)],
            "Ice Cream": [("Vanilla",40),("Chocolate",50),("Strawberry",50),("Kulfi",70)],
            "Specials": [("Chef Special Pasta",249),("Sizzler",399)]
        }

        self.cart = []
        self.page = "HOME"
        self.active_category = 0
        self.scroll_offset = 0

        self.panel_w = int(self.frame_w * 0.22)
        self.cart_w = 280
        self.items_visible = 4

        self.up_btn = None
        self.down_btn = None
        self.process_btn = None
        self.item_rects = []

        self.feedback = None
        self.feedback_time = 0
        self.feedback_duration = getattr(config, "FEEDBACK_DURATION", 1.2)

        # no double-add by hover
        self.last_add_times = {}
        self.add_debounce = 0.4  

        self.confirm_start_time = 0
        self.confirm_duration = 1.5

    def _set_feedback(self, text):
        self.feedback = text
        self.feedback_time = time.time()

    def _rect_contains(self, rect, x, y, pad=0):
        if rect is None or x is None or y is None:
            return False
        rx, ry, rw, rh = rect
        return (rx - pad) <= x <= (rx + rw + pad) and (ry - pad) <= y <= (ry + rh + pad)

    def _draw_header(self, frame):
        draw_text_center(frame, "AIR TOUCHLESS MENU", (self.frame_w//2, 32), font_scale=0.92)

    def render_payment_page(self, frame, cursor=None, pinch_event=False):
        # unchanged
        h, w = self.frame_h, self.frame_w
        now = time.time()

        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (10, 10, 12), -1)
        cv2.addWeighted(overlay, 0.25, frame, 0.75, 0, frame)

        draw_text_center(frame, "Select Payment Method", (w//2, 120), font_scale=1.0)

        pay_w = int(w * 0.45)
        pay_h = int(56 * (h / 720))
        pay_x = (w - pay_w) // 2

        cod_rect = (pay_x, (h//2) - pay_h - 10, pay_w, pay_h)
        online_rect = (pay_x, (h//2) + 10, pay_w, pay_h)

        draw_button(frame, cod_rect, "CASH ON DELIVERY")
        draw_button(frame, online_rect, "ONLINE PAYMENT")

        if cursor is not None:
            cx, cy = cursor
            if self._rect_contains(cod_rect, cx, cy, pad=20):
                self.page = "PAY_CONFIRM"
                self.confirm_start_time = now
                self._set_feedback("Your order is processing")
                time.sleep(0.05)

        return frame

    def render_confirm_page(self, frame):
        # unchanged
        h, w = self.frame_h, self.frame_w
        now = time.time()

        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 1 - 0.5, 0, frame)

        cv2.putText(frame, "Your order is processing...", (w//2 - 260, h//2 - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (80,220,120), 2)

        if (now - self.confirm_start_time) >= self.confirm_duration:
            self.cart.clear()
            self.page = "HOME"
            self.scroll_offset = 0
            self.feedback = None

        return frame

    def render(self, frame, cursor=None, pinch_event=False, hand_raw=None):

        now = time.time()

        if self.page == "PAY":
            return self.render_payment_page(frame, cursor, pinch_event)
        if self.page == "PAY_CONFIRM":
            return self.render_confirm_page(frame)

        h, w = self.frame_h, self.frame_w

        rounded_rect(frame, (8, 8, 8+self.panel_w, h-12), (28,28,32), radius=12, alpha=0.50)
        rounded_rect(frame, (w-self.cart_w-12, 8, w-8, h-8), (28,28,32), radius=12, alpha=0.50)

        self._draw_header(frame)

        category_rects = []
        cat_h = int(54 * (h/720))
        x0 = 18

        # LEFT CATEGORY PANEL + HOVER SELECT
        for i, cat in enumerate(self.categories):
            y = 80 + i * (cat_h + 10)
            rect = (x0, y, self.panel_w - 36, cat_h)
            category_rects.append((i, rect, cat))

            hovered = cursor and self._rect_contains(rect, cursor[0], cursor[1], pad=6)

            draw_button(frame, rect, cat, highlight=(i == self.active_category or hovered))

            if hovered:
                self.active_category = i
                self.scroll_offset = 0

        items = self.menu[self.categories[self.active_category]]

        base_x = self.panel_w + 36
        item_w = w - base_x - self.cart_w - 50
        item_h = int(86 * (h/720))

        max_offset = max(0, len(items) - self.items_visible)
        self.scroll_offset = max(0, min(self.scroll_offset, max_offset))

        # ITEMS + HOVER ADD
        self.item_rects = []
        for slot in range(self.items_visible):
            idx = self.scroll_offset + slot
            if idx >= len(items): break

            name, price = items[idx]
            y = 150 + slot * (item_h + 12)
            rect = (base_x, y, item_w, item_h)

            hovered = cursor and self._rect_contains(rect, cursor[0], cursor[1], pad=10)
            draw_button(frame, rect, f"{name}   Rs.{price}", highlight=hovered)

            self.item_rects.append((idx, rect, name, price))

            if hovered:
                last = self.last_add_times.get(idx, 0)
                if (now - last) > self.add_debounce:
                    self.cart.append((name, price))
                    self.last_add_times[idx] = now
                    self._set_feedback(f"Added {name}")

        # SCROLL BUTTONS (HOVER)
        if len(items) > self.items_visible:
            self.up_btn = (base_x + item_w + 10, 150, 46, 46)
            self.down_btn = (base_x + item_w + 10,
                             150 + (item_h + 12)*(self.items_visible-1), 46, 46)

            draw_button(frame, self.up_btn, "^")
            draw_button(frame, self.down_btn, "v")

            if cursor and self._rect_contains(self.up_btn, cursor[0], cursor[1], pad=6):
                self.scroll_offset = max(0, self.scroll_offset - 1)

            if cursor and self._rect_contains(self.down_btn, cursor[0], cursor[1], pad=6):
                self.scroll_offset = min(max_offset, self.scroll_offset + 1)

        # CART, TOTAL & PROCESS BUTTON
        cart_x = w - self.cart_w - 12
        draw_text_center(frame, "CART", (cart_x+self.cart_w//2, 50), font_scale=0.85)

        y0 = 90
        for i, (n,p) in enumerate(self.cart[-10:]):
            cv2.putText(frame, f"{n[:20]} Rs.{p}", (cart_x+15, y0+i*26),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (230,230,230), 1)

        subtotal = sum(p for _,p in self.cart)
        gst = subtotal * 0.18
        total = subtotal + gst

        cv2.putText(frame, f"Total: Rs.{total:.2f}", (cart_x+15, h-90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)

        btn_w = self.cart_w - 40
        btn_h = int(56 * (h/720))
        btn_x = cart_x + 15
        btn_y = h - int(120*(h/720)) - btn_h

        self.process_btn = (btn_x, btn_y, btn_w, btn_h)
        hovered = cursor and self._rect_contains(self.process_btn, cursor[0], cursor[1], pad=10)

        draw_button(frame, self.process_btn, "Process To Pay", highlight=hovered)

        if hovered:
            if len(self.cart) == 0:
                self._set_feedback("Cart is empty")
            else:
                self.page = "PAY"
                self._set_feedback("Choose payment method")

        # FEEDBACK TEXT
        if self.feedback and (time.time()-self.feedback_time) < self.feedback_duration:
            cv2.putText(frame, self.feedback, (base_x, h - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.78, (80,235,130), 2)

        return frame
