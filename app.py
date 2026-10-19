import streamlit as st

st.set_page_config(
    page_title="AI Hand Gesture Computer Control",
    page_icon="✋",
    layout="wide",
)

st.title("✋ AI Hand Gesture Computer Control")
st.subheader("A computer-vision project for hands-free desktop interaction")
st.write(
    "Explore how hand landmarks can be mapped to common computer actions. "
    "This page is a project showcase; the actual webcam-based mouse and "
    "volume controller runs locally on a compatible Windows computer."
)

st.link_button(
    "View source code on GitHub",
    "https://github.com/pratham655/YRNOVATECH-INTERNSHIP-TASK-4",
)

st.divider()

metric1, metric2, metric3 = st.columns(3)
metric1.metric("Vision pipeline", "OpenCV + MediaPipe")
metric2.metric("Interaction", "Hand landmarks")
metric3.metric("Platform for controls", "Windows desktop")

st.header("What the project does")
left, right = st.columns([1, 1])
with left:
    st.markdown(
        """
        - **Cursor movement:** moves the pointer using the index fingertip.
        - **Pinch to click:** detects the distance between the thumb and index fingertip.
        - **Two-finger scroll:** recognizes raised index and middle fingers.
        - **Thumbs-up:** can increase Windows system volume.
        - **Safety controls:** starts paused; press **P** to pause/resume and **Q** or **Esc** to quit.
        """
    )
with right:
    st.info(
        "Safety first: the desktop controller starts paused. Test with harmless "
        "applications first, and keep the PyAutoGUI corner failsafe enabled."
    )
    st.caption(
        "This showcase does not access your webcam or control the visitor's "
        "mouse. Browser permissions and operating-system security prevent this "
        "page from controlling the local desktop directly."
    )

st.header("Explore the gesture mapping")
gesture = st.selectbox(
    "Choose a gesture or input",
    [
        "Move index fingertip",
        "Pinch thumb + index",
        "Raise index + middle fingers",
        "Thumbs-up",
        "Press P",
        "Press Q or Esc",
    ],
)
descriptions = {
    "Move index fingertip": (
        "Cursor movement",
        "The index fingertip's normalized x/y coordinates are mapped to screen coordinates "
        "with a margin and smoothing to reduce jitter.",
    ),
    "Pinch thumb + index": (
        "Mouse click",
        "The distance between the thumb tip and index fingertip is compared with a "
        "threshold. A click is triggered on the transition into a pinch, with a cooldown.",
    ),
    "Raise index + middle fingers": (
        "Scroll upward",
        "The app checks whether the index and middle fingertips are above their respective "
        "finger joints, then scrolls at a limited interval.",
    ),
    "Thumbs-up": (
        "Increase volume",
        "A simple landmark rule detects the thumbs-up pose. On Windows, PyCAW adjusts "
        "the master volume in small steps when the control is active.",
    ),
    "Press P": (
        "Pause / resume",
        "Toggles desktop control on and off. The program starts paused to avoid accidental input.",
    ),
    "Press Q or Esc": (
        "Exit",
        "Stops the webcam loop and closes the OpenCV window.",
    ),
}
action, explanation = descriptions[gesture]
st.success(f"**Action:** {action}")
st.write(explanation)

st.header("How it works")
st.markdown(
    """
    1. **Capture:** OpenCV reads frames from the webcam.
    2. **Detect:** MediaPipe Hands estimates 21 landmarks on a visible hand.
    3. **Interpret:** Python uses geometric rules, such as fingertip distances and joint positions,
       to identify interaction gestures.
    4. **Act:** PyAutoGUI sends mouse actions, while PyCAW handles Windows volume changes.
    """
)

with st.expander("Technical details"):
    st.markdown(
        """
        - **Language:** Python
        - **Computer vision:** OpenCV and MediaPipe
        - **Desktop input:** PyAutoGUI
        - **Windows audio:** PyCAW and comtypes
        - **Recognition approach:** landmark-based geometric rules; not a separately trained classifier
        - **Runtime:** local Windows desktop with a webcam for the actual control program
        """
    )

st.header("Run the actual desktop controller")
st.write(
    "The controller cannot be run from this hosted showcase because it needs direct webcam, "
    "mouse, and Windows audio access. To run it locally, follow the setup instructions in the repository README."
)
st.code(
    "py -3.12 -m venv .venv\n"
    ".\\.venv\\Scripts\\Activate.ps1\n"
    "pip install -r requirements.txt\n"
    "python hand_gesture_control.py",
    language="powershell",
)
st.link_button(
    "Open repository installation guide",
    "https://github.com/pratham655/YRNOVATECH-INTERNSHIP-TASK-4#installation",
)

st.divider()
st.caption(
    "YR NOVATECH AI & ML Internship — Task 4 | Project showcase, not a browser-based desktop controller."
)
