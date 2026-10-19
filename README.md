# AI Hand Gesture Computer Control

A Python computer-vision project that estimates hand landmarks and maps simple hand gestures to desktop actions.

## Hosted Streamlit demo

The hosted app is an **interactive hand-gesture lab**, not just a project description. Visitors can:

- Take a picture using the browser camera, or upload a PNG/JPG/WEBP image.
- Detect up to two hands using MediaPipe.
- View the 21-point hand skeleton drawn over the image.
- See a rule-based estimate such as open palm, fist, pointing, or victory/peace.
- See estimated handedness and the number of extended fingers.

The hosted app analyses a **single image per capture**. It is not continuous live video and cannot control a visitor's local mouse or Windows volume from a hosted server.

## Local desktop-controller features

The separate `hand_gesture_control.py` program runs on a compatible Windows computer with a webcam:

- Cursor movement using the index fingertip
- Pinch-to-click
- Upward scrolling using a two-finger gesture
- Windows volume increase using a thumbs-up gesture
- Press **P** to pause/resume; press **Q** or **Esc** to quit

## Technologies

Python, Streamlit, OpenCV, MediaPipe, NumPy, Pillow, PyAutoGUI, PyCAW, and comtypes.

The hosted image demo and local controller use landmark-based geometric rules, not a separately trained gesture classifier.

## Run the Streamlit app locally

Use Python 3.11 or 3.12 in a virtual environment.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Run the desktop controller locally (Windows only)

Use a separate environment or install the desktop requirements in your environment:

```powershell
py -3.12 -m venv .venv-desktop
.\.venv-desktop\Scripts\Activate.ps1
pip install -r requirements-desktop.txt
python hand_gesture_control.py
```

## Deploy to Streamlit Community Cloud

1. Open Streamlit Community Cloud and sign in with GitHub.
2. Choose **Create app**.
3. Select repository `pratham655/YRNOVATECH-INTERNSHIP-TASK-4`, branch `main`, and main file `app.py`.
4. Deploy. Python dependencies are listed in `requirements.txt`; Linux system libraries are listed in `packages.txt`.
5. If already deployed, Streamlit Cloud should rebuild after the commit. If not, open **Manage app** and reboot the app.

## Safety and privacy

- The hosted app does not execute desktop actions.
- Images are processed by the hosted app to return landmarks and a gesture estimate. Avoid uploading sensitive images.
- The local controller starts paused. Test it with harmless applications first and keep PyAutoGUI's corner failsafe enabled.

## Internship

YR NOVATECH AI & ML Internship — Task 4
