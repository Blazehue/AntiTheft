# Quick Start Guide
## Anti-Theft Alarm System

### 🎯 5-Minute Setup

Follow these steps to get the system running quickly.

---

## Step 1: Install Python Dependencies

```powershell
# Navigate to project directory
cd C:\Users\pandr\OneDrive\Desktop\GithubStreaks\Day16

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: If `face_recognition` installation fails (requires CMake and dlib), the system will work with basic OpenCV detection.

---

## Step 2: Create Storage Directories

The system will create these automatically, but you can create them manually:

```powershell
mkdir storage
mkdir storage\intruders
mkdir storage\logs
mkdir storage\authorized_faces
```

---

## Step 3: Add Authorized Faces (Optional)

To enable face recognition for authorized persons:

1. Take clear photos of authorized persons
2. Save them as: `storage\authorized_faces\person_name.jpg`
3. Use clear, well-lit, front-facing photos

Example:
```
storage\authorized_faces\john_doe.jpg
storage\authorized_faces\jane_smith.jpg
```

---

## Step 4: Configure System

Edit `config.json` if needed:

```json
{
  "camera": {
    "device_id": 0,  // Change if camera not found (try 1, 2)
    "resolution": [640, 480],
    "fps": 30
  },
  "motion_detection": {
    "threshold": 25,  // Lower = more sensitive
    "min_contour_area": 500
  }
}
```

---

## Step 5: Run the System

```powershell
python main.py
```

### Expected Output:

```
======================================================================
ANTI-THEFT ALARM SYSTEM
Computer Vision + Computer Organization & Architecture
======================================================================
✅ Configuration loaded from: config.json

🔧 Initializing components...
   📝 Memory Management...
   🎯 Motion Detection...
   👤 Face Recognition...
   ⚙️  State Machine...
   🚨 Alarm System...
   💾 Storage System...
   📊 Performance Monitor...
   📹 Video Capture...

✅ System initialized successfully!

🚀 Starting Anti-Theft Alarm System...

▶️  System running. Press 'q' to quit, 's' to toggle arm/disarm
   System Armed: True
```

---

## Step 6: Test the System

### Test Motion Detection
1. Move in front of the camera
2. Watch the video feed - motion areas highlighted in green
3. System state should change: MONITORING → ALERT → ALARM

### Test Face Recognition
1. Add your photo to `authorized_faces/` folder
2. Restart system
3. Your face should be recognized (green box)
4. Unknown faces trigger alarm (red box)

### Test Alarm System
1. Press **'s'** to ARM the system
2. Move in front of camera
3. After 2 seconds in ALERT, alarm triggers
4. Image saved to `storage/intruders/`

---

## Keyboard Controls

| Key | Action |
|-----|--------|
| **q** | Quit application |
| **s** | Toggle ARM/DISARM |
| **ESC** | Quit application |

---

## Understanding the Display

```
┌─────────────────────────────────────────┐
│ State: MONITORING              FPS: 28  │ ← System status
│ Status: ARMED                            │
│                                          │
│                                          │
│         [VIDEO FEED]                     │
│                                          │
│ Motion detected areas: Green boxes       │ ← Detection
│ Face detected: Green/Red boxes           │
│                                          │
└─────────────────────────────────────────┘
```

**Colors**:
- **Green**: Motion areas, authorized faces
- **Red**: Unknown faces (intruders)

**States**:
- **IDLE**: System off
- **MONITORING**: Active, no threats (green)
- **ALERT**: Evaluating threat (orange)
- **ALARM**: Threat confirmed (red)
- **COOLDOWN**: Recovery period

---

## Viewing Results

### Captured Intruder Images
```powershell
dir storage\intruders\
```

### System Logs
```powershell
Get-Content storage\logs\system_*.log
```

### Performance Reports
```powershell
Get-Content storage\logs\performance_report_*.json | ConvertFrom-Json
```

---

## Troubleshooting

### Problem: Camera Not Found
```
Solution: Change device_id in config.json
Try: 0, 1, or 2
```

### Problem: Low FPS (< 10)
```
Solutions:
1. Reduce resolution: [320, 240]
2. Disable face recognition
3. Close other applications
```

### Problem: Too Many False Alarms
```
Solutions:
1. Increase threshold: 30-40
2. Increase min_contour_area: 1000
3. Improve lighting
```

### Problem: Missing Dependencies
```powershell
# Reinstall specific packages
pip install opencv-python numpy psutil

# If face_recognition fails, skip it
# System will use OpenCV Haar Cascade instead
```

---

## Performance Tips

### For Best Performance:
- ✅ Use webcam (not virtual camera)
- ✅ Good lighting conditions
- ✅ Close unnecessary applications
- ✅ Use SSD for storage (faster writes)

### For Lower CPU Usage:
- Set `detection_interval: 10` (check every 10th frame)
- Disable face recognition
- Reduce resolution to 320x240

---

## Email Notifications Setup (Optional)

Edit `config.json`:

```json
{
  "notification": {
    "email_enabled": true,
    "email_settings": {
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "sender_email": "your_email@gmail.com",
      "sender_password": "your_app_password",
      "recipient_email": "alert_recipient@gmail.com"
    }
  }
}
```

**Gmail Users**: Use [App Password](https://support.google.com/accounts/answer/185833)

---

## Next Steps

### Learn the COA Concepts
Read `DOCS/COA_MAPPING.md` to understand how each component demonstrates Computer Organization & Architecture principles.

### Customize the System
- Adjust detection sensitivity
- Add more authorized faces
- Configure email notifications
- Tune performance settings

### View Performance Metrics
After running, check:
- FPS and latency
- CPU and memory usage
- Cache hit rates
- I/O throughput

---

## Need Help?

1. Check README.md for detailed information
2. Review COA_MAPPING.md for concept explanations
3. Check logs in `storage/logs/` for errors

---

**You're all set! 🎉**

The system is now monitoring for intruders using Computer Vision and demonstrating 15+ Computer Organization & Architecture concepts in action!
