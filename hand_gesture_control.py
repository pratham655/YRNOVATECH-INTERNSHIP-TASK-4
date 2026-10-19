import math
import time

import cv2
import mediapipe as mp
import pyautogui

# Windows volume support (provided by pycaw)
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Safety: move the mouse to a screen corner to trigger PyAutoGUI's failsafe.
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.02

SCREEN_W, SCREEN_H = pyautogui.size()
CAM_W, CAM_H = 960, 540

# Adjust these if tracking feels too sensitive.
MARGIN = 0.12
SMOOTHING = 0.25
PINCH_CLICK_DISTANCE = 0.045
SCROLL_STEP = 35
VOLUME_STEP = 0.04

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def get_volume_interface():
    """Return Windows audio endpoint interface, or None if unavailable."""
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interface, POINTER(IAudioEndpointVolume))
    except Exception as exc:
        print(f"Windows volume control unavailable: {exc}")
        return None


def clamp(value, low, high):
    return max(low, min(high, value))


def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_H)

    if not cap.isOpened():
        raise RuntimeError("Could not open webcam. Check camera permissions or try another camera index.")

    volume = get_volume_interface()
    control_enabled = False  # Start safely with computer control paused.
    previous_x, previous_y = SCREEN_W / 2, SCREEN_H / 2
    last_click_time = 0.0
    pinch_was_active = False
    last_scroll_time = 0.0
    last_volume_time = 0.0
    status = "PAUSED - press P to enable"

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=0,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    ) as hands:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Could not read a webcam frame.")
                break

            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (CAM_W, CAM_H))
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            status = "NO HAND DETECTED"
            if result.multi_hand_landmarks:
                hand = result.multi_hand_landmarks[0]
                lm = hand.landmark
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

                # Landmark positions are normalized to [0, 1].
                index_tip = lm[8]
                thumb_tip = lm[4]
                middle_tip = lm[12]
                wrist = lm[0]

                # Move cursor based on index fingertip, with a small dead-zone margin.
                mapped_x = (index_tip.x - MARGIN) / (1 - 2 * MARGIN) * SCREEN_W
                mapped_y = (index_tip.y - MARGIN) / (1 - 2 * MARGIN) * SCREEN_H
                mapped_x = clamp(mapped_x, 0, SCREEN_W - 1)
                mapped_y = clamp(mapped_y, 0, SCREEN_H - 1)

                target_x = previous_x + (mapped_x - previous_x) * SMOOTHING
                target_y = previous_y + (mapped_y - previous_y) * SMOOTHING
                previous_x, previous_y = target_x, target_y

                pinch_distance = distance(index_tip, thumb_tip)
                scroll_gesture = middle_tip.y < lm[10].y and index_tip.y < lm[6].y
                # Thumb tip moving above its joint is a rough thumbs-up cue.
                thumbs_up = thumb_tip.y < lm[3].y and all(
                    lm[tip].y > lm[tip - 2].y for tip in (8, 12, 16, 20)
                )

                if control_enabled:
                    pyautogui.moveTo(int(target_x), int(target_y), _pause=False)
                    status = "CONTROL ACTIVE"

                    # Pinch thumb + index to click once per pinch.
                    pinch_active = pinch_distance < PINCH_CLICK_DISTANCE
                    if pinch_active and not pinch_was_active and time.time() - last_click_time > 0.45:
                        pyautogui.click()
                        last_click_time = time.time()
                        status = "CLICK"
                    pinch_was_active = pinch_active

                    # Hold a two-finger-up gesture to scroll upward.
                    if scroll_gesture and time.time() - last_scroll_time > 0.22:
                        pyautogui.scroll(SCROLL_STEP)
                        last_scroll_time = time.time()
                        status = "SCROLL UP"

                    # Thumbs-up increases volume in small steps.
                    if thumbs_up and volume is not None and time.time() - last_volume_time > 0.25:
                        current = volume.GetMasterVolumeLevelScalar()
                        volume.SetMasterVolumeLevelScalar(clamp(current + VOLUME_STEP, 0.0, 1.0), None)
                        last_volume_time = time.time()
                        status = "VOLUME UP"
                else:
                    status = "PAUSED - press P to enable"
                    pinch_was_active = False

                cv2.putText(
                    frame,
                    f"Pinch: {pinch_distance:.3f}",
                    (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (255, 255, 255),
                    2,
                )

            # Persistent controls/status overlay.
            mode = "ACTIVE" if control_enabled else "PAUSED"
            cv2.rectangle(frame, (0, 0), (CAM_W, 58), (25, 25, 25), -1)
            cv2.putText(frame, f"Computer Control: {mode}", (16, 24),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 180), 2)
            cv2.putText(frame, "P: pause/resume   Q: quit", (16, 48),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
            cv2.putText(frame, status, (20, CAM_H - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 180), 2)

            cv2.imshow("AI Hand Gesture Computer Control", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or key == 27:
                break
            if key == ord("p"):
                control_enabled = not control_enabled
                pinch_was_active = False
                print("Computer control:", "ACTIVE" if control_enabled else "PAUSED")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        main()
    except pyautogui.FailSafeException:
        print("PyAutoGUI failsafe triggered. Exiting safely.")
    except KeyboardInterrupt:
        print("Stopped by user.")
