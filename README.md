# AI Virtual Mouse 🖱️

> **Forked from**: [gokulnpc/AI-Virtual-Mouse](https://github.com/gokulnpc/AI-Virtual-Mouse)
Control your mouse cursor using hand gestures detected by your webcam! This project uses computer vision and hand tracking to create a touchless mouse control system with palm-based tracking and intuitive gestures.

![Demo](image.png)

## Features

- **Palm-Based Cursor Control**: Move your cursor by tracking your entire palm movement (more stable than single finger)
- **Smart Click & Drag**: Quick fist close for single click, hold fist for 1+ second to drag
- **Multi-Camera Support**: Automatically detects and lets you choose between multiple cameras (including iPhone via Continuity Camera)
- **Mirrored Display**: Natural mirror-like control for intuitive hand movements
- **Expanded Tracking Area**: Minimal border (10px) for maximum control space
- **HD Support**: Works with 720p and higher resolution cameras
- **Real-time Visual Feedback**: See hand landmarks, tracking zones, and action indicators

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
   cd AI-Virtual-Mouse
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Grant camera permissions** (macOS)
   - Go to **System Settings** → **Privacy & Security** → **Camera**
   - Enable access for **Terminal** or your Python IDE

## Usage

1. **Run the application:**
   ```bash
   python AIVirtualMouse.py
   ```

2. **Select your camera:**
   - The program will scan for available cameras
   - If multiple cameras are detected, you'll be prompted to choose one
   - For iPhone users: Select the higher camera index (usually Camera 1)

3. **Wait for initialization:**
   - The camera will initialize (may take a few seconds for iPhone)
   - You'll see "Camera connected successfully!" when ready

### Hand Gestures

| Gesture | Action | Description |
|---------|--------|-------------|
| ![Open hand](https://img.shields.io/badge/✋-Open_Hand-blue) | **Move Cursor** | Open your hand (3+ fingers up) - cursor follows your palm center |
| ![Closed fist](https://img.shields.io/badge/✊-Quick_Fist-green) | **Click** | Close your fist briefly (< 1 second) for a single click |
| ![Hold fist](https://img.shields.io/badge/✊-Hold_Fist-orange) | **Click & Drag** | Close and hold your fist (1+ seconds), then move to drag. Open hand to release |

### Visual Feedback

- **Purple Rectangle**: Active tracking zone (nearly full screen with 10px border)
- **Purple Circle**: Appears on palm center when moving cursor
- **Green Circle + "CLICK"**: Single click triggered
- **Green Circle + "DRAG"**: Drag mode active
- **FPS Counter**: Shows performance in top-left corner

### Exit

Press `Ctrl+C` in the terminal to stop the application.

## Configuration

You can adjust these parameters in `AIVirtualMouse.py`:

```python
wCam, hCam = 1280, 720   # Camera resolution (720p recommended, supports up to 1080p)
frameR = 10               # Frame reduction (border size in pixels)
smoothening = 7           # Cursor smoothing (higher = smoother but slower response)
```

## Using iPhone as Webcam (Continuity Camera)

### Setup
1. **Requirements:**
   - iPhone running iOS 16 or later
   - Mac running macOS Ventura or later
   - Both devices signed into the same Apple ID
   - WiFi and Bluetooth enabled on both devices

2. **Connect:**
   - Keep your iPhone near your Mac
   - Run the program - your iPhone should appear as Camera 1 or higher
   - Select the iPhone camera when prompted
   - Wait for the camera to initialize (takes a few seconds)

3. **Tips:**
   - The program includes retry logic to handle iPhone camera activation
   - If the iPhone camera doesn't appear, run the program again to "wake up" Continuity Camera
   - Keep devices within Bluetooth range for best performance

## Troubleshooting

### Camera Not Detected
- **Check permissions**: System Settings → Privacy & Security → Camera
- **Restart Terminal** after granting permissions
- **For iPhone**: Ensure Continuity Camera is enabled and devices are nearby

### Camera Connection Issues
- The program automatically retries up to 3 times with delays
- For iPhone cameras, the first connection may take longer
- If it fails, try running the program again

### Performance Issues
- **Lower resolution**: Change `wCam, hCam` to `640, 480` for faster processing
- **Increase smoothening**: Higher values = smoother but slower cursor
- **Better lighting**: Improves hand detection accuracy

### Verbose Logging
The application suppresses most MediaPipe warnings. The remaining messages are harmless diagnostic information from the underlying libraries.

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

1. **Camera Setup**: 
   - Scans for available cameras with initialization delays for external cameras
   - Mirrors the video feed horizontally for natural control
   - Supports multiple resolutions (640x480 to 1920x1080)

2. **Hand Detection**: 
   - MediaPipe detects hand landmarks (21 points per hand)
   - Tracks single hand for optimal performance

3. **Palm Center Calculation**:
   - Calculates palm center using wrist (landmark 0) and middle finger base (landmark 9)
   - More stable than single fingertip tracking

4. **Gesture Recognition**: 
   - **Open hand** (3+ fingers up) → Move mode
   - **Closed fist** (0 fingers up) → Click/Drag mode
   - Timer-based differentiation: < 1 sec = click, ≥ 1 sec = drag

5. **Cursor Control**:
   - Exponential smoothing for stable movement
   - Screen coordinate mapping with minimal border
   - Drag mode uses `autopy.mouse.toggle()` for click-and-hold

6. **Visual Feedback**:
   - Real-time display of hand landmarks
   - Action indicators (CLICK/DRAG text)
   - FPS counter for performance monitoring

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

## Changelog

### Version 2.0 - Enhanced Edition

**Major Improvements:**
- ✅ **Palm-based tracking** - Switched from index finger to palm center for more stable cursor control
- ✅ **Smart click & drag** - Timer-based gesture: quick fist close = click, hold fist = drag
- ✅ **Multi-camera support** - Automatic camera detection with selection menu
- ✅ **iPhone camera support** - Full Continuity Camera integration with retry logic
- ✅ **Mirrored display** - Horizontal flip for natural, mirror-like control
- ✅ **Expanded tracking area** - Reduced border from 100px to 10px for maximum control space
- ✅ **HD support** - Increased default resolution from 480p to 720p
- ✅ **Better error handling** - Camera initialization with retries and clear error messages
- ✅ **Enhanced visual feedback** - Added "CLICK" and "DRAG" text indicators
- ✅ **Suppressed warnings** - Cleaner console output with MediaPipe warning suppression

**Technical Changes:**
- Changed gesture detection from finger-based to palm-based tracking
- Implemented timer system for click vs drag differentiation
- Added camera scanning with initialization delays
- Improved camera connection with 3-attempt retry logic
- Added horizontal video flip for mirror effect
- Updated hand landmark calculations for palm center

---

**Note**: Readme generated by AI