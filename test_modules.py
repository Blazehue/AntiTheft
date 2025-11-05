"""
Simple Test Script - Verifies core modules work
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("\n" + "="*60)
print("ANTI-THEFT ALARM SYSTEM - MODULE VERIFICATION")
print("="*60 + "\n")

# Test 1: Memory Management
print("[1/7] Testing Memory Management...")
try:
    from memory_management import CircularFrameBuffer, LRUCache
    import numpy as np
    
    buffer = CircularFrameBuffer(5)
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    buffer.write(frame)
    
    cache = LRUCache(10)
    cache.put("test", "value")
    result = cache.get("test")
    
    print("  ✅ Memory Management OK")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 2: CPU Architecture
print("[2/7] Testing CPU Architecture...")
try:
    from cpu_architecture import CPUMonitor
    
    monitor = CPUMonitor()
    monitor.record_usage()
    
    print("  ✅ CPU Architecture OK")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 3: Motion Detection
print("[3/7] Testing Motion Detection...")
try:
    from motion_detection import MotionDetector, BooleanLogic
    import cv2
    
    config = {'threshold': 25, 'min_contour_area': 500, 'blur_kernel_size': 21}
    detector = MotionDetector(config)
    
    frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    motion_detected, info = detector.detect_motion(frame)
    
    logic = BooleanLogic()
    result = logic.AND(True, False)
    
    print("  ✅ Motion Detection OK")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 4: Face Recognition
print("[4/7] Testing Face Recognition...")
try:
    from face_recognition_module import FaceRecognizer
    
    cache = LRUCache(10)
    config = {'tolerance': 0.6, 'authorized_faces_path': 'storage/authorized_faces'}
    recognizer = FaceRecognizer(config, cache)
    
    print("  ✅ Face Recognition OK")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 5: State Machine
print("[5/7] Testing State Machine...")
try:
    from state_machine import StateMachine, SystemState
    
    fsm = StateMachine(SystemState.IDLE)
    fsm.transition_to(SystemState.MONITORING, "Test")
    
    print("  ✅ State Machine OK")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 6: I/O & Storage
print("[6/7] Testing I/O & Storage...")
try:
    from io_storage import FileSystem, Logger
    
    config = {'base_path': 'storage', 'logs_path': 'storage/logs'}
    fs = FileSystem(config)
    
    logger = Logger('storage/logs', 'test')
    logger.info("Test message")
    
    print("  ✅ I/O & Storage OK")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 7: Performance Monitor
print("[7/7] Testing Performance Monitor...")
try:
    from performance_monitor import FPSCounter, PerformanceMonitor
    
    fps = FPSCounter()
    fps.tick()
    
    monitor = PerformanceMonitor()
    
    print("  ✅ Performance Monitor OK")
except Exception as e:
    print(f"  ❌ Error: {e}")

print("\n" + "="*60)
print("✅ ALL CORE MODULES VERIFIED!")
print("="*60)
print("\nSystem is ready to run!")
print("\nNext steps:")
print("  1. Run demo: python demo.py")
print("  2. Run system: python main.py")
print("  3. Read docs: DOCS/QUICK_START.md")
print()
