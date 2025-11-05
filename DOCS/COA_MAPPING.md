# Computer Organization & Architecture Mapping Document

## Overview
This document maps each component of the Anti-Theft Alarm System to specific Computer Organization & Architecture concepts.

---

## 1. Memory Organization

### 1.1 Circular Frame Buffer (L1 Cache Simulation)

**File**: `src/memory_management.py` - `CircularFrameBuffer` class

**COA Concepts**:
- **FIFO Queue Structure**: First-In-First-Out data structure
- **Fixed Memory Allocation**: Static buffer size (simulates hardware constraints)
- **Read/Write Pointers**: Head and tail pointers for circular access
- **Overflow Handling**: Buffer full condition management
- **Sequential Access**: Consecutive memory locations

**How It Works**:
```python
buffer[head] = new_frame  # Write operation
head = (head + 1) % capacity  # Circular increment
```

**Key Metrics**:
- Buffer utilization percentage
- Overflow count (frame drops)
- Read/write operation counts

---

### 1.2 LRU Cache (L2 Cache)

**File**: `src/memory_management.py` - `LRUCache` class

**COA Concepts**:
- **Cache Replacement Policy**: Least Recently Used algorithm
- **Cache Hit/Miss**: Performance tracking
- **Hash Table**: O(1) lookup time
- **Temporal Locality**: Recently used data likely to be reused
- **Eviction Policy**: Remove oldest entry when full

**Cache Hit Rate Formula**:
```
Hit Rate = (Cache Hits / Total Accesses) × 100%
```

**Performance Impact**:
- High hit rate (>80%) = Excellent cache performance
- Low hit rate (<50%) = Poor temporal locality

---

### 1.3 Memory Hierarchy

**File**: `src/memory_management.py` - `MemoryHierarchy` class

**Levels**:
1. **L1 Cache** (Frame Buffer): 1 μs access time
2. **L2 Cache** (Face Database): 10 μs access time
3. **Main Memory** (RAM): 100 μs access time
4. **Secondary Storage** (Disk): 10,000 μs access time

**Trade-offs**:
- Speed vs Capacity
- Cost vs Performance
- Volatile vs Non-volatile

---

## 2. CPU Architecture

### 2.1 Instruction Pipeline

**File**: `src/cpu_architecture.py` - `Pipeline` class

**Pipeline Stages**:
1. **FETCH**: Acquire frame from camera (I/O read)
2. **DECODE**: Preprocess frame (grayscale, blur)
3. **EXECUTE**: Perform detection (motion/face)
4. **WRITEBACK**: Store results, trigger actions

**Performance Metrics**:
- **Throughput**: Frames per second (FPS)
- **Latency**: Time per frame (milliseconds)
- **CPI**: Average time / Ideal time

**Pipeline Hazards**:
- **Data Hazard**: Dependency between stages
- **Structural Hazard**: Resource conflict
- **Control Hazard**: State changes

---

### 2.2 Multi-Threading & Parallelism

**File**: `src/cpu_architecture.py` - `WorkerThread` class

**Threads**:
1. **Video Capture Thread**: Continuous frame acquisition
2. **Processing Thread**: Motion and face detection
3. **Alert Thread**: Alarm and notification handling
4. **Monitor Thread**: Performance tracking

**Synchronization**:
- **Locks** (`threading.Lock`): Mutual exclusion
- **Semaphores** (`threading.Semaphore`): Resource counting
- **Queues** (`queue.Queue`): Inter-thread communication

**Parallel Speedup**:
```
Speedup = Sequential Time / Parallel Time
```

---

### 2.3 CPU Monitoring

**File**: `src/cpu_architecture.py` - `CPUMonitor` class

**Metrics Tracked**:
- **CPU Utilization**: Percentage of CPU time used
- **Per-Core Usage**: Individual core statistics
- **Process CPU Time**: User + System time
- **Thread Count**: Number of active threads

---

## 3. Arithmetic & Logic Unit (ALU)

### 3.1 Pixel-Level Arithmetic

**File**: `src/motion_detection.py` - `ArithmeticLogicUnit` class

**Operations**:

**Subtraction** (Frame Differencing):
```python
diff = |frame1 - frame2|  # Absolute difference
```

**Addition** (Frame Blending):
```python
result = frame1 + frame2
```

**Multiplication** (Brightness Adjustment):
```python
result = frame × scalar
```

**Use Case**: Motion detection by comparing consecutive frames

---

### 3.2 Boolean Logic Operations

**File**: `src/motion_detection.py` - `BooleanLogic` class

**Logic Gates**:

**AND Gate**:
```python
output = a AND b  # True only if both True
```

**OR Gate**:
```python
output = a OR b  # True if at least one True
```

**NOT Gate**:
```python
output = NOT a  # Inverse
```

**XOR Gate**:
```python
output = a XOR b  # True if inputs different
```

**Alarm Logic Circuit**:
```python
detection = motion_detected OR unknown_face
alarm = detection AND system_armed
```

Truth Table:
| Motion | Unknown | Armed | Alarm |
|--------|---------|-------|-------|
| 0      | 0       | 0     | 0     |
| 0      | 0       | 1     | 0     |
| 0      | 1       | 1     | 1     |
| 1      | 0       | 1     | 1     |
| 1      | 1       | 1     | 1     |

---

### 3.3 Bitwise Operations

**File**: `src/motion_detection.py`

**Operations**:
- **AND**: Image masking
- **OR**: Combining regions
- **NOT**: Color inversion
- **XOR**: Change detection

**Example** (Masking):
```python
masked_image = image AND mask
```

---

## 4. Input/Output Systems

### 4.1 I/O Devices

**File**: `src/io_storage.py`

**Input Devices**:
- **Webcam**: Video capture (polling-based I/O)
  - Read operation: `camera.read()`
  - Polling frequency: 30 FPS

**Output Devices**:
- **Display**: Frame rendering
- **Speaker**: Alarm sound
- **Disk**: Image storage
- **Network**: Email/SMS

**I/O Methods**:
1. **Polling**: Continuously check device status
2. **Interrupt-Driven**: Device notifies when ready (simulated)
3. **DMA**: Direct Memory Access (conceptual)

---

### 4.2 File System Operations

**File**: `src/io_storage.py` - `FileSystem` class

**Operations**:
- **Sequential Write**: Log files (append mode)
- **Random Access**: Image files (direct path access)
- **Directory Management**: Create/delete folders
- **Storage Monitoring**: Track disk usage

**Performance Metrics**:
- **Write Throughput**: MB/s
- **Read Throughput**: MB/s
- **Average Access Time**: Milliseconds

---

## 5. State Machines

### 5.1 Finite State Machine (FSM)

**File**: `src/state_machine.py` - `StateMachine` class

**States**:
1. **IDLE**: System inactive
2. **MONITORING**: Active surveillance
3. **ALERT**: Potential threat (evaluation)
4. **ALARM**: Confirmed threat (alarm active)
5. **COOLDOWN**: Post-alarm recovery

**State Transition Diagram**:
```
IDLE ←→ MONITORING ←→ ALERT → ALARM → COOLDOWN ↺
```

**Transition Logic**:
- Validates all transitions before execution
- Maintains state history
- Executes callbacks on state entry

**State Register**: Stores current system state

---

### 5.2 Control Flow

**Implementation**:
```python
if motion_detected AND system_armed:
    if current_state == MONITORING:
        transition_to(ALERT)
    elif current_state == ALERT AND time_in_state > 2:
        transition_to(ALARM)
```

**Combinational Logic**: Output depends only on current inputs
**Sequential Logic**: Output depends on current state and inputs

---

## 6. Performance Monitoring

### 6.1 Throughput Measurement

**File**: `src/performance_monitor.py` - `FPSCounter` class

**Throughput (FPS)**:
```
FPS = Number of Frames / Time Elapsed
```

**Target Performance**:
- Real-time: 30 FPS
- Acceptable: 15-20 FPS
- Poor: < 10 FPS

---

### 6.2 Latency Measurement

**Latency** = Time to process single frame

**Components**:
- Capture time
- Preprocessing time
- Detection time
- Rendering time

**Total Latency** = Sum of all component times

---

### 6.3 CPI (Cycles Per Instruction)

**Formula**:
```
CPI = Average Frame Time / Ideal Frame Time
```

**Interpretation**:
- CPI = 1: Perfect efficiency
- CPI > 1: Pipeline stalls or slow operations
- CPI < 1: Better than expected (rare)

---

### 6.4 Cache Performance

**Cache Hit Rate**:
```
Hit Rate = Hits / (Hits + Misses) × 100%
```

**Effective Access Time**:
```
EAT = (Hit Rate × Cache Time) + (Miss Rate × Memory Time)
```

---

## 7. Data Compression

### 7.1 JPEG Compression

**File**: `src/io_storage.py`

**Trade-off**:
- Higher quality = Larger file size
- Lower quality = Smaller file size

**Compression Ratio**:
```
Ratio = Original Size / Compressed Size
```

**Quality Settings**: 0-100 (default: 85)

---

## 8. System Performance Analysis

### 8.1 Amdahl's Law

**Speedup Limit**:
```
Speedup = 1 / [(1 - P) + (P / N)]
```

Where:
- P = Parallelizable portion
- N = Number of processors

**Application**: Multi-threading benefit calculation

---

### 8.2 Performance Bottlenecks

**Common Bottlenecks**:
1. **Camera I/O**: Slow frame capture
2. **Face Recognition**: CPU-intensive
3. **Disk Writes**: Slow storage
4. **Memory Access**: Cache misses

**Optimization Strategies**:
- Increase buffer size
- Implement better caching
- Use faster storage (SSD)
- Reduce resolution

---

## Summary Table

| COA Topic | Implementation | File | Key Metric |
|-----------|----------------|------|------------|
| Memory Organization | Circular Buffer | `memory_management.py` | Utilization % |
| Cache Memory | LRU Cache | `memory_management.py` | Hit Rate % |
| Pipelining | Frame Pipeline | `cpu_architecture.py` | Throughput (FPS) |
| Multi-threading | Worker Threads | `cpu_architecture.py` | CPU Usage % |
| ALU Operations | Pixel Arithmetic | `motion_detection.py` | Processing Time |
| Boolean Logic | Alarm Logic | `motion_detection.py` | Decision Accuracy |
| State Machine | System States | `state_machine.py` | Transition Count |
| I/O Systems | File Operations | `io_storage.py` | Throughput (MB/s) |
| Performance | Metrics | `performance_monitor.py` | FPS, Latency, CPI |

---

## Conclusion

This project demonstrates **15+ COA concepts** in a practical, real-world application. Each component is carefully designed to showcase fundamental computer architecture principles while building a functional anti-theft system.

**Key Takeaway**: COA concepts are not just theoretical—they directly impact real-world software performance and design!
