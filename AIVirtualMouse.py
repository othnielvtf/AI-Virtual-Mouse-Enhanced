import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import os

# Suppress MediaPipe warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

wCam, hCam = 1280, 720
frameR = 10  # Reduced from 100 to increase tracking area
smoothening = 7

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
isDragging = False
fistCloseTime = 0
hasClicked = False

# Detect available cameras
def list_cameras():
    available_cameras = []
    print("Scanning for cameras (this may take a moment)...")
    for i in range(10):  # Check first 10 camera indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            # Give camera time to initialize (important for iPhone/external cameras)
            time.sleep(0.5)
            ret, frame = cap.read()
            if ret:
                available_cameras.append(i)
                print(f"  Found: Camera {i}")
            cap.release()
            time.sleep(0.3)  # Brief pause between cameras
    return available_cameras

# List available cameras
cameras = list_cameras()
if not cameras:
    print("Error: No cameras detected. Please check camera permissions in System Settings > Privacy & Security > Camera")
    exit()

print("\n=== Available Cameras ===")
for idx in cameras:
    print(f"Camera {idx}")
print("========================\n")

# Ask user to select camera
if len(cameras) == 1:
    selected_camera = cameras[0]
    print(f"Using Camera {selected_camera}")
else:
    while True:
        try:
            selected_camera = int(input(f"Select camera index (available: {cameras}): "))
            if selected_camera in cameras:
                break
            else:
                print(f"Invalid selection. Please choose from: {cameras}")
        except ValueError:
            print("Please enter a valid number")

print(f"\nStarting AI Virtual Mouse with Camera {selected_camera}...")
print("Controls:")
print("  - Open hand (3+ fingers) = Move cursor")
print("  - Close fist briefly = Click")
print("  - Hold fist closed (1+ sec) = Drag")
print("  - Press Ctrl+C to exit\n")

# Open camera with retry logic (important for iPhone cameras)
cap = None
max_retries = 3
for attempt in range(max_retries):
    if attempt > 0:
        print(f"Retrying camera connection (attempt {attempt + 1}/{max_retries})...")
        time.sleep(2)  # Wait longer between retries
    
    cap = cv2.VideoCapture(selected_camera)
    if cap.isOpened():
        time.sleep(1)  # Give camera time to fully initialize
        ret, test_frame = cap.read()
        if ret and test_frame is not None:
            print("Camera connected successfully!")
            break
        else:
            cap.release()
            if attempt < max_retries - 1:
                print("Camera opened but not ready yet...")
    else:
        if attempt < max_retries - 1:
            print("Could not open camera...")

if not cap or not cap.isOpened():
    print("Error: Could not open selected camera after multiple attempts.")
    print("If using iPhone, make sure Continuity Camera is enabled and try again.")
    exit()

cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

while True:
    success, img = cap.read()
    if not success or img is None:
        print("Error: Failed to read from camera")
        break
    
    # Flip the image horizontally for mirror effect
    img = cv2.flip(img, 1)
    
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    
    if len(lmList) != 0:
        # Get palm center (wrist landmark 0 and middle finger base landmark 9)
        x_palm = (lmList[0][1] + lmList[9][1]) // 2
        y_palm = (lmList[0][2] + lmList[9][2]) // 2
        
        # Get thumb and index finger tips for clicking
        x_index, y_index = lmList[8][1:]  # Index finger tip
        x_thumb, y_thumb = lmList[4][1:]  # Thumb tip
        
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(255, 0, 255), 2)
        
        # Moving Mode - Track palm movement (hand open, all fingers up or at least 3 fingers)
        if fingers.count(1) >= 3:
            # If we were dragging, release the mouse button
            if isDragging:
                autopy.mouse.toggle(down=False)
                isDragging = False
            
            # Reset fist timer when hand opens
            fistCloseTime = 0
            hasClicked = False
            
            x3 = np.interp(x_palm, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y_palm, (frameR, hCam-frameR), (0, hScr))
            clocX = plocX + (x3-plocX) / smoothening
            clocY = plocY + (y3-plocY) / smoothening
            autopy.mouse.move(clocX, clocY)
            cv2.circle(img, (x_palm, y_palm), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # Click/Drag Mode - Close fist (all fingers down)
        elif fingers.count(1) == 0:
            currentTime = time.time()
            
            # First time closing fist - record the time
            if fistCloseTime == 0:
                fistCloseTime = currentTime
            
            # Calculate how long fist has been closed
            fistDuration = currentTime - fistCloseTime
            
            # If less than 1 second and haven't clicked yet - perform single click
            if fistDuration < 1.0 and not hasClicked:
                autopy.mouse.click()
                hasClicked = True
                cv2.circle(img, (x_palm, y_palm), 15, (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "CLICK", (x_palm - 30, y_palm - 30), 
                           cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            
            # If more than 1 second - enter drag mode
            elif fistDuration >= 1.0:
                x3 = np.interp(x_palm, (frameR, wCam-frameR), (0, wScr))
                y3 = np.interp(y_palm, (frameR, hCam-frameR), (0, hScr))
                clocX = plocX + (x3-plocX) / smoothening
                clocY = plocY + (y3-plocY) / smoothening
                
                # Start dragging if not already
                if not isDragging:
                    autopy.mouse.toggle(down=True)
                    isDragging = True
                
                autopy.mouse.move(clocX, clocY)
                cv2.circle(img, (x_palm, y_palm), 15, (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "DRAG", (x_palm - 30, y_palm - 30), 
                           cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                plocX, plocY = clocX, clocY
            else:
                # Just show the closed fist indicator
                cv2.circle(img, (x_palm, y_palm), 15, (0, 255, 0), cv2.FILLED)
                
    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow('Image', img)
    cv2.waitKey(1)