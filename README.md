
# AI Hand Gesture Computer Control

A Python computer-vision application that uses a webcam to track hand landmarks and control desktop actions through hand gestures.

## Features

- Real-time hand tracking
- Cursor movement using the index fingertip
- Pinch-to-click interaction
- Upward scrolling using a two-finger gesture
- Windows volume increase using a thumbs-up gesture
- Pause/resume and quit controls
- On-screen status indicators

## Technologies Used

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- PyCAW
- comtypes

## How It Works

OpenCV captures webcam frames, MediaPipe detects hand landmarks, and Python-based geometric rules interpret gestures. PyAutoGUI performs mouse actions, while PyCAW controls Windows system volume.

This implementation uses landmark-based rules rather than a separately trained gesture classifier.

## Gesture Controls

| Gesture / Input | Action |
|---|---|
| Move index fingertip | Move cursor |
| Pinch thumb and index finger | Click |
| Raise index and middle fingers | Scroll upward |
| Thumbs-up | Increase volume |
| Press P | Pause or resume |
| Press Q or Esc | Exit |

## Installation

Use Python 3.12 on Windows.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python hand_gesture_control.py
```

## Safety

The program starts paused. Press P to enable control and P again to pause. Press Q or Esc to exit. Test using harmless applications first.

## Demo Video

See the `demo/` folder for the project demonstration.

## Screenshots

See the `screenshots/` folder for screenshots of the application.

## Internship

YR NOVATECH AI & ML Internship — Task 4
