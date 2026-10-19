# AI Hand Gesture Computer Control

A Python computer-vision project that uses a webcam to recognize hand landmarks and map deliberate hand gestures to desktop actions such as moving the mouse, clicking, scrolling, and adjusting system volume.

> **Status:** Project setup and implementation in progress.

## Planned Features

- Real-time hand tracking with OpenCV and MediaPipe
- Gesture-based mouse cursor movement
- Click and drag actions with safeguards
- Scrolling and volume controls
- On-screen gesture/status indicators
- Emergency quit and pause controls to prevent unwanted input
- Screenshots, demo video, and gesture-action documentation

## Technology Stack

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- PyCAW (Windows volume control; optional platform-specific feature)

## Setup (Windows)

Use Python 3.12 for compatibility with the selected MediaPipe version.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python hand_gesture_control.py
```

If PowerShell blocks activation, run this in the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Safety

- Press **Q** to quit the application.
- Press **P** to pause or resume computer control.
- Test in a safe environment and keep the pause/quit keys accessible.
- Desktop automation may cause unintended actions; start with low sensitivity and avoid using it for sensitive transactions.

## Gesture Mapping

The final mappings will be documented here after implementation and testing.

## Project Structure

```text
YRNOVATECH-INTERNSHIP-TASK-4/
├── hand_gesture_control.py
├── requirements.txt
├── README.md
├── screenshots/
└── demo/
```

## Demo and Screenshots

Add verified project screenshots to `screenshots/` and the final demonstration video to `demo/` once recorded.

## Learning Outcomes

This project explores landmark-based hand tracking, geometric gesture interpretation, real-time computer vision, and safe desktop automation.

## Internship

Created as a project for the YR NOVATECH AI & ML Internship — Task 4.
