# Anti-Theft Alarm System
**Integrating Computer Vision with Computer Organization & Architecture**
(still work in progress)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Project Overview

An intelligent anti-theft alarm system that demonstrates Computer Organization & Architecture (COA) concepts through practical computer vision implementation. This project bridges theoretical COA principles with real-world application development, serving as both a functional security system and an educational platform for understanding low-level computing concepts.

### Core Capabilities

**Real-time Motion Detection** - Advanced frame differencing with contour analysis and adaptive thresholding  
**Face Recognition** - Authorized vs unauthorized person identification with confidence scoring  
**Intelligent State Machine** - IDLE, MONITORING, ALERT, ALARM, and COOLDOWN states with validated transitions  
**Multi-threaded Architecture** - Parallel processing demonstration with thread synchronization  
**Memory Management** - Circular buffers and LRU cache implementation simulating hardware memory hierarchy  
**Performance Monitoring** - Comprehensive FPS, CPU, and memory metrics with real-time visualization  
**I/O & Storage Systems** - File system operations, logging, and persistent storage management  
**Alert Notifications** - Configurable email/SMS notifications with captured intruder images  

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     VIDEO CAPTURE THREAD                     │
│                   (I/O Device - Webcam)                      │
│                 Hardware Polling Interface                   │
└───────────────────────┬─────────────────────────────────────┘
                        │ Frame Buffer (Circular Queue)
                        │ FIFO Memory Structure
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   PROCESSING PIPELINE                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  FETCH   │→ │  DECODE  │→ │ EXECUTE  │→ │WRITEBACK │   │
│  │ (Input)  │  │(Analysis)│  │(Process) │  │ (Output) │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                               │
│  Motion Detection (ALU)  ←→  Face Recognition (Cache)       │
│  Arithmetic Operations       LRU Replacement Policy          │
└───────────────────────┬─────────────────────────────────────┘
                        │ Shared Memory Region
                        │ Thread Synchronization
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    ALERT THREAD                              │
│   State Machine  →  Alarm System  →  Notifications         │
│   FSM Controller     I/O Operations    Network Interface     │
└─────────────────────────────────────────────────────────────┘
```

---

## COA Concepts Demonstrated

### 1. Memory Management

**Circular Frame Buffer**: Implements a FIFO queue structure for video frames, simulating L1 cache behavior with fixed capacity and automatic overwrite of oldest entries. Demonstrates hardware-level buffer management and cache line replacement.

**LRU Cache**: Implements Least Recently Used replacement policy for face recognition database, tracking access patterns and automatically evicting least-used entries when capacity is reached. Includes cache hit rate monitoring and performance metrics.

**Memory Hierarchy**: Simulates the complete memory hierarchy from RAM (active frame buffer) to cache (face recognition database) to disk storage (persistent logging). Demonstrates latency differences and access patterns across levels.

**Performance Metrics**: Tracks cache hit rate, memory utilization, page faults, and memory access patterns to demonstrate real-world memory management challenges.

**Implementation**: `src/memory_management.py`

### 2. CPU Architecture

**Pipeline Stages**: Implements a four-stage instruction pipeline (Fetch, Decode, Execute, Write-back) where each video frame passes through sequential processing stages. Demonstrates instruction-level parallelism and pipeline hazards.

**Multi-threading**: Employs separate threads for capture, processing, and alerting, demonstrating parallel execution, context switching, and CPU core utilization. Includes thread pool management and load balancing.

**Thread Synchronization**: Implements locks, semaphores, and shared memory regions with mutex protection to prevent race conditions and ensure data consistency across concurrent operations.

**Performance Metrics**: Calculates throughput (FPS), latency per frame, and CPI (cycles per instruction) equivalent to demonstrate CPU efficiency and bottleneck identification.

**Implementation**: `src/cpu_architecture.py`

### 3. Arithmetic & Logic Operations

**ALU Operations**: Performs pixel-level arithmetic including subtraction (frame differencing), addition (frame averaging), multiplication (intensity scaling), and division operations for motion detection algorithms.

**Boolean Logic**: Implements AND, OR, NOT, XOR gate operations for alarm condition evaluation, threshold comparisons, and binary decision making in detection logic.

**Bitwise Operations**: Utilizes bitwise AND for image masking, XOR for change detection, and shift operations for efficient memory access and pixel manipulation.

**Threshold Comparators**: Implements hardware-style comparators for motion detection thresholds, contour area evaluation, and confidence scoring in face recognition.

**Implementation**: `src/motion_detection.py`

### 4. I/O Systems

**Input Devices**: Webcam interface using polling-based I/O with configurable frame rates, resolution settings, and device enumeration. Demonstrates interrupt-driven vs. polling I/O models.

**Output Devices**: Display rendering, audio alarm system, and file system output demonstrating different I/O device classes and their characteristics.

**File System**: Implements disk read/write operations with buffering, caching, and error handling. Includes directory management, file metadata tracking, and storage optimization.

**Network I/O**: Asynchronous email notification system demonstrating network stack operations, protocol handling, and non-blocking I/O patterns.

**Implementation**: `src/io_storage.py`

### 5. State Machines

**Finite State Machine**: Implements a complete FSM with five states (IDLE, MONITORING, ALERT, ALARM, COOLDOWN) representing system operational modes. Each state has defined entry/exit conditions and valid transitions.

**State Transitions**: Validates all state changes based on detection events, timer expiration, and user input. Prevents invalid state transitions and maintains system consistency.

**Control Flow**: Event-driven state management where external stimuli (motion detection, face recognition results) trigger state evaluations and transitions through deterministic logic.

**Timing Control**: Implements state-specific timing requirements including alert evaluation periods, alarm durations, and cooldown intervals to prevent false triggers.

**Implementation**: `src/state_machine.py`

### 6. Performance Monitoring

**FPS Counter**: Tracks frames per second as a measure of system throughput, identifying processing bottlenecks and measuring the impact of optimization efforts.

**CPU Utilization**: Monitors per-thread and system-wide CPU usage to demonstrate resource allocation, thread efficiency, and multi-core utilization patterns.

**Memory Profiling**: Tracks RSS (Resident Set Size), VMS (Virtual Memory Size), and peak usage to demonstrate memory consumption patterns and identify memory leaks.

**Execution Profiling**: Measures execution time for each pipeline stage, detection algorithm, and I/O operation to identify performance bottlenecks and optimization opportunities.

**Implementation**: `src/performance_monitor.py`

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Webcam or video file for testing
- Windows, Linux, or macOS operating system
- 2GB RAM minimum (4GB recommended)
- Multi-core processor recommended for optimal performance

### Step 1: Clone Repository

```powershell
git clone <repository-url>
cd Anti-Theft-Alarm-System
```

### Step 2: Create Virtual Environment

**Windows (PowerShell)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/macOS**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

**System Dependencies**:

**Ubuntu/Debian**:
```bash
sudo apt-get install python3-opencv libsm6 libxext6 libxrender-dev
sudo apt-get install cmake libboost-all-dev
```

**macOS**:
```bash
brew install cmake boost
```

**Windows**: Most dependencies install via pip. For face_recognition, install Visual C++ Build Tools if needed.

---

## Configuration

Edit `config.json` to customize system behavior:

```json
{
  "camera": {
    "device_id": 0,
    "resolution": [640, 480],
    "fps": 30,
    "auto_exposure": true
  },
  "motion_detection": {
    "threshold": 25,
    "min_contour_area": 500,
    "gaussian_blur_kernel": 21,
    "detection_interval": 1
  },
  "face_recognition": {
    "enabled": true,
    "detection_interval": 5,
    "confidence_threshold": 0.6,
    "model": "hog"
  },
  "alarm": {
    "enabled": true,
    "duration": 5,
    "cooldown_period": 10,
    "sound_file": "alarm.wav"
  },
  "memory": {
    "frame_buffer_size": 30,
    "cache_size": 100,
    "max_log_files": 50
  },
  "performance": {
    "enable_monitoring": true,
    "report_interval": 60,
    "target_fps": 30
  },
  "notifications": {
    "email_enabled": false,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "",
    "sender_password": "",
    "recipient_email": ""
  }
}
```

### Configuration Parameters

**Camera Settings**:
- `device_id`: Camera index (0 for default, try 1, 2 for multiple cameras)
- `resolution`: [width, height] in pixels (lower values improve performance)
- `fps`: Target frame rate (higher values increase CPU usage)
- `auto_exposure`: Enable automatic exposure adjustment

**Motion Detection**:
- `threshold`: Pixel difference threshold (lower = more sensitive, range: 10-50)
- `min_contour_area`: Minimum motion area in pixels (filters small movements)
- `gaussian_blur_kernel`: Blur size for noise reduction (odd number, 15-25)
- `detection_interval`: Frames between detection checks (1 = every frame)

**Face Recognition**:
- `enabled`: Toggle face recognition feature
- `detection_interval`: Frames between face detection (higher = better performance)
- `confidence_threshold`: Match confidence (0.0-1.0, lower = more strict)
- `model`: Detection model ('hog' for CPU, 'cnn' for GPU)

**Alarm System**:
- `duration`: Alarm duration in seconds
- `cooldown_period`: Seconds before system can re-alarm
- `sound_file`: Path to alarm audio file

**Memory Management**:
- `frame_buffer_size`: Circular buffer capacity (affects memory usage)
- `cache_size`: Face recognition cache entries
- `max_log_files`: Maximum stored log files before rotation

**Performance**:
- `enable_monitoring`: Toggle performance metrics collection
- `report_interval`: Seconds between performance reports
- `target_fps`: Desired frame rate for optimization

---

## Usage

### Basic Usage

```powershell
python main.py
```

### Advanced Usage

**Test Mode** (using video file instead of webcam):
```powershell
python main.py --input video.mp4
```

**Headless Mode** (no display window):
```powershell
python main.py --headless
```

**Custom Configuration**:
```powershell
python main.py --config custom_config.json
```

**Debug Mode** (verbose logging):
```powershell
python main.py --debug
```

### Keyboard Controls

- **q** - Quit application gracefully
- **s** - Toggle ARM/DISARM status
- **p** - Pause/Resume monitoring
- **r** - Reset alarm state
- **d** - Toggle debug overlay
- **m** - Toggle motion detection visualization
- **f** - Toggle face detection overlay

### System States

**IDLE**: System inactive, no monitoring or detection. Camera may be disabled to conserve resources.

**MONITORING**: Active surveillance mode. Continuously captures frames, performs motion detection, and face recognition. Default operational state.

**ALERT**: Potential threat detected. System enters 2-second evaluation period to confirm detection before triggering alarm. Reduces false positives.

**ALARM**: Confirmed threat detected. Alarm activated, images captured, notifications sent. System logs intrusion event.

**COOLDOWN**: Post-alarm recovery period (default 10 seconds). Prevents alarm re-triggering on same event. System remains in monitoring mode but alarm is suppressed.

### System Workflow

```
IDLE → (ARM) → MONITORING
  ↑                ↓
  |          (Motion Detected)
  |                ↓
  |            ALERT (2s evaluation)
  |         ↓             ↓
  |    (Confirmed)    (False Alarm)
  |         ↓             ↓
  |      ALARM        MONITORING
  |         ↓
  |    COOLDOWN (10s)
  |         ↓
  └─── MONITORING
```

---

## Project Structure

```
Anti-Theft-Alarm-System/
├── src/
│   ├── __init__.py
│   ├── memory_management.py         # Circular buffers, LRU cache, memory hierarchy
│   ├── cpu_architecture.py          # Pipeline implementation, threading, CPU monitoring
│   ├── motion_detection.py          # ALU operations, boolean logic, detection algorithms
│   ├── face_recognition_module.py   # Cache-based face recognition and identification
│   ├── state_machine.py             # FSM implementation, alarm logic, notifications
│   ├── io_storage.py                # File system operations, logging, persistent storage
│   └── performance_monitor.py       # FPS tracking, resource monitoring, benchmarking
├── storage/
│   ├── intruders/                   # Captured intruder images with timestamps
│   ├── logs/                        # System logs, event logs, performance reports
│   └── authorized_faces/            # Authorized person images for recognition
├── tests/
│   ├── test_memory.py               # Memory management unit tests
│   ├── test_motion_detection.py     # Detection algorithm tests
│   ├── test_state_machine.py        # FSM validation tests
│   └── test_performance.py          # Performance benchmarking tests
├── scripts/
│   ├── benchmark.py                 # Performance benchmarking script
│   ├── train_faces.py               # Face database training utility
│   └── generate_report.py           # Performance report generator
├── docs/
│   ├── architecture.md              # Detailed architecture documentation
│   ├── coa_concepts.md              # COA concept explanations
│   └── api_reference.md             # API documentation
├── main.py                          # Main application entry point
├── config.json                      # System configuration file
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
├── LICENSE                          # MIT License
└── README.md                        # This file
```

---

## COA Concept Implementation Map

| COA Concept | Module | Class/Function | Lines | Description |
|-------------|--------|----------------|-------|-------------|
| **Circular Buffer** | `memory_management.py` | `CircularFrameBuffer` | 15-85 | FIFO queue with fixed capacity, automatic overwrite |
| **LRU Cache** | `memory_management.py` | `LRUCache` | 90-165 | Least Recently Used replacement policy implementation |
| **Memory Hierarchy** | `memory_management.py` | `MemoryHierarchy` | 170-245 | RAM/Cache/Disk simulation with latency modeling |
| **Pipeline Stages** | `cpu_architecture.py` | `Pipeline.execute_stage()` | 50-120 | Four-stage instruction pipeline |
| **Multi-threading** | `cpu_architecture.py` | `WorkerThread` | 125-195 | Thread pool with synchronization |
| **Thread Locks** | `cpu_architecture.py` | `ThreadSafeQueue` | 200-250 | Mutex and semaphore implementation |
| **ALU Operations** | `motion_detection.py` | `ArithmeticLogicUnit` | 30-105 | Pixel arithmetic operations |
| **Boolean Logic** | `motion_detection.py` | `BooleanLogic` | 110-175 | AND/OR/NOT/XOR gate operations |
| **Comparators** | `motion_detection.py` | `Comparator` | 180-220 | Threshold comparison logic |
| **FSM** | `state_machine.py` | `StateMachine` | 25-150 | Five-state finite state machine |
| **State Transitions** | `state_machine.py` | `validate_transition()` | 155-195 | State change validation |
| **File I/O** | `io_storage.py` | `FileSystem` | 20-120 | Buffered file operations |
| **Directory Mgmt** | `io_storage.py` | `DirectoryManager` | 125-180 | File system navigation |
| **Logging** | `io_storage.py` | `Logger` | 185-250 | Persistent event logging |
| **FPS Tracking** | `performance_monitor.py` | `FPSCounter` | 15-65 | Frame rate calculation |
| **CPU Monitoring** | `performance_monitor.py` | `CPUMonitor` | 70-125 | Thread and system CPU usage |
| **Memory Profiling** | `performance_monitor.py` | `MemoryProfiler` | 130-190 | RSS/VMS memory tracking |
| **Benchmarking** | `performance_monitor.py` | `Benchmark` | 195-260 | Performance profiling tools |

---

## Performance Metrics

The system collects and reports comprehensive performance metrics across multiple dimensions:

### Video Processing Metrics

**Frames Per Second (FPS)**: Measures system throughput by tracking frames processed per second. Current, average, minimum, and maximum FPS values are maintained.

**Processing Latency**: Time required to process each frame through the complete pipeline (fetch, decode, execute, write-back). Measured in milliseconds with histogram distribution.

**Pipeline Efficiency**: Ratio of actual throughput to theoretical maximum throughput based on pipeline design. Identifies pipeline stalls and hazards.

**Cycles Per Instruction (CPI)**: Equivalent metric showing average clock cycles needed per frame operation. Lower values indicate better efficiency.

### Detection Metrics

**Motion Detection Rate**: Percentage of frames where motion is detected. Tracks both instantaneous and rolling average rates.

**False Positive Rate**: Percentage of motion detections that don't result in alarm triggers. Used to tune detection sensitivity.

**Face Recognition Latency**: Average time to perform face recognition operation. Includes both cache hits and cache misses.

**Detection Accuracy**: Percentage of correct identifications (authorized vs. unauthorized persons) validated against ground truth.

**Cache Hit Rate**: Percentage of face recognition requests served from cache vs. requiring disk access. Higher rates indicate better memory hierarchy utilization.

### System Resource Metrics

**CPU Utilization**: Per-thread and system-wide CPU usage as percentage of available capacity. Broken down by capture, processing, and alert threads.

**Memory Usage**: 
- RSS (Resident Set Size): Physical memory actually used
- VMS (Virtual Memory Size): Total virtual memory allocated
- Peak usage: Maximum memory used during operation
- Memory growth rate: Rate of memory consumption over time

**Thread Metrics**:
- Active thread count
- Thread creation/destruction rate
- Context switch frequency
- Lock contention statistics

### I/O Performance Metrics

**Disk Write Throughput**: Megabytes per second written to disk for image capture and logging. Measures storage subsystem performance.

**File Operation Counts**: Total read and write operations, successful vs. failed operations, and operation latency distribution.

**Storage Utilization**: Current disk usage for logs and captured images, with projections for space exhaustion.

**Network I/O**: Email notification success rate, average transmission time, and network latency when notifications are enabled.

### Reports and Visualization

Performance reports are automatically generated at configured intervals and saved to `storage/logs/performance_report_TIMESTAMP.json`. Reports include:

- Aggregate statistics for all metric categories
- Time-series data for trending analysis
- Comparative analysis against baseline performance
- Bottleneck identification and optimization recommendations
- System health indicators and alerts

Example report structure:
```json
{
  "timestamp": "2024-11-07T10:30:00",
  "duration_seconds": 3600,
  "video_processing": {
    "average_fps": 28.5,
    "min_fps": 22.1,
    "max_fps": 30.0,
    "average_latency_ms": 35.1,
    "pipeline_efficiency": 0.95
  },
  "detection": {
    "motion_detection_rate": 0.15,
    "false_positive_rate": 0.03,
    "face_recognition_latency_ms": 125.3,
    "cache_hit_rate": 0.82
  },
  "resources": {
    "average_cpu_percent": 45.2,
    "peak_memory_mb": 512.3,
    "thread_count": 4
  },
  "io": {
    "disk_write_throughput_mbps": 2.1,
    "total_write_operations": 1547,
    "storage_used_mb": 2048.5
  }
}
```

---

## Authorized Face Management

### Adding Authorized Faces

**Method 1: Manual Addition**
1. Create directory: `storage/authorized_faces/` (if not exists)
2. Add face images with naming convention: `person_name.jpg`
3. Supported formats: JPG, PNG, BMP
4. Image requirements:
   - Clear, well-lit face photo
   - Face should occupy at least 30% of image
   - Minimal occlusions (no sunglasses, masks)
   - Multiple angles recommended for better recognition

**Method 2: Training Script**
```powershell
python scripts/train_faces.py --add-person "John Doe"
```
This launches webcam capture mode to collect multiple face samples.

**Method 3: Bulk Import**
```powershell
python scripts/train_faces.py --import-dir /path/to/faces/
```
Processes entire directory of labeled face images.

### Face Database Structure

```
storage/authorized_faces/
├── john_doe_1.jpg
├── john_doe_2.jpg        # Multiple samples improve accuracy
├── jane_smith_1.jpg
├── jane_smith_2.jpg
└── encodings.pkl         # Pre-computed face encodings (auto-generated)
```

### Recognition Process

1. System loads all images from `authorized_faces/` on startup
2. Face encodings are computed and cached in memory (LRU cache)
3. Each detected face is compared against authorized database
4. Confidence scores above threshold trigger authorized person detection
5. Unauthorized faces trigger alarm sequence
6. Face database is automatically reloaded on file system changes

### Best Practices

- Use 3-5 images per person with varying angles and lighting
- Update images periodically to account for appearance changes
- Higher resolution source images improve recognition accuracy
- Ensure consistent naming convention for organization
- Remove outdated or low-quality images that cause false negatives

---

## Testing and Validation

### Unit Tests

**Memory Management Tests**:
```powershell
python -m pytest tests/test_memory.py -v
```
Tests circular buffer operations, LRU cache behavior, and memory hierarchy simulation.

**Motion Detection Tests**:
```powershell
python -m pytest tests/test_motion_detection.py -v
```
Validates ALU operations, threshold comparisons, and contour detection accuracy.

**State Machine Tests**:
```powershell
python -m pytest tests/test_state_machine.py -v
```
Verifies state transitions, timing requirements, and invalid state prevention.

**Performance Tests**:
```powershell
python -m pytest tests/test_performance.py -v
```
Benchmarks FPS, latency, and resource utilization under various loads.

### Integration Tests

**Full System Test**:
```powershell
python -m pytest tests/test_integration.py -v
```
End-to-end testing with simulated webcam input and event sequences.

### Continuous Testing

**Run All Tests**:
```powershell
python -m pytest tests/ -v --cov=src --cov-report=html
```
Generates code coverage report in `htmlcov/` directory.

### Performance Benchmarking

**Standard Benchmark**:
```powershell
python scripts/benchmark.py
```
Runs standardized performance tests and generates comparison report.

**Stress Test**:
```powershell
python scripts/benchmark.py --stress --duration 300
```
5-minute stress test with maximum load to identify memory leaks and performance degradation.

**Profiling Mode**:
```powershell
python -m cProfile -o profile.stats main.py
python scripts/analyze_profile.py profile.stats
```
Detailed execution profiling with bottleneck identification.

---

## Performance Optimization Guide

### Improving Frame Rate

**Resolution Reduction**: Lower camera resolution reduces processing load
```json
"resolution": [320, 240]  // From [640, 480]
```
Expected improvement: 40-60% FPS increase

**Detection Interval**: Skip frames between detection operations
```json
"detection_interval": 3  // Check every 3rd frame instead of every frame
```
Expected improvement: 2-3x FPS increase with minimal detection accuracy loss

**Disable Face Recognition**: If not needed, disable for significant performance gain
```json
"face_recognition": {"enabled": false}
```
Expected improvement: 50-100% FPS increase

**Optimize Blur Kernel**: Smaller kernel size reduces preprocessing time
```json
"gaussian_blur_kernel": 15  // From 21
```
Expected improvement: 10-15% FPS increase

### Reducing Memory Usage

**Buffer Size Reduction**: Decrease circular buffer capacity
```json
"frame_buffer_size": 15  // From 30
```
Expected savings: 50% buffer memory usage

**Cache Size Reduction**: Limit face recognition cache entries
```json
"cache_size": 50  // From 100
```
Expected savings: 50% cache memory usage

**Log Rotation**: Enable automatic old file deletion
```json
"max_log_files": 20,
"max_image_files": 100
```
Prevents unbounded disk usage growth

**Disable Performance Monitoring**: Reduces overhead when not needed
```json
"enable_monitoring": false
```
Expected savings: 5-10% memory usage

### Reducing False Alarms

**Increase Motion Threshold**: Less sensitive to minor movements
```json
"threshold": 35  // From 25
```
Reduces false positives from lighting changes, shadows

**Increase Contour Area**: Filter out small motion regions
```json
"min_contour_area": 1000  // From 500
```
Eliminates detections from insects, curtains, etc.

**Extend Alert Period**: Longer evaluation before alarm
```json
"alert_evaluation_period": 5  // From 2 seconds
```
Allows more time to confirm threat vs. transient motion

**Adjust Gaussian Blur**: More blur reduces noise sensitivity
```json
"gaussian_blur_kernel": 25  // From 21
```
Smooths out minor pixel variations

### Hardware-Specific Optimizations

**GPU Acceleration** (if available):
```json
"face_recognition": {"model": "cnn"}  // From "hog"
```
Requires CUDA-compatible GPU, provides 5-10x speedup for face recognition

**Multi-core Utilization**: Increase worker threads
```python
thread_count = os.cpu_count()  // Use all available cores
```
Improves parallel processing efficiency

---

## Troubleshooting

### Camera Issues

**Problem**: "Camera not available" or "Failed to open camera"

**Solutions**:
1. Verify camera connection: `ls /dev/video*` (Linux) or Device Manager (Windows)
2. Try different device IDs in config.json: 0, 1, 2
3. Check camera permissions: `sudo chmod 666 /dev/video0` (Linux)
4. Close other applications using camera (Zoom, Skype, etc.)
5. Test with: `python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"`

**Problem**: Poor video quality or frozen frames

**Solutions**:
1. Reduce FPS in configuration if CPU is overloaded
2. Check USB bandwidth if using multiple cameras
3. Update camera drivers
4. Disable auto-exposure if lighting is consistent

### Import and Dependency Errors

**Problem**: "ModuleNotFoundError" or import failures

**Solutions**:
1. Verify virtual environment is activated: `which python` should show venv path
2. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
3. Check Python version: `python --version` (requires 3.8+)
4. For face_recognition issues on Windows: Install Visual C++ Build Tools
5. For OpenCV issues: `pip uninstall opencv-python opencv-contrib-python` then `pip install opencv-python`

**Problem**: "No module named 'face_recognition'"

**Solutions**:
1. Install system dependencies first (cmake, boost)
2. Install dlib separately: `pip install dlib`
3. Then install face_recognition: `pip install face_recognition`
4. On macOS: `brew install cmake` before pip install

### High Resource Usage

**Problem**: CPU usage above 80%

**Solutions**:
1. Reduce FPS: Set `"fps": 15` in config
2. Lower resolution: Set `"resolution": [320, 240]`
3. Increase detection intervals
4. Disable face recognition if not needed
5. Close background applications
6. Monitor with: `python scripts/benchmark.py --monitor`

**Problem**: High memory usage or memory leaks

**Solutions**:
1. Reduce buffer sizes in configuration
2. Enable log rotation to prevent unbounded growth
3. Check for circular references in custom code
4. Run memory profiler: `python -m memory_profiler main.py`
5. Restart system periodically if deployed long-term

### Detection Accuracy Issues

**Problem**: Missing motion events (false negatives)

**Solutions**:
1. Lower motion threshold: `"threshold": 15`
2. Decrease minimum contour area: `"min_contour_area": 300`
3. Improve lighting conditions
4. Clean camera lens
5. Adjust camera angle to cover motion area
6. Test with: `python main.py --debug` to visualize detection

**Problem**: Too many false alarms (false positives)

**Solutions**:
1. Increase motion threshold: `"threshold": 40`
2. Increase contour area: `"min_contour_area": 1500`
3. Extend alert evaluation period
4. Stabilize camera mount to reduce vibration
5. Avoid areas with moving shadows, curtains, pets
6. Use face recognition to filter authorized persons

**Problem**: Face recognition not working

**Solutions**:
1. Verify authorized face images are in correct directory
2. Check image quality: faces should be clear and well-lit
3. Increase confidence threshold if too strict
4. Add multiple images per person from different angles
5. Retrain face encodings: Delete `encodings.pkl` and restart
6. Test individual images: `python scripts/test_face.py image.jpg`

### Alarm and Notification Issues

**Problem**: Alarm not triggering

**Solutions**:
1. Verify alarm is enabled in config: `"alarm": {"enabled": true}`
2. Check audio file exists and is valid format
3. Test audio system: `python -c "import pygame; pygame.mixer.init(); pygame.mixer.music.load('alarm.wav'); pygame.mixer.music.play()"`
4. Verify system is in MONITORING state, not IDLE
5. Check cooldown period hasn't been triggered recently

**Problem**: Email notifications not sending

**Solutions**:
1. Verify SMTP settings in configuration
2. Enable "Less secure app access" or generate app-specific password for Gmail
3. Check firewall rules allowing SMTP port (587 or 465)
4. Test SMTP connection: `python scripts/test_email.py`
5. Verify recipient email address is correct
6. Check spam folder for notifications
7. Enable debug logging to see SMTP errors

### File System and Storage Issues

**Problem**: "Permission denied" when saving images or logs

**Solutions**:
1. Verify write permissions: `ls -la storage/`
2. Create directories manually: `mkdir -p storage/{intruders,logs,authorized_faces}`
3. Run with appropriate permissions or change ownership
4. Check disk space: `df -h`
5. Verify path separators are correct for OS

**Problem**: Storage directory filling up quickly

**Solutions**:
1. Enable log rotation with max file limits
2. Implement auto-cleanup for old intruder images
3. Compress old log files: `gzip storage/logs/*.log`
4. Reduce image capture frequency during alarms
5. Use lower resolution for captured images
6. Set up external storage or network drive

### State Machine Issues

**Problem**: System stuck in ALERT or ALARM state

**Solutions**:
1. Press 'r' key to manually reset state
2. Check timer logic in state_machine.py
3. Verify state transition validation is working
4. Restart application to reset state
5. Check logs for error messages: `tail -f storage/logs/system.log`

**Problem**: Rapid state transitions or oscillations

**Solutions**:
1. Increase cooldown period to prevent rapid re-triggering
2. Extend alert evaluation period for more stable detection
3. Add hysteresis to motion detection threshold
4. Implement state change rate limiting
5. Review state transition logs to identify patterns

---

## Learning Outcomes

### Computer Organization & Architecture Concepts

**Memory Hierarchy Understanding**: Students gain practical experience with multi-level memory systems, understanding the trade-offs between capacity, speed, and cost. The circular buffer simulates L1 cache behavior, while the LRU cache demonstrates cache replacement policies and their impact on performance.

**CPU Architecture and Pipelining**: The four-stage pipeline (Fetch, Decode, Execute, Write-back) provides hands-on experience with instruction-level parallelism, pipeline hazards, and throughput optimization. Students learn how modern CPUs achieve high performance through concurrent instruction processing.

**Thread Synchronization and Concurrency**: Multi-threaded architecture demonstrates real-world challenges of parallel processing including race conditions, deadlocks, and proper use of synchronization primitives (locks, semaphores, mutexes).

**Arithmetic Logic Unit Operations**: Direct implementation of ALU-style operations for image processing shows how low-level arithmetic and boolean logic gates combine to perform complex computations.

**I/O Systems and Device Management**: Interaction with webcam (input device), display (output device), and file system demonstrates polling vs. interrupt-driven I/O, buffering strategies, and device driver concepts.

**Performance Optimization**: Real-time metrics collection and analysis teaches students to identify bottlenecks, measure optimization impact, and understand the relationship between hardware resources and software performance.

**State Machine Design**: Finite state machine implementation provides experience with control flow, event-driven programming, and deterministic system behavior crucial for embedded systems and hardware design.

### Software Engineering Skills

**System Architecture Design**: Experience designing modular, maintainable systems with clear separation of concerns and well-defined interfaces between components.

**Performance Profiling**: Hands-on practice with performance measurement tools, bottleneck identification, and data-driven optimization decisions.

**Testing and Validation**: Unit testing, integration testing, and benchmarking practices ensure system reliability and correctness.

**Documentation**: Comprehensive documentation demonstrates the importance of clear technical writing for maintaining and extending complex systems.

### Computer Vision and AI

**Motion Detection Algorithms**: Understanding frame differencing, background subtraction, and contour analysis for real-time object detection.

**Face Recognition Systems**: Experience with machine learning-based recognition, confidence scoring, and database management for identification tasks.

**Real-time Processing**: Techniques for achieving real-time performance with computationally intensive algorithms through optimization and hardware utilization.

---

## Advanced Topics

### GPU Acceleration

For systems with CUDA-compatible GPUs, significant performance improvements are possible:

**Configuration**:
```json
{
  "face_recognition": {
    "model": "cnn",
    "batch_size": 8,
    "gpu_memory_fraction": 0.5
  },
  "motion_detection": {
    "use_gpu": true
  }
}
```

**Expected Performance**:
- Face recognition: 5-10x speedup
- Motion detection: 2-3x speedup
- Overall system: 3-5x throughput improvement

**Requirements**:
- NVIDIA GPU with CUDA support
- CUDA Toolkit 11.0 or higher
- cuDNN library
- GPU-enabled OpenCV build

### Deep Learning Integration

Replace traditional motion detection with YOLO-based object detection:

**Installation**:
```powershell
pip install ultralytics
```

**Configuration**:
```json
{
  "detection": {
    "method": "yolo",
    "model": "yolov8n.pt",
    "confidence": 0.5,
    "classes": ["person"]
  }
}
```

**Advantages**:
- Higher accuracy with complex scenes
- Object classification (person, vehicle, animal)
- Reduced false positives from non-person motion

**Trade-offs**:
- Higher computational requirements
- Requires GPU for real-time performance
- Larger model files and memory usage

### Cloud Storage Integration

Upload intruder images and logs to cloud storage:

**AWS S3 Integration**:
```python
# config.json
{
  "storage": {
    "backend": "s3",
    "bucket": "my-security-system",
    "region": "us-east-1"
  }
}
```

**Features**:
- Automatic backup of critical events
- Remote access to captured images
- Scalable storage without local disk limits
- Integration with cloud-based analytics

### Mobile Notifications

Real-time push notifications to mobile devices:

**Telegram Integration**:
```json
{
  "notifications": {
    "telegram_enabled": true,
    "bot_token": "YOUR_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID"
  }
}
```

**WhatsApp Integration** (via Twilio):
```json
{
  "notifications": {
    "whatsapp_enabled": true,
    "twilio_account_sid": "YOUR_SID",
    "twilio_auth_token": "YOUR_TOKEN",
    "from_number": "whatsapp:+14155238886",
    "to_number": "whatsapp:+1234567890"
  }
}
```

### Multi-Camera Support

Monitor multiple locations simultaneously:

**Configuration**:
```json
{
  "cameras": [
    {"id": 0, "name": "Front Door", "resolution": [640, 480]},
    {"id": 1, "name": "Back Yard", "resolution": [640, 480]},
    {"id": 2, "name": "Garage", "resolution": [320, 240]}
  ]
}
```

**Architecture**:
- Separate processing thread per camera
- Shared state machine and alarm system
- Combined dashboard display
- Per-camera configuration and tuning

### Web Dashboard

Browser-based monitoring interface:

**Features**:
- Live video stream from all cameras
- Real-time performance metrics
- Historical event log and playback
- Remote arm/disarm control
- Configuration management
- System health monitoring

**Technology Stack**:
- Flask/FastAPI backend
- WebSocket for real-time updates
- React/Vue.js frontend
- Chart.js for metrics visualization

### Edge Deployment

Deploy on edge devices for low-power operation:

**Raspberry Pi Optimization**:
```json
{
  "performance": {
    "mode": "edge",
    "target_fps": 10,
    "resolution": [320, 240],
    "enable_hardware_acceleration": true
  }
}
```

**NVIDIA Jetson Nano**:
```json
{
  "performance": {
    "mode": "jetson",
    "use_tensorrt": true,
    "gpu_memory_fraction": 0.8
  }
}
```

---

## API Reference

### Core Classes

**CircularFrameBuffer**:
```python
from src.memory_management import CircularFrameBuffer

buffer = CircularFrameBuffer(capacity=30)
buffer.push(frame)           # Add frame to buffer
frame = buffer.pop()         # Remove and return oldest frame
frame = buffer.peek()        # View oldest frame without removing
is_full = buffer.is_full()   # Check if buffer is at capacity
buffer.clear()               # Remove all frames
```

**LRUCache**:
```python
from src.memory_management import LRUCache

cache = LRUCache(max_size=100)
cache.put(key, value)        # Store item in cache
value = cache.get(key)       # Retrieve item (None if not found)
exists = cache.contains(key) # Check if key exists
hit_rate = cache.hit_rate()  # Get cache hit rate percentage
cache.clear()                # Remove all items
```

**StateMachine**:
```python
from src.state_machine import StateMachine, SystemState

fsm = StateMachine()
fsm.transition_to(SystemState.MONITORING)  # Change state
current = fsm.current_state                # Get current state
is_valid = fsm.can_transition(new_state)   # Check if transition is valid
fsm.update(detected=True, authorized=False) # Process detection event
```

**MotionDetector**:
```python
from src.motion_detection import MotionDetector

detector = MotionDetector(threshold=25, min_area=500)
motion_detected, contours = detector.detect(frame)
visualization = detector.visualize(frame)  # Draw detection overlay
sensitivity = detector.get_sensitivity()   # Get current threshold
detector.set_sensitivity(30)               # Update threshold
```

**PerformanceMonitor**:
```python
from src.performance_monitor import PerformanceMonitor

monitor = PerformanceMonitor()
monitor.start()                           # Begin monitoring
fps = monitor.get_fps()                   # Current frames per second
cpu = monitor.get_cpu_usage()             # CPU usage percentage
memory = monitor.get_memory_usage()       # Memory usage in MB
report = monitor.generate_report()        # Full performance report
monitor.stop()                            # Stop monitoring
```

### Configuration API

**Load Configuration**:
```python
from src.config import Config

config = Config.load('config.json')
camera_id = config.get('camera.device_id', default=0)
threshold = config.get('motion_detection.threshold')
```

**Update Configuration at Runtime**:
```python
config.set('motion_detection.threshold', 30)
config.save('config.json')
```

### Event Callbacks

**Register Event Handlers**:
```python
def on_motion_detected(frame, contours):
    print(f"Motion detected with {len(contours)} contours")

def on_face_recognized(name, confidence):
    print(f"Recognized {name} with {confidence:.2f} confidence")

def on_alarm_triggered(reason):
    print(f"Alarm triggered: {reason}")

system.register_callback('motion_detected', on_motion_detected)
system.register_callback('face_recognized', on_face_recognized)
system.register_callback('alarm_triggered', on_alarm_triggered)
```

---

## Contributing

Contributions are welcome! This project serves both as a functional security system and an educational platform for learning Computer Organization and Architecture concepts.

### Development Setup

**Fork and Clone**:
```bash
git clone https://github.com/yourusername/Anti-Theft-Alarm-System.git
cd Anti-Theft-Alarm-System
git checkout -b feature/your-feature-name
```

**Install Development Dependencies**:
```bash
pip install -r requirements-dev.txt
```

This includes:
- pytest for testing
- black for code formatting
- pylint for linting
- mypy for type checking
- sphinx for documentation

**Code Style**:
- Follow PEP 8 guidelines
- Use type hints for function signatures
- Maximum line length: 100 characters
- Use docstrings for all public methods

**Before Submitting**:
```bash
# Format code
black src/ tests/

# Run linter
pylint src/ tests/

# Type checking
mypy src/

# Run tests
pytest tests/ -v --cov=src

# Build documentation
cd docs && make html
```

### Contribution Areas

**Core Features**:
- Additional detection algorithms
- New state machine states or transitions
- Enhanced memory management strategies
- Performance optimizations

**COA Educational Content**:
- New COA concept demonstrations
- Improved documentation of existing concepts
- Visual diagrams and explanations
- Interactive tutorials

**Testing**:
- Additional unit tests
- Integration test scenarios
- Performance benchmarks
- Edge case coverage

**Documentation**:
- Tutorial improvements
- API documentation
- Architecture diagrams
- Example use cases

### Pull Request Process

1. Create an issue describing the enhancement or bug fix
2. Develop on a feature branch
3. Ensure all tests pass and coverage remains high
4. Update documentation reflecting changes
5. Submit pull request with clear description
6. Address review feedback
7. Merge after approval

---

## License

MIT License

Copyright (c) 2024 Anti-Theft Alarm System Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Acknowledgments

**Computer Vision Libraries**:
- OpenCV community for comprehensive computer vision tools and documentation
- dlib developers for face detection and recognition algorithms
- face_recognition library maintainers for simplified face recognition API

**Educational Resources**:
- Computer Organization and Design (Patterson & Hennessy) for COA fundamentals
- Computer Architecture: A Quantitative Approach for advanced topics
- Operating Systems: Three Easy Pieces for threading and synchronization concepts

**Development Tools**:
- Python Software Foundation for the Python programming language
- pytest team for testing framework
- GitHub for version control and collaboration platform

**Community Contributors**:
- All contributors who have submitted bug reports, feature requests, and code improvements
- Educators using this project in COA courses
- Students providing feedback on learning effectiveness

---

## Citation

If you use this project in academic work or research, please cite:

```bibtex
@software{antitheft_alarm_system,
  title = {Anti-Theft Alarm System: Integrating Computer Vision with COA},
  author = {[Your Name]},
  year = {2024},
  url = {https://github.com/yourusername/Anti-Theft-Alarm-System},
  note = {Educational implementation of computer organization concepts}
}
```

---

## Support and Contact

**Bug Reports and Feature Requests**:
- GitHub Issues: https://github.com/yourusername/Anti-Theft-Alarm-System/issues
- Use issue templates for consistent reporting
- Include system information and logs when reporting bugs

**Documentation**:
- Full documentation: https://antitheft-docs.readthedocs.io
- API Reference: https://antitheft-docs.readthedocs.io/api
- Tutorial videos: [YouTube channel link]

**Community**:
- Discussion Forum: https://github.com/yourusername/Anti-Theft-Alarm-System/discussions
- Discord Server: [Discord invite link]
- Stack Overflow Tag: anti-theft-alarm-system

**Email Support**:
- General inquiries: info@example.com
- Academic partnerships: academic@example.com
- Security issues: security@example.com

---

## Roadmap

### Version 2.0 (Q1 2025)

**Core Enhancements**:
- GPU acceleration for all processing pipelines
- YOLO-based object detection integration
- Multi-camera support with synchronized processing
- Web dashboard for remote monitoring

**COA Concepts**:
- SIMD instruction demonstration
- Branch prediction simulation
- Cache coherence protocol implementation
- Virtual memory management demonstration

### Version 2.5 (Q2 2025)

**Advanced Features**:
- Deep learning-based person re-identification
- Behavioral analysis and anomaly detection
- Cloud storage integration (AWS S3, Google Cloud)
- Mobile app for iOS and Android

**Performance**:
- Real-time 4K video processing
- Sub-10ms detection latency
- 99.9% uptime for continuous monitoring
- Reduced memory footprint by 40%

### Version 3.0 (Q3 2025)

**Enterprise Features**:
- Multi-tenant support for commercial deployment
- Role-based access control
- Audit logging and compliance reporting
- Integration with existing security systems

**AI/ML**:
- Predictive threat assessment
- Automatic sensitivity tuning based on environment
- Scene understanding and context awareness
- Voice command integration

---

## Frequently Asked Questions

**Q: Can this system replace commercial security systems?**  
A: This is primarily an educational project demonstrating COA concepts. While functional, commercial security systems have additional features, certifications, and reliability requirements for critical applications.

**Q: What hardware is recommended?**  
A: Minimum: Dual-core CPU, 2GB RAM, webcam. Recommended: Quad-core CPU, 4GB RAM, HD webcam. For optimal performance: GPU with CUDA support.

**Q: Can I use this commercially?**  
A: Yes, the MIT license permits commercial use. However, ensure you meet all legal requirements for surveillance systems in your jurisdiction.

**Q: How accurate is the face recognition?**  
A: Accuracy depends on image quality, lighting, and database size. Expect 90-95% accuracy under good conditions. Multiple training images per person improve accuracy.

**Q: Does this work on Raspberry Pi?**  
A: Yes, with optimization. Use lower resolution (320x240), reduce FPS to 10-15, and disable face recognition or use lightweight models for acceptable performance.

**Q: Can I access the system remotely?**  
A: Not out of the box, but web dashboard and mobile app features are planned for future releases. You can implement remote access using Flask/FastAPI backend.

**Q: How much storage is needed?**  
A: Depends on usage. Expect 1-2GB per day with default settings (captured images + logs). Implement log rotation and old file cleanup for long-term deployment.

**Q: Is GPU required?**  
A: No, the system runs on CPU only. GPU acceleration significantly improves performance but is optional.

**Q: Can I integrate with other systems?**  
A: Yes, the modular architecture and event callback system allow integration with home automation systems, alarm panels, and other security infrastructure.

---

**Version**: 1.0.0  
**Last Updated**: November 2024  
**Status**: Active Development

---

**Built with dedication for Computer Architecture Education**
