# AI Hand Gesture Computer Control

A real-time Python computer-vision application that uses a webcam to track hand landmarks and map selected hand gestures to desktop actions on Windows.

**Internship project:** YR NOVATECH AI & ML Internship — Task 4  
**Status:** Initial implementation available; tested by the developer to run without errors.

## Features

- Real-time webcam capture and display using OpenCV
- Hand landmark tracking with MediaPipe
- Mouse cursor movement using the index fingertip
- Pinch gesture (thumb + index fingertip) to click
- Two-finger gesture to scroll upward
- Thumbs-up gesture to increase Windows system volume
- On-screen status and pinch-distance display
- Pause/resume and quit keyboard controls
- Cursor smoothing to reduce jitter

## Technology Stack

- **Python** — application logic
- **OpenCV** — webcam video capture and display
- **MediaPipe** — hand landmark detection and tracking
- **PyAutoGUI** — cursor movement, click, and scroll actions
- **PyCAW + comtypes** — Windows system-volume interface
- **math / time** — fingertip-distance calculations and action timing

## How It Works

1. OpenCV captures frames from the webcam.
2. MediaPipe detects a hand and estimates its landmarks.
3. Python rules evaluate fingertip positions and distances.
4. When computer control is enabled, PyAutoGUI performs mouse actions and PyCAW adjusts Windows volume.
5. The webcam window shows the current control state.

This implementation uses MediaPipe hand landmarks with **rule-based gesture logic**. It does not train a separate custom gesture-classification model.

## Gesture Mapping

| Input | Action |
|---|---|
| Move index fingertip | Move the mouse cursor |
| Pinch thumb and index finger together | Click once when the pinch begins |
| Raise index and middle fingers | Scroll upward |
| Thumbs-up | Increase system volume |
| Press `P` | Pause/resume computer control |
| Press `Q` or `Esc` | Quit the application |

**Current limitations:** the initial version implements upward scrolling and volume increase only. Downward scrolling, volume decrease, drag-and-drop, and additional gestures are not implemented yet.

## Requirements

- Windows
- Python 3.12 recommended
- A working webcam
- Microphone/camera permission is not required for this project; camera access is required.

## Setup (Windows PowerShell)

Clone the repository and enter the project directory:

```powershell
git clone https://github.com/pratham655/YRNOVATECH-INTERNSHIP-TASK-4.git
cd YRNOVATECH-INTERNSHIP-TASK-4
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python hand_gesture_control.py
```

If PowerShell blocks virtual-environment activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Controls and Safety

- The application starts in **PAUSED** mode.
- Press **P** to enable computer control; press it again to pause.
- Press **Q** or **Esc** to quit.
- PyAutoGUI's fail-safe is enabled: move the pointer to a screen corner to trigger its fail-safe exception.
- Test with harmless windows first. Gesture-based automation can click or scroll the real desktop, so avoid using it for payments, deleting files, or other sensitive actions.

## Project Structure

```text
YRNOVATECH-INTERNSHIP-TASK-4/
├── hand_gesture_control.py
├── requirements.txt
├── README.md
├── screenshots/   # Add project screenshots here
└── demo/          # Add the recorded demo here
```

## Demo and Screenshots

Add screenshots showing the webcam hand tracking and each working gesture to `screenshots/`. Add the final demonstration video to `demo/` and link it here once it has been uploaded to GitHub.

## Learning Outcomes

- Real-time webcam processing
- Hand landmark tracking
- Geometric gesture interpretation
- Desktop automation with safety controls
- Connecting Python to Windows audio controls

## Internship

Created for the YR NOVATECH AI & ML Internship — Task 4.
