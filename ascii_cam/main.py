import time
import sys
import os
import signal
import argparse
from typing import NoReturn
from .camera import Camera
from .ascii_converter import frame_to_ascii
from .config import FRAME_WIDTH, TARGET_FPS

def hide_cursor() -> None:
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor() -> None:
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def signal_handler(sig, frame) -> NoReturn:
    print("\nExiting ASCII Camera...")
    show_cursor()
    sys.exit(0)

def main() -> None:
    parser = argparse.ArgumentParser(description="ASCII Camera - Real-time camera to ASCII art converter")
    parser.add_argument("--width", type=int, default=FRAME_WIDTH, help=f"Width of the ASCII art (default: {FRAME_WIDTH})")
    parser.add_argument("--fps", type=int, default=TARGET_FPS, help=f"Target FPS (default: {TARGET_FPS})")
    parser.add_argument("--no-color", action="store_true", help="Disable color output (grayscale mode)")
    parser.add_argument("--index", type=int, default=None, help="Camera index (overrides config)")
    parser.add_argument("--video", type=str, default=None, help="Path to a video file to use instead of the camera")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)

    if args.video is not None:
        cam = Camera(source=args.video)
    elif args.index is not None:
        cam = Camera(source=args.index)
    else:
        cam = Camera()
    
    frame_delay = 1.0 / args.fps

    print("Starting ASCII Camera... Press Ctrl+C to exit.")
    time.sleep(1)
    
    sys.stdout.write("\033[2J\033[H")
    hide_cursor()

    try:
        while True:
            start_time = time.time()
            
            frame = cam.get_frame()
            if frame is None:
                time.sleep(0.1)
                continue

            ascii_frame = frame_to_ascii(frame, args.width, use_color=not args.no_color)

            sys.stdout.write("\033[H")
            sys.stdout.write(ascii_frame)
            sys.stdout.flush()

            elapsed_time = time.time() - start_time
            sleep_time = max(0, frame_delay - elapsed_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        pass
    finally:
        cam.release()
        show_cursor()
        print("\nCamera released. Goodbye!")

if __name__ == "__main__":
    main()
