# gesture-controlled-mouse

A compact Python project that controls the system mouse using real-time hand gestures detected with MediaPipe and OpenCV. `pyautogui` is used for system-level mouse actions. This repository contains two main scripts:

- `VirtualMouse.py` — main app that reads camera frames, detects gestures and maps them to mouse actions.
- `HandTracking.py` — reusable MediaPipe-based hand detector module (landmarks, finger state, distance helper).


---

## Features
- Real-time hand tracking with MediaPipe.
- Cursor movement driven by the index finger with smoothing to reduce jitter.
- Left click via pinch (index + middle finger close together).
- Scrolling using the open hand and the rock sign gesture.
- Lightweight, modular code: gesture logic separated from the tracking module.

---

## Gestures (implemented)
Below are the gestures the code currently recognises **exactly as implemented** in `VirtualMouse.py`.

1. **Move cursor (Index finger only)**
   - Condition: `fingers[1] == 1 and fingers[2] == 0`.
   - Landmarks: index fingertip (id `8`).
   - Behaviour: Moves cursor smoothly to index fingertip position.
   - Visual feedback: filled circle at the index tip.

2. **Left click (Pinch: Index + Middle fingers)**
   - Condition: `fingers[1] == 1 and fingers[2] == 1` and distance between landmarks `8` (index tip) and `12` (middle tip) < `clickThreshold` and at least 0.5s since last click.
   - Action: `pyautogui.click()`.
   - Visual feedback: green-filled circle at the mid-point when the click is triggered.

3. **Scroll Down (Open hand)**
   - Condition: `fingers == [1, 1, 1, 1, 1]` (all fingers up).
   - Action: `pyautogui.scroll(-scrollSpeed * scrollSensitivity)`.
   - Visual feedback: text “Open Hand (Scroll Down)”.

4. **Scroll Up (Rock Sign)**
   - Condition: `fingers[1] == 1 and fingers[4] == 1 and fingers[0] == 0 and fingers[2] == 0 and fingers[3] == 0` (index + pinky up only).
   - Action: `pyautogui.scroll(scrollSpeed * scrollSensitivity)`.
   - Visual feedback: text “Rock Sign (Scroll Up)”.

> Implementation details: `fingers` array = `[thumb, index, middle, ring, pinky]`.

---

## Configuration & parameters
Defaults from the code:

- `wCam, hCam = 640, 480` — camera resolution.
- `frameR = 100` — margin inside camera frame.
- `smoothening = 7` — cursor smoothing factor.
- `clickThreshold = 100` — distance threshold for pinch click.
- `scrollSpeed = 2` — scroll multiplier.
- `scrollSensitivity = 20` — additional scroll multiplier.
- `pyautogui.FAILSAFE = False` — disables failsafe (be cautious).

---

## Files in this repo
- `VirtualMouse.py` — main application
- `HandTracking.py` — MediaPipe-based helper module
- `requirements.txt` — minimal dependencies
- `README.md` — project documentation

---

## Minimal `requirements.txt`
```txt
opencv-python>=4.5
mediapipe>=0.8
pyautogui>=0.9
numpy>=1.22
```
## Installation & Run
1. (Optional) Create a virtual environment:
   ``` bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac / Linux
    source venv/bin/activate
    ```
2. Install dependencies:
   ``` bash
   pip install -r requirements.txt
   ```
3. Run the app:
    ``` bash
    python VirtualMouse.py
    ```
4. To stop: close the OpenCV window or press Ctrl+C in the terminal.
