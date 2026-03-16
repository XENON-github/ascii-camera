# ascii-camera

A Python application that captures live frames from your webcam, converts them into ASCII art, and displays them in the terminal in real-time.

## File Structure
```text
ascii_cam/
├── __init__.py
├── main.py
├── camera.py
├── ascii_converter.py
└── config.py
run.py
start.sh
```

## Requirements
- Python 3.10+

## Installation and Execution

### 1. Clone the repo:
```git clone https://github.com/XENON-github/ascii-camera```

### 2. Run the application:

```cd ascii-camera```

The `start.sh` (Linux/macOS) or `start.bat` (Windows) script will automatically create a virtual environment and install dependencies.

**Linux/macOS:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```cmd
start.bat
```

### 3. Command Line Arguments:
```bash
./start.sh --help
```

### Controls
- **Ctrl+C**: Exit the program gracefully.

## Configuration
Modify `ascii_cam/config.py` to change settings:
- `ASCII_CHARS`: The character ramp.
- `FRAME_WIDTH`: Desired width of the ASCII output.
- `TARGET_FPS`: Targeted frames per second.
- `ASPECT_RATIO_CORRECTION`: Vertical correction factor.
- `ENABLE_EDGES`: Toggle Canny edge detection.
- `INVERT_EDGES`: Choose whether edges are drawn with dense or light characters.
