# AI Hand Gesture Computer Control

A Python computer-vision project that estimates hand landmarks and maps simple hand gestures to desktop actions.

## What works in the hosted Streamlit app

The hosted app at Streamlit Community Cloud is an **interactive hand-gesture lab**, not just a project description. It lets a visitor:

- Take a picture using the browser camera, or upload a PNG/JPG/WEBP image.
- Detect up to two hands using MediaPipe.
- View the 21-point hand skeleton and connections drawn over the image.
- See a rule-based estimate such as open palm, fist, pointing, or victory/peace.
- See the estimated handedness and count of extended fingers.

The app analyses a **single image per capture**. It is not a continuous live video stream, and it cannot control the visitor's local mouse or Windows volume from a hosted server.

## Local desktop-controller features

The separate `hand_gesture_control.py` program runs on a compatible Windows computer with a webcam:

- Cursor movement using the index fingertip
- Pinch-to-click
- Upward scrolling using a two-finger gesture
- Windows volume increase using a thumbs-up gesture
- Press **P** to pause/resume; press **Q** or **Esc** to quit

## Technologies

Python, Streamlit, OpenCV, MediaPipe, NumPy, Pillow, PyAutoGUI, PyCAW, and comtypes.

The hosted image demo and local controller use landmark-based geometric rules; neither is a separately trained gesture classifier.

## Run the Streamlit app locally

Use Python 3.11 or 3.12 in a virtual environment.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Run the desktop controller locally (Windows only)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python hand_gesture_control.py
```

The desktop controller needs the original desktop dependencies available in `requirements.txt`. If you run it in a fresh environment, ensure `pyautogui`, `pycaw`, and `comtypes` are installed too.

## Deploy to Streamlit Community Cloud

1. Open Streamlit Community Cloud and sign in with GitHub.
2. Choose **Create app**.
3. Select repository `pratham655/YRNOVATECH-INTERNSHIP-TASK-4`, branch `main`, and main file `app.py`.
4. Deploy. Cloud dependencies are listed in `requirements.txt`; Linux system libraries are listed in `packages.txt`.
5. If the app was already deployed, open the app's **Manage app** menu and reboot it after the latest commit if it does not update automatically.

## Safety and privacy

- The hosted app does not execute desktop actions.
- Images are processed by the hosted app to return landmarks and a gesture estimate. Do not upload sensitive images.
- The local controller starts paused. Test it with harmless applications first and keep PyAutoGUI's corner failsafe enabled.

## Internship

YR NOVATECH AI & ML Internship — Task 4
