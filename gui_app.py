"""
Anti-Theft Alarm System - Modern GUI Application
Advanced interface with camera panel, controls, status indicators, and real-time monitoring
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import cv2
from PIL import Image, ImageTk
import threading
import time
import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from memory_management import CircularFrameBuffer, LRUCache
from motion_detection import MotionDetector
from state_machine import SystemState
from face_recognition_module import FaceRecognizer


class AntiTheftGUI:
    """Main GUI Application with Camera Panel"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ Anti-Theft Alarm System - Security Monitor")
        self.root.geometry("1600x900")
        self.root.configure(bg="#1a1a2e")
        
        # System state
        self.camera = None
        self.is_running = False
        self.is_armed = False
        self.current_state = SystemState.IDLE
        self.current_frame = None
        
        # Components
        self.motion_detector = MotionDetector({
            'threshold': 25,
            'min_contour_area': 500,
            'blur_kernel_size': 21
        })
        self.frame_buffer = CircularFrameBuffer(30)
        
        # Face recognition setup
        self.lru_cache = LRUCache(capacity=100)
        self.face_recognizer = FaceRecognizer(
            config={
                'tolerance': 0.6,
                'model': 'hog',
                'detection_interval': 1,
                'authorized_faces_path': 'storage/face_database/authorized_faces'
            },
            cache=self.lru_cache
        )
        # Load authorized faces
        self.face_recognizer.load_authorized_faces()
        
        # Track face detection results
        self.last_face_names = []
        self.last_face_locations = []
        
        # Statistics
        self.stats = {
            'fps': 0,
            'detections': 0,
            'alarms': 0,
            'uptime': 0
        }
        self.start_time = time.time()
        
        # Setup GUI
        self.setup_styles()
        self.create_layout()
        
        # Start updates
        self.update_camera()
        self.update_stats()
        
        # Handle close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Configure visual styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colors
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'bg_light': '#0f3460',
            'accent': '#e94560',
            'success': '#00d9ff',
            'warning': '#ffa500',
            'danger': '#ff0000',
            'text': '#ffffff',
            'text_dim': '#8892b0'
        }
        
        # Configure styles
        style.configure("Dark.TFrame", background=self.colors['bg_dark'])
        style.configure("Medium.TFrame", background=self.colors['bg_medium'])
        style.configure("Light.TFrame", background=self.colors['bg_light'])
        
        style.configure("Title.TLabel",
                       background=self.colors['bg_dark'],
                       foreground=self.colors['text'],
                       font=("Consolas", 18, "bold"))
        
        style.configure("Info.TLabel",
                       background=self.colors['bg_medium'],
                       foreground=self.colors['text'],
                       font=("Consolas", 10))
        
        style.configure("Stat.TLabel",
                       background=self.colors['bg_light'],
                       foreground=self.colors['success'],
                       font=("Consolas", 14, "bold"))
    
    def create_layout(self):
        """Create main application layout"""
        # Top bar
        self.create_top_bar()
        
        # Main content area
        content = ttk.Frame(self.root, style="Dark.TFrame")
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Left: Camera + Controls (70%)
        left_panel = ttk.Frame(content, style="Medium.TFrame")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.create_camera_panel(left_panel)
        self.create_control_panel(left_panel)
        
        # Right: Status + Logs (30%)
        right_panel = ttk.Frame(content, style="Medium.TFrame")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_panel.config(width=400)
        
        self.create_status_panel(right_panel)
        self.create_log_panel(right_panel)
    
    def create_top_bar(self):
        """Create top status bar"""
        top_bar = tk.Frame(self.root, bg=self.colors['bg_light'], height=60)
        top_bar.pack(fill=tk.X, padx=10, pady=10)
        top_bar.pack_propagate(False)
        
        # Logo/Title
        title = tk.Label(top_bar, text="🛡️ ANTI-THEFT SECURITY SYSTEM",
                        bg=self.colors['bg_light'],
                        fg=self.colors['text'],
                        font=("Consolas", 20, "bold"))
        title.pack(side=tk.LEFT, padx=20)
        
        # System time
        self.time_label = tk.Label(top_bar, text="",
                                   bg=self.colors['bg_light'],
                                   fg=self.colors['text_dim'],
                                   font=("Consolas", 12))
        self.time_label.pack(side=tk.RIGHT, padx=20)
        self.update_time()
    
    def create_camera_panel(self, parent):
        """Create camera display panel with overlays"""
        camera_frame = ttk.Frame(parent, style="Light.TFrame")
        camera_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header with status
        header = tk.Frame(camera_frame, bg=self.colors['bg_light'], height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="📹 LIVE FEED",
                bg=self.colors['bg_light'],
                fg=self.colors['text'],
                font=("Consolas", 14, "bold")).pack(side=tk.LEFT, padx=15)
        
        # State indicator
        self.state_indicator = tk.Label(header, text="● OFFLINE",
                                       bg=self.colors['bg_light'],
                                       fg=self.colors['text_dim'],
                                       font=("Consolas", 12, "bold"))
        self.state_indicator.pack(side=tk.RIGHT, padx=15)
        
        # Camera canvas
        self.camera_canvas = tk.Canvas(camera_frame,
                                       bg="#000000",
                                       highlightthickness=2,
                                       highlightbackground=self.colors['accent'])
        self.camera_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Overlay info frame (transparent overlay)
        self.overlay_frame = tk.Frame(camera_frame, bg=self.colors['bg_dark'])
        self.overlay_frame.place(relx=0.02, rely=0.02, relwidth=0.25, relheight=0.25)
        
        # Overlay stats
        tk.Label(self.overlay_frame, text="SYSTEM STATUS",
                bg=self.colors['bg_dark'], fg=self.colors['success'],
                font=("Consolas", 10, "bold")).pack(anchor="w", padx=5, pady=2)
        
        self.overlay_fps = tk.Label(self.overlay_frame, text="FPS: 0",
                                    bg=self.colors['bg_dark'], fg=self.colors['text'],
                                    font=("Consolas", 9))
        self.overlay_fps.pack(anchor="w", padx=5)
        
        self.overlay_motion = tk.Label(self.overlay_frame, text="Motion: NO",
                                      bg=self.colors['bg_dark'], fg=self.colors['text'],
                                      font=("Consolas", 9))
        self.overlay_motion.pack(anchor="w", padx=5)
        
        self.overlay_faces = tk.Label(self.overlay_frame, text="Faces: 0",
                                     bg=self.colors['bg_dark'], fg=self.colors['text'],
                                     font=("Consolas", 9))
        self.overlay_faces.pack(anchor="w", padx=5)
    
    def create_control_panel(self, parent):
        """Create control buttons panel"""
        control_frame = tk.Frame(parent, bg=self.colors['bg_medium'], height=100)
        control_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        control_frame.pack_propagate(False)
        
        # Button container
        btn_container = tk.Frame(control_frame, bg=self.colors['bg_medium'])
        btn_container.pack(expand=True)
        
        # Start/Stop button
        self.start_btn = tk.Button(btn_container, text="▶ START SYSTEM",
                                   command=self.toggle_system,
                                   bg=self.colors['success'], fg=self.colors['text'],
                                   font=("Consolas", 12, "bold"),
                                   width=15, height=2,
                                   relief=tk.FLAT, cursor="hand2")
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        # Arm/Disarm button
        self.arm_btn = tk.Button(btn_container, text="🛡️ ARM SYSTEM",
                                command=self.toggle_arm,
                                bg=self.colors['warning'], fg=self.colors['text'],
                                font=("Consolas", 12, "bold"),
                                width=15, height=2,
                                relief=tk.FLAT, cursor="hand2",
                                state=tk.DISABLED)
        self.arm_btn.pack(side=tk.LEFT, padx=10)
        
        # Snapshot button
        self.snapshot_btn = tk.Button(btn_container, text="📸 SNAPSHOT",
                                     command=self.take_snapshot,
                                     bg=self.colors['bg_light'], fg=self.colors['text'],
                                     font=("Consolas", 12, "bold"),
                                     width=15, height=2,
                                     relief=tk.FLAT, cursor="hand2",
                                     state=tk.DISABLED)
        self.snapshot_btn.pack(side=tk.LEFT, padx=10)
        
        # Settings button
        settings_btn = tk.Button(btn_container, text="⚙️ SETTINGS",
                                command=self.open_settings,
                                bg=self.colors['bg_light'], fg=self.colors['text'],
                                font=("Consolas", 12, "bold"),
                                width=15, height=2,
                                relief=tk.FLAT, cursor="hand2")
        settings_btn.pack(side=tk.LEFT, padx=10)
    
    def create_status_panel(self, parent):
        """Create status monitoring panel"""
        status_frame = tk.LabelFrame(parent, text="📊 SYSTEM STATUS",
                                    bg=self.colors['bg_medium'],
                                    fg=self.colors['text'],
                                    font=("Consolas", 12, "bold"),
                                    relief=tk.GROOVE, bd=2)
        status_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # Stats container
        stats_container = tk.Frame(status_frame, bg=self.colors['bg_medium'])
        stats_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # FPS
        self.create_stat_row(stats_container, "FPS:", "fps_value", 0)
        
        # Uptime
        self.create_stat_row(stats_container, "Uptime:", "uptime_value", 1)
        
        # Detections
        self.create_stat_row(stats_container, "Detections:", "detection_value", 2)
        
        # Faces detected
        self.create_stat_row(stats_container, "Faces Now:", "faces_value", 3)
        
        # Alarms
        self.create_stat_row(stats_container, "Alarms:", "alarm_value", 4)
        
        # Separator
        tk.Frame(stats_container, bg=self.colors['accent'], height=2).pack(fill=tk.X, pady=10)
        
        # Armed status
        armed_frame = tk.Frame(stats_container, bg=self.colors['bg_medium'])
        armed_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(armed_frame, text="Armed Status:",
                bg=self.colors['bg_medium'], fg=self.colors['text'],
                font=("Consolas", 11)).pack(side=tk.LEFT)
        
        self.armed_status = tk.Label(armed_frame, text="DISARMED",
                                     bg=self.colors['bg_medium'],
                                     fg=self.colors['text_dim'],
                                     font=("Consolas", 11, "bold"))
        self.armed_status.pack(side=tk.RIGHT)
        
        # Current state
        state_frame = tk.Frame(stats_container, bg=self.colors['bg_medium'])
        state_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(state_frame, text="Current State:",
                bg=self.colors['bg_medium'], fg=self.colors['text'],
                font=("Consolas", 11)).pack(side=tk.LEFT)
        
        self.state_status = tk.Label(state_frame, text="IDLE",
                                     bg=self.colors['bg_medium'],
                                     fg=self.colors['text_dim'],
                                     font=("Consolas", 11, "bold"))
        self.state_status.pack(side=tk.RIGHT)
    
    def create_stat_row(self, parent, label_text, value_attr, row):
        """Create a statistics row"""
        row_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        row_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(row_frame, text=label_text,
                bg=self.colors['bg_medium'], fg=self.colors['text'],
                font=("Consolas", 11)).pack(side=tk.LEFT)
        
        value_label = tk.Label(row_frame, text="0",
                              bg=self.colors['bg_medium'],
                              fg=self.colors['success'],
                              font=("Consolas", 11, "bold"))
        value_label.pack(side=tk.RIGHT)
        
        setattr(self, value_attr, value_label)
    
    def create_log_panel(self, parent):
        """Create event log panel"""
        log_frame = tk.LabelFrame(parent, text="📋 EVENT LOG",
                                 bg=self.colors['bg_medium'],
                                 fg=self.colors['text'],
                                 font=("Consolas", 12, "bold"),
                                 relief=tk.GROOVE, bd=2)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Log text area with scrollbar
        log_container = tk.Frame(log_frame, bg=self.colors['bg_medium'])
        log_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(log_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_container,
                               bg="#000000", fg=self.colors['success'],
                               font=("Consolas", 9),
                               yscrollcommand=scrollbar.set,
                               height=15,
                               relief=tk.FLAT)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Clear log button
        clear_btn = tk.Button(log_frame, text="Clear Log",
                             command=self.clear_log,
                             bg=self.colors['bg_light'], fg=self.colors['text'],
                             font=("Consolas", 9), relief=tk.FLAT, cursor="hand2")
        clear_btn.pack(pady=5)
        
        # Initial log
        self.log_event("System initialized", "INFO")
    
    def update_camera(self):
        """Update camera feed"""
        if self.is_running and self.camera is not None:
            ret, frame = self.camera.read()
            
            if ret:
                self.current_frame = frame.copy()
                
                # Process frame - Motion Detection
                motion_detected, info = self.motion_detector.detect_motion(frame)
                
                if motion_detected:
                    self.stats['detections'] += 1
                    self.overlay_motion.config(text="Motion: YES", fg=self.colors['danger'])
                    
                    # Draw contours
                    if 'contours' in info:
                        cv2.drawContours(frame, info['contours'], -1, (0, 255, 0), 2)
                    
                    if self.is_armed:
                        self.log_event(f"Motion detected! Area: {info.get('largest_area', 0)}", "ALERT")
                else:
                    self.overlay_motion.config(text="Motion: NO", fg=self.colors['text'])
                
                # Process frame - Face Recognition
                face_names, face_locations = self.face_recognizer.recognize_faces(frame)
                self.last_face_names = face_names
                self.last_face_locations = face_locations
                
                # Draw face detection boxes
                face_count = len(face_locations)
                if face_count > 0:
                    self.overlay_faces.config(text=f"Faces: {face_count}", fg=self.colors['success'])
                    
                    for i, location in enumerate(face_locations):
                        # location format: (top, right, bottom, left)
                        top, right, bottom, left = location
                        
                        # Determine color and label
                        name = face_names[i] if i < len(face_names) else "Unknown"
                        if name == "Detected":
                            color = (255, 255, 0)  # Cyan for detected faces
                            label = "Face Detected"
                        elif name == "Unknown":
                            color = (0, 0, 255)  # Red for unknown faces
                            label = "Unknown"
                        else:
                            color = (0, 255, 0)  # Green for authorized faces
                            label = f"Auth: {name}"
                        
                        # Draw rectangle around face
                        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                        
                        # Draw label background
                        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), color, cv2.FILLED)
                        
                        # Draw label text
                        cv2.putText(frame, label, (left + 6, bottom - 6),
                                   cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                    
                    # Log unknown faces
                    unknown_count = face_names.count("Unknown") + face_names.count("Detected")
                    if unknown_count > 0 and self.is_armed:
                        self.log_event(f"Unknown face detected! Count: {unknown_count}", "WARNING")
                else:
                    self.overlay_faces.config(text="Faces: 0", fg=self.colors['text_dim'])
                
                # Add timestamp overlay
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cv2.putText(frame, timestamp, (10, frame.shape[0] - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                
                # Add armed indicator
                if self.is_armed:
                    cv2.putText(frame, "ARMED", (frame.shape[1] - 100, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                # Convert and display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                
                # Resize to fit canvas
                canvas_width = self.camera_canvas.winfo_width()
                canvas_height = self.camera_canvas.winfo_height()
                
                if canvas_width > 1 and canvas_height > 1:
                    img = img.resize((canvas_width - 4, canvas_height - 4), Image.Resampling.LANCZOS)
                    img_tk = ImageTk.PhotoImage(image=img)
                    
                    self.camera_canvas.delete("all")
                    self.camera_canvas.create_image(2, 2, anchor=tk.NW, image=img_tk)
                    self.camera_canvas.image = img_tk
        
        elif self.is_running and self.camera is None:
            # Show "No Camera" message
            self.camera_canvas.delete("all")
            self.camera_canvas.create_text(
                self.camera_canvas.winfo_width() // 2,
                self.camera_canvas.winfo_height() // 2,
                text="NO CAMERA DETECTED\nCheck device connection",
                fill=self.colors['danger'], font=("Consolas", 16, "bold")
            )
        
        # Schedule next update
        self.root.after(33, self.update_camera)  # ~30 FPS
    
    def update_stats(self):
        """Update statistics display"""
        if self.is_running:
            # Calculate uptime
            uptime_seconds = int(time.time() - self.start_time)
            hours = uptime_seconds // 3600
            minutes = (uptime_seconds % 3600) // 60
            seconds = uptime_seconds % 60
            uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            # Update stats
            self.uptime_value.config(text=uptime_str)
            self.detection_value.config(text=str(self.stats['detections']))
            self.alarm_value.config(text=str(self.stats['alarms']))
            
            # Update face count
            face_count = len(self.last_face_locations)
            self.faces_value.config(text=str(face_count))
            if face_count > 0:
                self.faces_value.config(fg=self.colors['success'])
            else:
                self.faces_value.config(fg=self.colors['text_dim'])
            
            # Calculate FPS
            if hasattr(self, 'frame_count'):
                elapsed = time.time() - self.start_time
                fps = self.frame_count / elapsed if elapsed > 0 else 0
                self.fps_value.config(text=f"{fps:.1f}")
                self.overlay_fps.config(text=f"FPS: {fps:.1f}")
            
            self.frame_count = getattr(self, 'frame_count', 0) + 1
        
        self.root.after(1000, self.update_stats)  # Update every second
    
    def update_time(self):
        """Update system time"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def toggle_system(self):
        """Start/Stop system"""
        if not self.is_running:
            # Start system
            self.camera = cv2.VideoCapture(0)
            
            if not self.camera.isOpened():
                messagebox.showerror("Error", "Cannot access camera!")
                self.camera = None
                return
            
            self.is_running = True
            self.start_time = time.time()
            self.frame_count = 0
            
            self.start_btn.config(text="⏸ STOP SYSTEM", bg=self.colors['danger'])
            self.arm_btn.config(state=tk.NORMAL)
            self.snapshot_btn.config(state=tk.NORMAL)
            self.state_indicator.config(text="● ONLINE", fg=self.colors['success'])
            
            self.log_event("System started - Camera active", "INFO")
        
        else:
            # Stop system
            self.is_running = False
            self.is_armed = False
            
            if self.camera:
                self.camera.release()
                self.camera = None
            
            self.start_btn.config(text="▶ START SYSTEM", bg=self.colors['success'])
            self.arm_btn.config(text="🛡️ ARM SYSTEM", bg=self.colors['warning'], state=tk.DISABLED)
            self.snapshot_btn.config(state=tk.DISABLED)
            self.state_indicator.config(text="● OFFLINE", fg=self.colors['text_dim'])
            self.armed_status.config(text="DISARMED", fg=self.colors['text_dim'])
            
            self.log_event("System stopped", "INFO")
    
    def toggle_arm(self):
        """Arm/Disarm system"""
        if not self.is_armed:
            self.is_armed = True
            self.arm_btn.config(text="🔓 DISARM", bg=self.colors['danger'])
            self.armed_status.config(text="ARMED", fg=self.colors['danger'])
            self.log_event("System ARMED - Alarm active", "WARNING")
        else:
            self.is_armed = False
            self.arm_btn.config(text="🛡️ ARM SYSTEM", bg=self.colors['warning'])
            self.armed_status.config(text="DISARMED", fg=self.colors['text_dim'])
            self.log_event("System DISARMED", "INFO")
    
    def take_snapshot(self):
        """Save current frame"""
        if self.current_frame is not None:
            os.makedirs("storage/snapshots", exist_ok=True)
            filename = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            filepath = os.path.join("storage/snapshots", filename)
            cv2.imwrite(filepath, self.current_frame)
            self.log_event(f"Snapshot saved: {filename}", "INFO")
            messagebox.showinfo("Success", f"Snapshot saved!\n{filepath}")
    
    def open_settings(self):
        """Open settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg=self.colors['bg_medium'])
        
        tk.Label(settings_window, text="⚙️ Settings",
                bg=self.colors['bg_medium'], fg=self.colors['text'],
                font=("Consolas", 14, "bold")).pack(pady=20)
        
        tk.Label(settings_window, text="Motion Sensitivity: 25",
                bg=self.colors['bg_medium'], fg=self.colors['text'],
                font=("Consolas", 10)).pack(pady=10)
        
        tk.Label(settings_window, text="More settings coming soon...",
                bg=self.colors['bg_medium'], fg=self.colors['text_dim'],
                font=("Consolas", 10)).pack(pady=10)
        
        tk.Button(settings_window, text="Close",
                 command=settings_window.destroy,
                 bg=self.colors['accent'], fg=self.colors['text'],
                 font=("Consolas", 10, "bold")).pack(pady=20)
    
    def log_event(self, message, level="INFO"):
        """Add event to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color based on level
        colors = {
            "INFO": self.colors['success'],
            "WARNING": self.colors['warning'],
            "ALERT": self.colors['danger'],
            "ERROR": self.colors['danger']
        }
        
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Limit log size
        if float(self.log_text.index('end-1c').split('.')[0]) > 1000:
            self.log_text.delete('1.0', '100.0')
    
    def clear_log(self):
        """Clear event log"""
        self.log_text.delete('1.0', tk.END)
        self.log_event("Log cleared", "INFO")
    
    def on_closing(self):
        """Handle window close"""
        if self.is_running:
            if messagebox.askokcancel("Quit", "System is running. Stop and quit?"):
                self.toggle_system()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = AntiTheftGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
