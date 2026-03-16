import cv2
import sys
import os
from typing import Optional, Any, Union
from .config import CAMERA_INDEX

class Camera:
    def __init__(self, source: Union[int, str] = CAMERA_INDEX):
        self.cap = self._try_open(source)
        if not self.cap or not self.cap.isOpened():
            found = False
            # Only try other indices if we were trying an index
            if isinstance(source, int):
                for i in range(10):
                    if i == source: continue
                    cap = self._try_open(i)
                    if cap and cap.isOpened():
                        self.cap = cap
                        found = True
                        break
            
            if not found:
                print(f"Error: Could not open camera or video source: {source}")
                print("\nTroubleshooting:")
                print("1. Ensure your camera is plugged in.")
                print("2. Check if another process is using the camera (e.g., run 'fuser /dev/video*')")
                print("3. Check if your user has permission to access /dev/video*")
                print(f"   Current user groups: {os.popen('groups').read().strip()}")
                print("   Try running: sudo usermod -aG video $USER (then logout and back in)")
                sys.exit(1)

    def _try_open(self, source: Union[int, str]) -> Optional[cv2.VideoCapture]:
        # Try different backends
        # For video files (strings), CAP_ANY is usually best
        # For camera indices, CAP_V4L2 is often more reliable on Linux
        backends = [cv2.CAP_ANY]
        if isinstance(source, int):
            backends.insert(0, cv2.CAP_V4L2)

        for backend in backends:
            try:
                cap = cv2.VideoCapture(source, backend)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        return cap
                    cap.release()
            except Exception:
                continue
        return None

    def get_frame(self) -> Optional[Any]:
        if not self.cap or not self.cap.isOpened():
            return None
        ret, frame = self.cap.read()
        if not ret or frame is None:
            return None
        return cv2.flip(frame, 1)

    def release(self) -> None:
        if self.cap and self.cap.isOpened():
            self.cap.release()

    def __del__(self):
        self.release()
