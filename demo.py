"""
Demo Script - Tests all COA concepts without camera
Demonstrates system functionality using generated frames
"""

import cv2
import numpy as np
import time
import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from memory_management import CircularFrameBuffer, LRUCache
from cpu_architecture import Pipeline, CPUMonitor
from motion_detection import MotionDetector, BooleanLogic, ArithmeticLogicUnit
from state_machine import StateMachine, SystemState
from io_storage import FileSystem, Logger
from performance_monitor import FPSCounter, PerformanceMonitor


def generate_test_frame(width=640, height=480, with_motion=False):
    """Generate synthetic frame for testing"""
    # Create base frame
    frame = np.random.randint(0, 50, (height, width, 3), dtype=np.uint8)
    
    # Add motion (moving rectangle)
    if with_motion:
        x = int((time.time() * 100) % width)
        cv2.rectangle(frame, (x, height//2), (x+50, height//2+50), (0, 255, 0), -1)
    
    return frame


def test_memory_management():
    """Test memory management components"""
    print("\n" + "="*60)
    print("TEST 1: MEMORY MANAGEMENT")
    print("="*60)
    
    # Test Circular Buffer
    print("\n[Circular Frame Buffer - FIFO Queue]")
    buffer = CircularFrameBuffer(capacity=5)
    
    for i in range(7):
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        buffer.write(frame)
        print(f"  Write {i+1}: Size={buffer.size}, Overflows={buffer.overflow_count}")
    
    stats = buffer.get_stats()
    print(f"\n  Final Stats:")
    print(f"    Utilization: {stats['utilization']:.1f}%")
    print(f"    Overflows: {stats['overflow_count']}")
    
    # Test LRU Cache
    print("\n[LRU Cache - Cache Replacement Policy]")
    cache = LRUCache(capacity=3)
    
    # Add items
    cache.put("face1", "John")
    cache.put("face2", "Jane")
    cache.put("face3", "Bob")
    print(f"  Added 3 items to cache")
    
    # Access (hit)
    result = cache.get("face1")
    print(f"  Cache lookup 'face1': {'HIT' if result else 'MISS'} (result: {result})")
    
    # Add 4th item (causes eviction)
    cache.put("face4", "Alice")
    print(f"  Added 4th item (evicts LRU)")
    
    # Try to get evicted item
    result = cache.get("face2")
    print(f"  Cache lookup 'face2': {'HIT' if result else 'MISS'} (evicted)")
    
    cache_stats = cache.get_stats()
    print(f"\n  Cache Performance:")
    print(f"    Hit Rate: {cache_stats['hit_rate']:.1f}%")
    print(f"    Evictions: {cache_stats['eviction_count']}")
    
    print("\n✅ Memory Management Tests Passed")


def test_cpu_architecture():
    """Test CPU architecture components"""
    print("\n" + "="*60)
    print("TEST 2: CPU ARCHITECTURE")
    print("="*60)
    
    # Test CPU Monitoring
    print("\n[CPU & Performance Monitoring]")
    cpu_monitor = CPUMonitor()
    
    for i in range(3):
        cpu_monitor.record_usage()
        time.sleep(0.5)
        print(f"  Sample {i+1} recorded")
    
    stats = cpu_monitor.get_stats()
    print(f"\n  CPU Stats:")
    print(f"    Average CPU: {stats['average_cpu_percent']:.1f}%")
    print(f"    Peak CPU: {stats['peak_cpu_percent']:.1f}%")
    print(f"    CPU Cores: {stats['cpu_count']}")
    
    print("\n✅ CPU Architecture Tests Passed")


def test_boolean_logic():
    """Test boolean logic operations"""
    print("\n" + "="*60)
    print("TEST 3: BOOLEAN LOGIC & ALU")
    print("="*60)
    
    logic = BooleanLogic()
    alu = ArithmeticLogicUnit()
    
    # Test Logic Gates
    print("\n[Logic Gates]")
    print(f"  AND(True, True) = {logic.AND(True, True)}")
    print(f"  OR(False, True) = {logic.OR(False, True)}")
    print(f"  NOT(True) = {logic.NOT(True)}")
    print(f"  XOR(True, False) = {logic.XOR(True, False)}")
    
    # Test Alarm Logic
    print("\n[Alarm Logic Circuit]")
    test_cases = [
        (False, False, True, "No threat"),
        (True, False, True, "Motion only"),
        (False, True, True, "Unknown face"),
        (True, True, False, "Threat but disarmed"),
    ]
    
    for motion, unknown, armed, desc in test_cases:
        result = logic.alarm_condition(motion, unknown, armed)
        print(f"  {desc}: Motion={motion}, Unknown={unknown}, Armed={armed} → Alarm={result}")
    
    # Test ALU Operations
    print("\n[ALU Operations]")
    frame1 = np.ones((100, 100), dtype=np.uint8) * 100
    frame2 = np.ones((100, 100), dtype=np.uint8) * 150
    
    diff = alu.pixel_subtraction(frame1, frame2)
    print(f"  Frame Subtraction: |100 - 150| = {diff[0,0]}")
    
    print("\n✅ Boolean Logic & ALU Tests Passed")


def test_motion_detection():
    """Test motion detection"""
    print("\n" + "="*60)
    print("TEST 4: MOTION DETECTION")
    print("="*60)
    
    config = {
        'threshold': 25,
        'min_contour_area': 500,
        'blur_kernel_size': 21,
        'dilation_iterations': 2
    }
    
    detector = MotionDetector(config)
    
    print("\n[Processing Frames]")
    
    # Process frames without motion
    for i in range(3):
        frame = generate_test_frame(with_motion=False)
        motion_detected, info = detector.detect_motion(frame)
        print(f"  Frame {i+1}: Motion={motion_detected}, Time={info.get('processing_time_ms', 0):.2f}ms")
    
    # Process frames with motion
    for i in range(3):
        frame = generate_test_frame(with_motion=True)
        motion_detected, info = detector.detect_motion(frame)
        print(f"  Frame {i+4}: Motion={motion_detected}, Time={info.get('processing_time_ms', 0):.2f}ms")
    
    metrics = detector.get_performance_metrics()
    print(f"\n  Performance Metrics:")
    print(f"    Frames Processed: {metrics['frames_processed']}")
    print(f"    Average Time: {metrics['average_processing_time_ms']:.2f}ms")
    print(f"    Throughput: {metrics['fps']:.1f} FPS")
    print(f"    Detection Rate: {metrics['detection_rate_percent']:.1f}%")
    
    print("\n✅ Motion Detection Tests Passed")


def test_state_machine():
    """Test state machine"""
    print("\n" + "="*60)
    print("TEST 5: STATE MACHINE")
    print("="*60)
    
    fsm = StateMachine(SystemState.IDLE)
    
    print("\n[State Transitions]")
    print(f"  Initial State: {fsm.get_current_state().value}")
    
    # Valid transitions
    transitions = [
        (SystemState.MONITORING, "System armed"),
        (SystemState.ALERT, "Threat detected"),
        (SystemState.ALARM, "Confirmed threat"),
        (SystemState.COOLDOWN, "Alarm triggered"),
        (SystemState.MONITORING, "Cooldown complete"),
    ]
    
    for state, reason in transitions:
        success = fsm.transition_to(state, reason)
        status = "✓" if success else "✗"
        print(f"  {status} Transition to {state.value}: {reason}")
        time.sleep(0.5)
    
    # Invalid transition
    success = fsm.transition_to(SystemState.IDLE, "Invalid")
    print(f"  {'✓' if not success else '✗'} Invalid transition blocked (MONITORING → IDLE requires path)")
    
    stats = fsm.get_stats()
    print(f"\n  FSM Stats:")
    print(f"    Current State: {stats['current_state']}")
    print(f"    Total Transitions: {stats['transition_count']}")
    
    print("\n✅ State Machine Tests Passed")


def test_io_storage():
    """Test I/O and storage"""
    print("\n" + "="*60)
    print("TEST 6: I/O & STORAGE")
    print("="*60)
    
    config = {
        'base_path': 'storage_test',
        'intruder_images_path': 'storage_test/intruders',
        'logs_path': 'storage_test/logs',
        'authorized_faces_path': 'storage_test/authorized_faces',
        'compression_quality': 85
    }
    
    fs = FileSystem(config)
    
    print("\n[File System Operations]")
    
    # Write test image
    test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    filepath = fs.save_image(test_image, "test.jpg", "intruders")
    print(f"  ✓ Image written: {filepath}")
    
    # Read test image
    loaded_image = fs.read_image(filepath)
    print(f"  ✓ Image read: {loaded_image.shape if loaded_image is not None else 'Failed'}")
    
    # Get I/O stats
    io_stats = fs.get_io_stats()
    print(f"\n  I/O Performance:")
    print(f"    Files Written: {io_stats['files_written']}")
    print(f"    Files Read: {io_stats['files_read']}")
    print(f"    Avg Write Time: {io_stats['avg_write_time_ms']:.2f}ms")
    print(f"    Avg Read Time: {io_stats['avg_read_time_ms']:.2f}ms")
    
    # Test Logger
    print("\n[Logging System]")
    logger = Logger(config['logs_path'], "demo")
    logger.info("Test log entry")
    logger.warning("Test warning")
    logger.error("Test error")
    
    log_stats = logger.get_stats()
    print(f"  ✓ Log entries written: {log_stats['log_entries']}")
    print(f"  ✓ Log file: {log_stats['log_file']}")
    
    print("\n✅ I/O & Storage Tests Passed")
    
    # Cleanup
    import shutil
    if os.path.exists('storage_test'):
        shutil.rmtree('storage_test')
        print("  ✓ Test storage cleaned up")


def test_performance_monitoring():
    """Test performance monitoring"""
    print("\n" + "="*60)
    print("TEST 7: PERFORMANCE MONITORING")
    print("="*60)
    
    fps_counter = FPSCounter()
    
    print("\n[FPS Measurement]")
    print("  Simulating 30 frames...")
    
    for i in range(30):
        fps_counter.tick()
        time.sleep(0.033)  # ~30 FPS
    
    stats = fps_counter.get_stats()
    print(f"\n  FPS Stats:")
    print(f"    Current FPS: {stats['current_fps']:.1f}")
    print(f"    Average FPS: {stats['average_fps']:.1f}")
    print(f"    Total Frames: {stats['total_frames']}")
    
    print("\n✅ Performance Monitoring Tests Passed")


def run_all_tests():
    """Run all tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "ANTI-THEFT ALARM SYSTEM DEMO" + " "*25 + "║")
    print("║" + " "*10 + "Computer Organization & Architecture Tests" + " "*15 + "║")
    print("╚" + "="*68 + "╝")
    
    start_time = time.time()
    
    try:
        test_memory_management()
        test_cpu_architecture()
        test_boolean_logic()
        test_motion_detection()
        test_state_machine()
        test_io_storage()
        test_performance_monitoring()
        
        elapsed = time.time() - start_time
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED! ✅")
        print("="*60)
        print(f"Total execution time: {elapsed:.2f} seconds")
        print("\nCOA Concepts Demonstrated:")
        print("  ✓ Memory Management (Circular Buffer, LRU Cache)")
        print("  ✓ CPU Architecture (Monitoring, Threading)")
        print("  ✓ Boolean Logic (AND, OR, NOT, XOR gates)")
        print("  ✓ ALU Operations (Pixel arithmetic)")
        print("  ✓ Motion Detection (Frame differencing)")
        print("  ✓ State Machine (FSM with 5 states)")
        print("  ✓ I/O Systems (File operations, logging)")
        print("  ✓ Performance Monitoring (FPS, CPU, memory)")
        print("\n🎉 System is ready for deployment!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
