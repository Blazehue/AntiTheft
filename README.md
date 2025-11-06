# Anti-Theft Alarm System(still work in progress)
**Integrating Computer Vision with Computer Organization & Architecture**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Project Overview

An intelligent anti-theft alarm system that demonstrates Computer Organization & Architecture (COA) concepts through practical computer vision implementation. This project bridges theoretical COA principles with real-world application development.

### Key Features

✅ **Real-time Motion Detection** - Frame differencing with contour analysis  
✅ **Face Recognition** - Authorized vs unauthorized person detection  
✅ **Intelligent State Machine** - IDLE → MONITORING → ALERT → ALARM states  
✅ **Multi-threaded Architecture** - Parallel processing demonstration  
✅ **Memory Management** - Circular buffers, LRU cache implementation  
✅ **Performance Monitoring** - FPS, CPU, memory metrics  
✅ **I/O & Storage Systems** - File system operations, logging  
✅ **Alert Notifications** - Email/SMS with captured images  

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     VIDEO CAPTURE THREAD                     │
│                   (I/O Device - Webcam)                      │
└───────────────────────┬─────────────────────────────────────┘
                        │ Frame Buffer (Circular Queue)
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   PROCESSING PIPELINE                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  FETCH   │→ │  DECODE  │→ │ EXECUTE  │→ │WRITEBACK │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                               │
│  Motion Detection (ALU)  ←→  Face Recognition (Cache)       │
└───────────────────────┬─────────────────────────────────────┘
                        │ Shared Memory
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    ALERT THREAD                              │
│   State Machine  →  Alarm System  →  Notifications         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 COA Concepts Demonstrated

### 1. **Memory Management**
- **Circular Frame Buffer**: FIFO queue for video frames (L1 cache simulation)
- **LRU Cache**: Least Recently Used replacement policy for face database
- **Memory Hierarchy**: RAM → Cache → Disk storage simulation
- **Performance Metrics**: Cache hit rate, memory utilization

**Implementation**: `src/memory_management.py`

### 2. **CPU Architecture**
- **Pipeline Stages**: Fetch → Decode → Execute → Write-back
- **Multi-threading**: Separate threads for capture, processing, alerts
- **Thread Synchronization**: Locks, semaphores, shared memory
- **Performance**: Throughput (FPS), Latency, CPI calculation

**Implementation**: `src/cpu_architecture.py`

### 3. **Arithmetic & Logic Operations**
- **ALU Operations**: Pixel subtraction, addition, multiplication
- **Boolean Logic**: AND, OR, NOT gates for alarm conditions
- **Bitwise Operations**: Image masking, XOR operations
- **Threshold Comparators**: Motion detection logic

**Implementation**: `src/motion_detection.py`

### 4. **I/O Systems**
- **Input Devices**: Webcam (polling-based I/O)
- **Output Devices**: Display, speaker/alarm
- **File System**: Disk read/write operations
- **Network I/O**: Email notifications (async operations)

**Implementation**: `src/io_storage.py`

### 5. **State Machines**
- **Finite State Machine**: IDLE, MONITORING, ALERT, ALARM, COOLDOWN
- **State Transitions**: Validated state changes
- **Control Flow**: Event-driven state management

**Implementation**: `src/state_machine.py`

### 6. **Performance Monitoring**
- **FPS Counter**: Frames per second (throughput)
- **CPU Utilization**: Per-thread and system-wide
- **Memory Usage**: RSS, VMS tracking
- **Benchmarking**: Execution time profiling

**Implementation**: `src/performance_monitor.py`

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Webcam (or video file for testing)
- Windows/Linux/macOS

### Step 1: Clone Repository

```powershell
cd C:\Users\pandr\OneDrive\Desktop\GithubStreaks\Day16
```

### Step 2: Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

**Note**: Some libraries (face_recognition, pygame) may require additional system dependencies.

---

## ⚙️ Configuration

Edit `config.json` to customize system behavior:

```json
{
  "camera": {
    "device_id": 0,
    "resolution": [640, 480],
    "fps": 30
  },
  "motion_detection": {
    "threshold": 25,
    "min_contour_area": 500
  },
  "alarm": {
    "enabled": true,
    "duration": 5,
    "cooldown_period": 10
  }
}
```

### Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `threshold` | Motion sensitivity (lower = more sensitive) | 25 |
| `min_contour_area` | Minimum motion area to detect | 500 |
| `frame_buffer_size` | Circular buffer capacity | 30 |
| `cache_size` | Face recognition cache size | 100 |

---

## 📖 Usage

### Basic Usage

```powershell
python main.py
```

### Keyboard Controls

- **`q`** - Quit application
- **`s`** - Toggle ARM/DISARM status

### System States

1. **IDLE** - System inactive
2. **MONITORING** - Active surveillance (default)
3. **ALERT** - Potential threat detected (2-second evaluation)
4. **ALARM** - Confirmed threat, alarm triggered
5. **COOLDOWN** - Post-alarm recovery period

---

## 📁 Project Structure

```
Day16/
├── src/
│   ├── __init__.py
│   ├── memory_management.py      # Buffers, cache, memory hierarchy
│   ├── cpu_architecture.py       # Pipeline, threading, CPU monitoring
│   ├── motion_detection.py       # ALU, boolean logic, detection
│   ├── face_recognition_module.py # Cache-based face recognition
│   ├── state_machine.py          # FSM, alarm, notifications
│   ├── io_storage.py             # File system, logging
│   └── performance_monitor.py    # FPS, metrics, reports
├── storage/
│   ├── intruders/                # Captured intruder images
│   ├── logs/                     # System and event logs
│   └── authorized_faces/         # Authorized person images
├── main.py                        # Main application
├── config.json                    # System configuration
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 🎓 COA Topic Mapping

| COA Concept | File | Line/Function |
|-------------|------|---------------|
| **Circular Buffer (FIFO)** | `memory_management.py` | `CircularFrameBuffer` class |
| **LRU Cache** | `memory_management.py` | `LRUCache` class |
| **Pipeline Stages** | `cpu_architecture.py` | `Pipeline.execute_stage()` |
| **Multi-threading** | `cpu_architecture.py` | `WorkerThread` class |
| **ALU Operations** | `motion_detection.py` | `ArithmeticLogicUnit` class |
| **Boolean Logic** | `motion_detection.py` | `BooleanLogic` class |
| **FSM** | `state_machine.py` | `StateMachine` class |
| **File I/O** | `io_storage.py` | `FileSystem` class |
| **Performance Metrics** | `performance_monitor.py` | All classes |

---

## 📊 Performance Metrics

The system tracks comprehensive performance metrics:

### Video Processing
- **FPS**: Current and average frames per second
- **Latency**: Frame processing time (milliseconds)
- **CPI**: Cycles per instruction equivalent

### Detection
- **Motion Detection Rate**: Percentage of frames with motion
- **Face Recognition Time**: Average recognition latency
- **Cache Hit Rate**: Face cache efficiency

### System Resources
- **CPU Usage**: Per-thread and system-wide
- **Memory Usage**: RSS, VMS, peak usage
- **Thread Count**: Active threads

### I/O Performance
- **Disk Write Speed**: MB/s throughput
- **File Operations**: Read/write counts
- **Storage Usage**: Disk utilization

Reports are saved to `storage/logs/performance_report_*.json`

---

## 🔧 Adding Authorized Faces

1. Create folder: `storage/authorized_faces/`
2. Add face images: `person_name.jpg`
3. Restart system to load faces

The system will recognize these faces and not trigger alarms.

---

## 🧪 Testing

### Test Motion Detection
```powershell
python -m pytest tests/test_motion_detection.py
```

### Test Memory Management
```powershell
python -m pytest tests/test_memory.py
```

### Benchmark Performance
```powershell
python scripts/benchmark.py
```

---

## 📈 Performance Optimization

### Improve FPS
- Reduce frame resolution in `config.json`
- Increase `detection_interval` for face recognition
- Disable face recognition if not needed

### Reduce Memory Usage
- Decrease `frame_buffer_size`
- Lower `cache_size`
- Enable automatic old file deletion

### Reduce False Alarms
- Increase `threshold` value
- Increase `min_contour_area`
- Extend ALERT evaluation period

---

## 🐛 Troubleshooting

### Camera Not Found
```
Error: Camera not available
Solution: Check device_id in config.json (try 0, 1, 2)
```

### Import Errors
```
Error: Module not found
Solution: Activate virtual environment and reinstall dependencies
```

### High CPU Usage
```
Issue: CPU > 80%
Solution: Reduce FPS, disable face recognition, or lower resolution
```

### Low Detection Accuracy
```
Issue: Missing motion/faces
Solution: Adjust threshold values, improve lighting, clean camera lens
```

---

## 📝 Learning Outcomes

After completing this project, you will understand:

✅ Memory hierarchy and caching mechanisms  
✅ CPU pipelining and instruction-level parallelism  
✅ Thread synchronization and parallel processing  
✅ I/O systems and device interfacing  
✅ Boolean logic and digital circuits  
✅ State machines and control flow  
✅ Performance optimization techniques  
✅ Real-world application of COA concepts  

---

## 📄 License

MIT License - feel free to use for educational purposes.

---

## 👥 Contributors

- **Your Name** - Initial implementation

---

## 🙏 Acknowledgments

- OpenCV community for computer vision tools
- Python community for excellent libraries
- COA textbooks and online resources

---

## 📞 Support

For questions or issues:
- Create an issue in the repository
- Email: your.email@example.com

---

## 🔮 Future Enhancements

- [ ] GPU acceleration using CUDA
- [ ] Deep learning-based detection (YOLO)
- [ ] Cloud storage integration
- [ ] Mobile app notifications
- [ ] Multi-camera support
- [ ] Advanced analytics dashboard
- [ ] Telegram/WhatsApp integration
- [ ] Object detection (weapons, masks)

---

**Made with ❤️ for Computer Architecture Education**
