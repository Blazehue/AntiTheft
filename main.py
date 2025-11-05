"""
Anti-Theft Alarm System - Main Application
Integrates all COA concepts into a unified system
"""

import cv2
import json
import threading
import time
from typing import Optional
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from memory_management import CircularFrameBuffer, LRUCache, MemoryHierarchy
from cpu_architecture import Pipeline, WorkerThread, CPUMonitor
from motion_detection import MotionDetector, BooleanLogic
from face_recognition_module import FaceRecognizer
from state_machine import StateMachine, SystemState, AlarmSystem, NotificationSystem
from io_storage import FileSystem, Logger, EventRecorder
from performance_monitor import FPSCounter, PerformanceMonitor, PerformanceReport


class AntiTheftAlarmSystem:
    """
    Main Anti-Theft Alarm System
    
    Integrates all Computer Organization & Architecture concepts:
    - Memory Management (buffers, cache)
    - CPU Architecture (pipelining, threading)
    - Motion Detection (ALU operations, boolean logic)
    - Face Recognition (cache, pattern matching)
    - State Machine (FSM, control logic)
    - I/O & Storage (file system, logging)
    - Performance Monitoring (metrics, profiling)
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize the complete system
        
        Args:
            config_path: Path to configuration file
        """
        print("="*70)
        print("ANTI-THEFT ALARM SYSTEM")
        print("Computer Vision + Computer Organization & Architecture")
        print("="*70)
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize components
        self._initialize_components()
        
        # System state
        self.running = False
        self.system_armed = True
        
        print("\n✅ System initialized successfully!")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            print(f"✅ Configuration loaded from: {config_path}")
            return config
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            print("Using default configuration")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Get default configuration"""
        return {
            "camera": {"device_id": 0, "resolution": [640, 480], "fps": 30},
            "memory": {"frame_buffer_size": 30, "cache_size": 100},
            "motion_detection": {"threshold": 25, "min_contour_area": 500},
            "face_recognition": {"enabled": True, "tolerance": 0.6},
            "alarm": {"enabled": True, "duration": 5, "cooldown_period": 10},
            "storage": {"base_path": "storage"}
        }
    
    def _initialize_components(self):
        """Initialize all system components"""
        print("\n🔧 Initializing components...")
        
        # 1. Memory Management (COA: Memory Hierarchy)
        print("   📝 Memory Management...")
        memory_config = self.config.get('memory', {})
        self.frame_buffer = CircularFrameBuffer(memory_config.get('frame_buffer_size', 30))
        self.face_cache = LRUCache(memory_config.get('cache_size', 100))
        self.memory_hierarchy = MemoryHierarchy(
            l1_size=memory_config.get('frame_buffer_size', 30),
            l2_size=memory_config.get('cache_size', 100)
        )
        
        # 2. Motion Detection (COA: ALU, Boolean Logic)
        print("   🎯 Motion Detection...")
        self.motion_detector = MotionDetector(self.config.get('motion_detection', {}))
        self.boolean_logic = BooleanLogic()
        
        # 3. Face Recognition (COA: Cache Memory)
        print("   👤 Face Recognition...")
        face_config = self.config.get('face_recognition', {})
        face_config['authorized_faces_path'] = self.config.get('storage', {}).get('authorized_faces_path', 'storage/authorized_faces')
        self.face_recognizer = FaceRecognizer(face_config, self.face_cache)
        self.face_recognizer.load_authorized_faces()
        
        # 4. State Machine (COA: FSM)
        print("   ⚙️  State Machine...")
        self.state_machine = StateMachine(SystemState.IDLE)
        
        # 5. Alarm & Notification (COA: I/O Operations)
        print("   🚨 Alarm System...")
        self.alarm_system = AlarmSystem(self.config.get('alarm', {}))
        self.notification_system = NotificationSystem(self.config.get('notification', {}))
        
        # 6. File System & Logging (COA: Storage Hierarchy)
        print("   💾 Storage System...")
        self.file_system = FileSystem(self.config.get('storage', {}))
        self.logger = Logger(
            self.config.get('storage', {}).get('logs_path', 'storage/logs'),
            'system'
        )
        self.event_recorder = EventRecorder(
            self.config.get('storage', {}).get('logs_path', 'storage/logs')
        )
        
        # 7. Performance Monitoring (COA: Performance Metrics)
        print("   📊 Performance Monitor...")
        self.fps_counter = FPSCounter()
        self.perf_monitor = PerformanceMonitor()
        self.cpu_monitor = CPUMonitor()
        
        # 8. Video Capture (COA: I/O Device)
        print("   📹 Video Capture...")
        camera_config = self.config.get('camera', {})
        self.camera = cv2.VideoCapture(camera_config.get('device_id', 0))
        
        if not self.camera.isOpened():
            print("   ⚠️  Warning: Camera not available, using test mode")
            self.camera = None
        else:
            # Set camera properties
            width, height = camera_config.get('resolution', [640, 480])
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.camera.set(cv2.CAP_PROP_FPS, camera_config.get('fps', 30))
        
        # Threading (COA: Parallel Processing)
        self.processing_thread = None
        self.display_thread = None
        
        # Store detection results for display
        self.last_face_names = []
        self.last_face_locations = []
        
        self.logger.info("System components initialized")
    
    def start(self):
        """
        Start the alarm system
        
        COA Concept: System boot and initialization
        """
        if self.running:
            print("⚠️  System already running")
            return
        
        print("\n🚀 Starting Anti-Theft Alarm System...")
        
        self.running = True
        
        # Transition to MONITORING state
        self.state_machine.transition_to(SystemState.MONITORING, "System started")
        
        # Start performance monitoring
        self.perf_monitor.start_monitoring(interval=5.0)
        
        # Start processing
        self.logger.info("System started")
        self.event_recorder.record_event("SYSTEM", "System started", {})
        
        # Main loop
        self._main_loop()
    
    def _main_loop(self):
        """
        Main system loop
        
        COA Concept: Fetch-Execute cycle
        """
        print("\n▶️  System running. Press 'q' to quit, 's' to toggle arm/disarm")
        print(f"   System Armed: {self.system_armed}")
        
        try:
            while self.running:
                # FETCH: Capture frame from camera (I/O operation)
                frame = self._capture_frame()
                
                if frame is None:
                    continue
                
                # Store in frame buffer (Memory write)
                self.frame_buffer.write(frame)
                
                # DECODE & EXECUTE: Process frame
                self._process_frame(frame)
                
                # Update FPS counter
                self.fps_counter.tick()
                
                # Record CPU/Memory usage periodically
                if self.fps_counter.frame_count % 30 == 0:
                    self.cpu_monitor.record_usage()
                
                # Display frame
                display_frame = self._create_display_frame(frame)
                cv2.imshow('Anti-Theft Alarm System', display_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\n🛑 Shutdown requested by user")
                    break
                elif key == ord('s'):
                    self.system_armed = not self.system_armed
                    status = "ARMED" if self.system_armed else "DISARMED"
                    print(f"\n🔧 System {status}")
                    self.logger.info(f"System {status}")
                    self.event_recorder.record_event("SYSTEM", f"System {status}", {})
                
        except KeyboardInterrupt:
            print("\n🛑 Shutdown requested (Ctrl+C)")
        except Exception as e:
            print(f"\n❌ Error in main loop: {e}")
            self.logger.error(f"Main loop error: {e}")
        finally:
            self.stop()
    
    def _capture_frame(self) -> Optional:
        """
        Capture frame from camera
        
        COA Concept: I/O read operation (polling)
        """
        if self.camera is None:
            # Test mode - generate dummy frame
            import numpy as np
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            time.sleep(0.033)  # ~30 FPS
            return frame
        
        ret, frame = self.camera.read()
        if not ret:
            return None
        
        return frame
    
    def _process_frame(self, frame):
        """
        Process frame through detection pipeline
        
        COA Concept: Instruction pipeline (Fetch-Decode-Execute-Writeback)
        """
        # Stage 1: Motion Detection (ALU operations)
        motion_detected, motion_info = self.motion_detector.detect_motion(frame)
        
        # Stage 2: Face Recognition (Cache lookup)
        face_names, face_locations = self.face_recognizer.recognize_faces(frame)
        
        # Store for display
        self.last_face_names = face_names
        self.last_face_locations = face_locations
        
        unknown_face = self.face_recognizer.is_unknown_face_detected(face_names)
        
        # Stage 3: Decision Logic (Boolean operations)
        # Alarm = (MotionDetected OR UnknownFace) AND SystemArmed
        alarm_trigger = self.boolean_logic.alarm_condition(
            motion_detected,
            unknown_face,
            self.system_armed
        )
        
        # Stage 4: State Management & Actions
        self._handle_detection(alarm_trigger, motion_detected, unknown_face, frame)
    
    def _handle_detection(self, alarm_trigger: bool, motion_detected: bool, unknown_face: bool, frame):
        """
        Handle detection results and trigger actions
        
        COA Concept: Control flow and state transitions
        """
        current_state = self.state_machine.get_current_state()
        
        if alarm_trigger:
            # Threat detected
            if current_state == SystemState.MONITORING:
                # Transition to ALERT
                self.state_machine.transition_to(SystemState.ALERT, "Threat detected")
                self.logger.warning("Threat detected - entering ALERT state")
                self.event_recorder.record_event("ALERT", "Potential threat", {
                    'motion': motion_detected,
                    'unknown_face': unknown_face
                })
            
            elif current_state == SystemState.ALERT:
                # If in alert for more than 2 seconds, trigger alarm
                if self.state_machine.get_time_in_state() > 2.0:
                    self.state_machine.transition_to(SystemState.ALARM, "Confirmed threat")
                    self._trigger_alarm(frame, motion_detected, unknown_face)
        
        else:
            # No threat
            if current_state == SystemState.ALERT:
                # False alarm - return to monitoring
                self.state_machine.transition_to(SystemState.MONITORING, "False alarm")
                self.logger.info("False alarm - returning to MONITORING")
            
            elif current_state == SystemState.COOLDOWN:
                # Check if cooldown period expired
                if self.state_machine.get_time_in_state() > self.alarm_system.cooldown_period:
                    self.state_machine.transition_to(SystemState.MONITORING, "Cooldown expired")
                    self.logger.info("Cooldown complete - MONITORING resumed")
    
    def _trigger_alarm(self, frame, motion_detected: bool, unknown_face: bool):
        """
        Trigger alarm and notifications
        
        COA Concept: I/O operations (output devices, network)
        """
        print("\n" + "!"*70)
        print("🚨 ALARM TRIGGERED - INTRUDER DETECTED!")
        print("!"*70)
        
        # Activate alarm (speaker output)
        self.alarm_system.trigger()
        
        # Save intruder image (disk write)
        image_path = self.file_system.save_image(frame, "intruder.jpg", "intruders")
        
        # Log event
        self.logger.error("ALARM: Intruder detected", {
            'motion': motion_detected,
            'unknown_face': unknown_face,
            'image': image_path
        })
        
        self.event_recorder.record_event("ALARM", "Intruder detected", {
            'motion_detected': motion_detected,
            'unknown_face_detected': unknown_face,
            'image_path': image_path
        })
        
        # Send notifications (network I/O)
        if image_path:
            self.notification_system.send_email_alert(
                subject="🚨 ALARM: Intruder Detected!",
                body=f"Anti-Theft Alarm System detected an intruder.\n\nMotion: {motion_detected}\nUnknown Face: {unknown_face}",
                image_path=image_path
            )
        
        # Transition to cooldown
        self.state_machine.transition_to(SystemState.COOLDOWN, "Alarm triggered")
    
    def _create_display_frame(self, frame):
        """
        Create display frame with overlays
        
        COA Concept: Output rendering
        """
        display = frame.copy()
        
        # Draw face detection boxes
        if len(self.last_face_locations) > 0:
            for i, location in enumerate(self.last_face_locations):
                # location format: (top, right, bottom, left)
                top, right, bottom, left = location
                
                # Determine color based on detection status
                name = self.last_face_names[i] if i < len(self.last_face_names) else "Unknown"
                if name == "Detected":
                    color = (255, 255, 0)  # Cyan for detected faces
                    label = "Face Detected"
                elif name == "Unknown":
                    color = (0, 0, 255)  # Red for unknown faces
                    label = f"Unknown"
                else:
                    color = (0, 255, 0)  # Green for authorized faces
                    label = f"Authorized: {name}"
                
                # Draw rectangle around face
                cv2.rectangle(display, (left, top), (right, bottom), color, 2)
                
                # Draw label background
                cv2.rectangle(display, (left, bottom - 25), (right, bottom), color, cv2.FILLED)
                
                # Draw label text
                cv2.putText(display, label, (left + 6, bottom - 6),
                           cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
        
        # Add system info overlay
        info_y = 30
        line_height = 25
        
        # System state
        state = self.state_machine.get_current_state().value
        state_color = self._get_state_color(state)
        cv2.putText(display, f"State: {state}", (10, info_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, state_color, 2)
        info_y += line_height
        
        # Armed status
        armed_text = "ARMED" if self.system_armed else "DISARMED"
        armed_color = (0, 0, 255) if self.system_armed else (128, 128, 128)
        cv2.putText(display, f"Status: {armed_text}", (10, info_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, armed_color, 2)
        info_y += line_height
        
        # FPS
        fps = self.fps_counter.get_fps()
        cv2.putText(display, f"FPS: {fps:.1f}", (10, info_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        info_y += line_height
        
        # Face detection count
        face_count = len(self.last_face_locations)
        face_color = (255, 255, 0) if face_count > 0 else (128, 128, 128)
        cv2.putText(display, f"Faces: {face_count}", (10, info_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, face_color, 2)
        
        return display
    
    def _get_state_color(self, state: str) -> tuple:
        """Get color for state display"""
        colors = {
            'IDLE': (128, 128, 128),
            'MONITORING': (0, 255, 0),
            'ALERT': (0, 165, 255),
            'ALARM': (0, 0, 255),
            'COOLDOWN': (255, 165, 0)
        }
        return colors.get(state, (255, 255, 255))
    
    def stop(self):
        """
        Stop the alarm system
        
        COA Concept: System shutdown
        """
        if not self.running:
            return
        
        print("\n🛑 Stopping system...")
        self.running = False
        
        # Stop components
        self.perf_monitor.stop_monitoring()
        
        if self.camera:
            self.camera.release()
        
        cv2.destroyAllWindows()
        
        # Generate final performance report
        self._generate_final_report()
        
        # Transition to IDLE
        self.state_machine.transition_to(SystemState.IDLE, "System stopped")
        
        self.logger.info("System stopped")
        self.event_recorder.record_event("SYSTEM", "System stopped", {})
        
        print("✅ System stopped successfully")
    
    def _generate_final_report(self):
        """Generate and save final performance report"""
        print("\n📊 Generating performance report...")
        
        report = PerformanceReport.generate_report(
            fps_stats=self.fps_counter.get_stats(),
            monitor_stats=self.perf_monitor.get_average_metrics(),
            memory_stats=self.memory_hierarchy.get_memory_stats(),
            pipeline_stats={'average_latency_ms': 0, 'cpi': 0},  # Simplified
            motion_stats=self.motion_detector.get_performance_metrics(),
            face_stats=self.face_recognizer.get_performance_metrics(),
            io_stats=self.file_system.get_io_stats()
        )
        
        # Save report
        report_path = os.path.join(
            self.config.get('storage', {}).get('logs_path', 'storage/logs'),
            f"performance_report_{int(time.time())}.json"
        )
        PerformanceReport.save_report(report, report_path)
        
        # Print summary
        PerformanceReport.print_report_summary(report)


def main():
    """Main entry point"""
    # Create system instance
    system = AntiTheftAlarmSystem(config_path="config.json")
    
    # Start system
    system.start()


if __name__ == "__main__":
    main()
