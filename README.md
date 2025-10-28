# AI Virtual Mouse 🖱️

> **Forked from**: [gokulnpc/AI-Virtual-Mouse](https://github.com/gokulnpc/AI-Virtual-Mouse)

Control your mouse cursor using hand gestures detected by your webcam! This project uses computer vision and hand tracking to create a touchless mouse control system.

![Demo](image.png)

## Features

- **Cursor Movement**: Move your cursor by pointing with your index finger
- **Click Action**: Perform mouse clicks by pinching your index and middle fingers together
- **Real-time Tracking**: Smooth cursor movement with adjustable sensitivity
- **Visual Feedback**: See hand landmarks and tracking zones in real-time

## How It Works

The application uses:
- **OpenCV** - Camera capture and image processing
- **MediaPipe** - Hand tracking and landmark detection
- **AutoPy** - System mouse control
- **NumPy** - Coordinate calculations and interpolation

## Installation

### Prerequisites

- Python 3.7 or higher
- Webcam
- macOS, Windows, or Linux

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/othnielvtf/AI-Virtual-Mouse-Enhanced.git
   cd AI-Virtual-Mouse-Enhanced
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Grant camera permissions** (macOS)
   - Go to **System Settings** → **Privacy & Security** → **Camera**
   - Enable access for **Terminal** or your Python IDE

## Usage

Run the application:
```bash
python AIVirtualMouse.py
```

### Hand Gestures

| Gesture | Action | Description |
|---------|--------|-------------|
| ![Index finger up](https://img.shields.io/badge/☝️-Index_Finger-blue) | **Move Cursor** | Raise only your index finger to control cursor movement |
| ![Pinch gesture](https://img.shields.io/badge/🤏-Pinch-green) | **Click** | Raise index and middle fingers, then bring fingertips close together |

### Controls

- **Purple Rectangle**: Active tracking zone - keep your hand within this area
- **Purple Circle**: Appears on index finger when moving cursor
- **Green Circle**: Indicates a click has been triggered
- **FPS Counter**: Shows performance in top-left corner

### Exit

Press `Ctrl+C` in the terminal to stop the application.

## Configuration

You can adjust these parameters in `AIVirtualMouse.py`:

```python
wCam, hCam = 640, 480    # Camera resolution
frameR = 100              # Frame reduction (border size)
smoothening = 7           # Cursor smoothing (higher = smoother but slower)
```

## Troubleshooting

### Camera Not Found
If you see "camera failed to properly initialize":
- The default camera index is `0`. If you have multiple cameras, try changing line 19:
  ```python
  cap = cv2.VideoCapture(1)  # Try 1, 2, etc.
  ```

### Permission Denied (macOS)
- Ensure Terminal/IDE has camera access in System Settings
- Restart Terminal after granting permissions

### Verbose Logging
The application suppresses most MediaPipe warnings. If you still see too many messages, they're harmless diagnostic information.

## Project Structure

```
AI-Virtual-Mouse/
├── AIVirtualMouse.py          # Main application
├── HandTrackingModule.py      # Hand detection module
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation
└── image.png                  # Demo image
```

## How Hand Tracking Works

1. **Hand Detection**: MediaPipe detects hand landmarks (21 points per hand)
2. **Finger Recognition**: Determines which fingers are raised
3. **Gesture Mapping**: 
   - Index finger tip (landmark 8) → Cursor position
   - Distance between index and middle fingertips → Click trigger
4. **Smoothing**: Applies exponential smoothing for stable cursor movement
5. **Screen Mapping**: Converts camera coordinates to screen coordinates

## Credits

Built with:
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://mediapipe.dev/)
- [AutoPy](https://github.com/autopilot-rs/autopy)

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

---

**Note**: This is an experimental project. Performance may vary based on lighting conditions and camera quality.