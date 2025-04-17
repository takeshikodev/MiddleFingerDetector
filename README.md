# MiddleFingerDetector

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
    - [Test Mode](#test-mode)
    - [Live Mode](#live-mode)
5. [How It Works](#how-it-works)
6. [Configuration](#configuration)
7. [License](#license)

## Overview

**MiddleFingerDetector** is a Python application that uses a webcam and the MediaPipe library to detect the "middle finger" gesture in real-time. When the gesture is detected, the program can either print a message (in **Test Mode**) or trigger a system shutdown (in **Live Mode**). It is designed to help recognize hand gestures with high accuracy, utilizing OpenCV and MediaPipe for fast processing.

## Features

- Detects the "middle finger" gesture.
- Works with **one or two hands**.
- Can be run in **Test Mode** (just logs the detection) or **Live Mode** (triggers a system shutdown).
- Compatible with **Windows**, **Linux**, and **macOS**.
- Uses **MediaPipe** for hand landmark detection.
- Displays video feed and updates in real-time.

## Installation

To use this project, follow these steps to install the necessary dependencies:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/takeshikodev/MiddleFingerDetector.git
    cd MiddleFingerDetector
    ```

2. **Set up a virtual environment (optional but recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate     # On Windows
    ```

3. **Install required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

   The `requirements.txt` should contain:
    ```text
    opencv-python
    mediapipe
    ```

4. **Download and install MediaPipe** (if not installed via `requirements.txt`):
    ```bash
    pip install mediapipe
    ```

## Usage

To run the program, simply execute the script:

```bash
python main.py
```

By default, the program will run in **Test Mode**, where it will detect the gesture and print a message when detected. If you want to trigger a system shutdown, you can switch to **Live Mode**.

### Test Mode

In **Test Mode**, the program will log the detection of the middle finger but will not shut down the system.
To enable **Test Mode**, you can run the script with the default `test_mode=True`.

```bash
python main.py
```

You will see something like this in the terminal:

```pgsql
[INFO] MiddleFingerDetector initialized - TEST MODE (no shutdown)
[INFO] Video stream started (press ESC to exit)
```

### Live Mode

In **Live Mode**, the system will shut down when the middle finger gesture is detected.
To enable **Live Mode**, change the `test_mode` parameter to `False` in the code:

```python
detector = MiddleFingerDetector(test_mode=False)
```

After detecting the gesture, the program will trigger a system shutdown on supported operating systems.

```bash
[EVENT] Middle finger detected — shutting down...
```

## How It Works

1. **Camera Feed:** The program accesses the webcam and streams the video feed in real-time.
2. **Hand Detection:** Using MediaPipe, the program detects hands and their landmarks in the video frames.
3. **Gesture Recognition:** It checks whether only the middle finger is raised, based on the relative positions of the hand landmarks.
4. **Action Trigger:** If the middle finger is detected, the program either logs the event (Test Mode) or triggers a system shutdown (Live Mode).

## Configuration

- **Hand Detection:** The program uses MediaPipe to detect up to two hands in each frame (max_num_hands=2).
- **Shutdown Commands:** The shutdown command varies depending on the operating system:
  - **Windows:** `shutdown /s /t 1`
  - **Linux:** `shutdown -h now`
  - **macOS:** `sudo shutdown -h now`

If the shutdown command is unsupported (e.g., on an unknown OS), the program will print an error message instead.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) for details.
