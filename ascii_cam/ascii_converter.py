import cv2
import numpy as np
from typing import List, Optional, Tuple
from .config import (
    ASCII_CHARS, 
    ASPECT_RATIO_CORRECTION, 
    USE_CLAHE, 
    USE_SHARPENING, 
    ENABLE_EDGES,
    EDGE_STRENGTH,
    CANNY_LOW,
    CANNY_HIGH,
    INVERT_EDGES,
    BRIGHTNESS,
    CONTRAST
)

def frame_to_ascii(frame: np.ndarray, width: int, use_color: bool = True) -> str:
    if frame is None:
        return ""

    original_height, original_width = frame.shape[:2]
    height = int(original_height / original_width * width * ASPECT_RATIO_CORRECTION)
    
    resized_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_LANCZOS4)

    gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

    if USE_CLAHE:
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        processed = clahe.apply(gray_frame)
    else:
        processed = gray_frame

    if USE_SHARPENING:
        kernel = np.array([[ 0, -1,  0],
                           [-1,  5, -1],
                           [ 0, -1,  0]])
        processed = cv2.filter2D(processed, -1, kernel)

    processed = cv2.convertScaleAbs(processed, alpha=CONTRAST, beta=int(128 * (BRIGHTNESS - 1)))

    if ENABLE_EDGES:
        edges = cv2.Canny(processed, CANNY_LOW, CANNY_HIGH)
        edges = cv2.dilate(edges, np.ones((2, 2), np.uint8), iterations=1)
        
        edge_overlay = np.clip(edges.astype(float) * EDGE_STRENGTH, 0, 255).astype(np.uint8)
        
        if INVERT_EDGES:
            processed = cv2.subtract(processed, edge_overlay)
        else:
            processed = cv2.add(processed, edge_overlay)

    num_chars = len(ASCII_CHARS)
    ascii_indices = (processed.astype(int) * num_chars) // 256
    ascii_indices = np.clip(ascii_indices, 0, num_chars - 1)
    
    ascii_chars_list = list(ASCII_CHARS)
    
    if not use_color:
        ascii_chars_array = np.array(ascii_chars_list)
        ascii_frame_array = ascii_chars_array[ascii_indices]
        ascii_rows = ["".join(row) for row in ascii_frame_array]
        return "\n".join(ascii_rows)
    else:
        rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        
        output = []
        last_r, last_g, last_b = -1, -1, -1
        
        for y in range(height):
            line = []
            for x in range(width):
                idx = ascii_indices[y, x]
                char = ascii_chars_list[idx]
                r, g, b = rgb_frame[y, x]
                
                if r != last_r or g != last_g or b != last_b:
                    line.append(f"\033[38;2;{r};{g};{b}m{char}")
                    last_r, last_g, last_b = r, g, b
                else:
                    line.append(char)
            
            output.append("".join(line))
        
        return "\n".join(output) + "\033[0m"
