import cv2
import mediapipe as mp
import os
import platform

class MiddleFingerDetector:
    """
    Class for detecting the middle finger gesture using a webcam and triggering an action based on the gesture.

    The class uses OpenCV and MediaPipe to process video frames in real-time and detects the middle finger gesture.
    Depending on the mode (test or live), it either prints a log message or triggers a system shutdown.
    """

    def __init__(self, test_mode=True):
        """
        Initializes the MiddleFingerDetector with the specified mode.

        Args:
            test_mode (bool): If True, no system shutdown occurs when the middle finger is detected.
                If False, the system will shut down upon detection.
        """
        self.cap = cv2.VideoCapture(0)
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.75
        )
        self.drawer = mp.solutions.drawing_utils
        self.test_mode = test_mode
        self.shutdown_command = self._get_shutdown_command()

        mode_text = "TEST MODE (no shutdown)" if test_mode else "LIVE MODE (will shutdown)"
        print(f"[INFO] MiddleFingerDetector initialized - {mode_text}")

    def _get_shutdown_command(self):
        """
        Determines the shutdown command based on the operating system.

        Returns:
            str: The shutdown command appropriate for the system (Windows, Linux, or macOS).
            None: If the operating system is unsupported.
        """
        system = platform.system()
        if system == "Windows":
            return "shutdown /s /t 1"
        elif system == "Linux":
            return "shutdown -h now"
        elif system == "Darwin":
            return "sudo shutdown -h now"
        return None

    def _is_middle_finger_only_up(self, landmarks):
        """
        Determines if only the middle finger is raised while the others are down.

        Args:
            landmarks (list): List of landmark points representing the hand.

        Returns:
            bool: True if only the middle finger is up, False otherwise.
        """
        tips = [4, 8, 12, 16, 20]

        def is_up(i): return landmarks[tips[i]].y < landmarks[tips[i] - 2].y

        return (
            not is_up(1) and  # Index
            is_up(2) and      # Middle
            not is_up(3) and  # Ring
            not is_up(4)      # Pinky
        )

    def _handle_middle_finger_detected(self):
        """
        Handles the event when the middle finger is detected.

        If in test mode, it logs a message. In live mode, it shuts down the system.
        """
        if self.test_mode:
            print("[EVENT] Middle finger detected (test mode)")
        else:
            print("[EVENT] Middle finger detected — shutting down...")
            if self.shutdown_command:
                os.system(self.shutdown_command)
            else:
                print("[ERROR] Unsupported OS — cannot shutdown")

    def run(self):
        """
        Starts the video stream and processes each frame to detect the middle finger gesture.

        The method continuously captures frames from the webcam, processes them to detect hands,
        and checks if the middle finger gesture is detected. If detected, the appropriate action is triggered.
        The video feed will display until the ESC key is pressed or a shutdown occurs.
        """
        print("[INFO] Video stream started (press ESC to exit)")

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print("[ERROR] Failed to read frame from camera")
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.drawer.draw_landmarks(
                        frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS
                    )

                    if self._is_middle_finger_only_up(hand_landmarks.landmark):
                        self._handle_middle_finger_detected()
                        if not self.test_mode:
                            self.cap.release()
                            cv2.destroyAllWindows()
                            return

            cv2.imshow("Gesture Detector", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                print("[INFO] ESC pressed — exiting")
                break

        self.cap.release()
        cv2.destroyAllWindows()
        print("[INFO] Detector stopped cleanly")

if __name__ == "__main__":
    """
    Main entry point of the script. Initializes the MiddleFingerDetector and runs it in test mode.
    To change to live mode, set test_mode=False.
    """
    detector = MiddleFingerDetector(test_mode=True)
    detector.run()
