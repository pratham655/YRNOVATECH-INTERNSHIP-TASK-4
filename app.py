import math

import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
from PIL import Image

st.set_page_config(page_title="AI Hand Gesture Lab", page_icon="✋", layout="wide")

st.title("✋ AI Hand Gesture Lab")
st.write(
    "Capture a hand image with your camera or upload a photo. The app detects hand landmarks, "
    "draws the 21-point skeleton, and estimates a gesture using simple landmark rules."
)
st.warning(
    "This hosted demo analyses one image at a time. It does not continuously stream video or "
    "control your computer's mouse/volume. Run hand_gesture_control.py locally on Windows for that."
)

@st.cache_resource
def get_hands_model():
    return mp.solutions.hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        model_complexity=1,
        min_detection_confidence=0.45,
    )

def classify_gesture(hand):
    lm = hand.landmark
    # For fingers other than the thumb, a fingertip above its PIP joint usually means extended.
    index = lm[8].y < lm[6].y
    middle = lm[12].y < lm[10].y
    ring = lm[16].y < lm[14].y
    pinky = lm[20].y < lm[18].y
    # Thumb extension is estimated from horizontal distance from the palm's index MCP.
    thumb = abs(lm[4].x - lm[5].x) > abs(lm[3].x - lm[5].x) * 1.15
    fingers = [thumb, index, middle, ring, pinky]
    count = sum(fingers)

    if index and middle and not ring and not pinky:
        return "Victory / Peace ✌️", count
    if index and not middle and not ring and not pinky:
        return "Pointing ☝️", count
    if count >= 4:
        return "Open palm ✋", count
    if count == 0:
        return "Fist ✊", count
    if thumb and not index and not middle and not ring and not pinky:
        return "Thumbs-up / thumb extended 👍", count
    return "Other / transitional gesture", count

def analyse_image(uploaded):
    pil_image = Image.open(uploaded).convert("RGB")
    rgb = np.array(pil_image)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    results = get_hands_model().process(rgb)
    annotated = bgr.copy()
    found = []

    if results.multi_hand_landmarks:
        for idx, hand in enumerate(results.multi_hand_landmarks):
            mp.solutions.drawing_utils.draw_landmarks(
                annotated,
                hand,
                mp.solutions.hands.HAND_CONNECTIONS,
                mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                mp.solutions.drawing_styles.get_default_hand_connections_style(),
            )
            label, count = classify_gesture(hand)
            handedness = "Hand"
            if results.multi_handedness and idx < len(results.multi_handedness):
                handedness = results.multi_handedness[idx].classification[0].label
            found.append({"hand": handedness, "gesture": label, "extended_fingers": count})
    annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
    return pil_image, annotated_rgb, found

tab_camera, tab_upload = st.tabs(["📷 Use camera", "📁 Upload image"])
with tab_camera:
    camera_image = st.camera_input("Take a picture of your hand", help="Keep the full hand in frame with good lighting.")
with tab_upload:
    uploaded_image = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg", "webp"])

source = camera_image if camera_image is not None else uploaded_image
if source is None:
    st.info("Take a camera picture or upload a clear photo of one or both hands to start.")
    st.markdown("**Tips for better detection**")
    st.markdown("- Keep the whole hand visible, including fingertips and wrist.\n- Use bright, even lighting.\n- Keep your hand a little away from the camera.\n- Avoid busy backgrounds where possible.")
else:
    try:
        original, annotated, detections = analyse_image(source)
        left, right = st.columns(2)
        with left:
            st.subheader("Input image")
            st.image(original, use_container_width=True)
        with right:
            st.subheader("Detected landmarks")
            st.image(annotated, use_container_width=True)
        if detections:
            st.success(f"Detected {len(detections)} hand(s).")
            for i, item in enumerate(detections, start=1):
                with st.container(border=True):
                    st.subheader(f"Hand {i}: {item['gesture']}")
                    a, b = st.columns(2)
                    a.metric("Handedness estimate", item["hand"])
                    b.metric("Extended fingers", f"{item['extended_fingers']} / 5")
            st.caption("Gesture names are rule-based estimates, not a trained classifier. Some poses can be ambiguous depending on hand orientation.")
        else:
            st.error("No hand detected in this image.")
            st.write("Try a brighter, sharper photo with your entire hand visible and the palm facing the camera.")
    except Exception as exc:
        st.error("The image could not be processed.")
        st.exception(exc)

with st.expander("How this works"):
    st.markdown(
        "1. The camera widget or uploader supplies a single image.\n"
        "2. MediaPipe Hands estimates up to 21 landmarks per hand.\n"
        "3. OpenCV draws the landmark connections.\n"
        "4. Simple geometric rules estimate a likely gesture from fingertip and joint positions."
    )
    st.caption("This app processes the image on the Streamlit server for this interaction. Avoid uploading sensitive images.")

st.divider()
st.markdown("[View the source code on GitHub](https://github.com/pratham655/YRNOVATECH-INTERNSHIP-TASK-4) · "
            "[Read local desktop-controller setup](https://github.com/pratham655/YRNOVATECH-INTERNSHIP-TASK-4#installation)")
st.caption("YR NOVATECH AI & ML Internship — Task 4")
