"""
State Machine and Alert System
Demonstrates COA concepts: State Machines, Control Flow, I/O Operations

COA Concepts Implemented:
- Finite State Machine (FSM)
- State transition logic
- I/O operations (alarm, notifications)
- Control flow management
"""

import threading
import time
from enum import Enum
from typing import Optional, Callable
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from datetime import datetime


class SystemState(Enum):
    """
    System States for Finite State Machine
    
    COA Concept: State encoding in digital systems
    Each state represents a unique system condition
    """
    IDLE = "IDLE"  # System inactive, not monitoring
    MONITORING = "MONITORING"  # Active surveillance, no threats
    ALERT = "ALERT"  # Potential threat detected, evaluating
    ALARM = "ALARM"  # Confirmed threat, alarm triggered
    COOLDOWN = "COOLDOWN"  # Post-alarm cooldown period


class StateTransition:
    """
    State Transition Definition
    
    COA Concept: State transition table
    Defines valid transitions between states
    """
    
    # Valid state transitions (from_state -> to_state)
    VALID_TRANSITIONS = {
        SystemState.IDLE: [SystemState.MONITORING],
        SystemState.MONITORING: [SystemState.ALERT, SystemState.IDLE],
        SystemState.ALERT: [SystemState.ALARM, SystemState.MONITORING],
        SystemState.ALARM: [SystemState.COOLDOWN],
        SystemState.COOLDOWN: [SystemState.MONITORING, SystemState.IDLE]
    }
    
    @staticmethod
    def is_valid_transition(from_state: SystemState, to_state: SystemState) -> bool:
        """
        Check if state transition is valid
        
        COA Concept: State transition validation logic
        """
        if from_state not in StateTransition.VALID_TRANSITIONS:
            return False
        return to_state in StateTransition.VALID_TRANSITIONS[from_state]


class StateMachine:
    """
    Finite State Machine Implementation
    
    COA Concepts:
    - State register (current state storage)
    - State transition logic (combinational logic)
    - State history tracking
    """
    
    def __init__(self, initial_state: SystemState = SystemState.IDLE):
        """
        Initialize state machine
        
        Args:
            initial_state: Starting state
        """
        self.current_state = initial_state
        self.previous_state = None
        self.state_enter_time = time.time()
        
        # State history
        self.state_history = []
        self.transition_count = 0
        
        # Thread safety
        self.lock = threading.Lock()
        
        # State callbacks
        self.state_callbacks = {}
        
        # Record initial state
        self._record_state_entry(initial_state)
    
    def transition_to(self, new_state: SystemState, reason: str = "") -> bool:
        """
        Transition to new state
        
        COA Concept: State transition with validation
        Implements state transition logic circuit
        
        Returns:
            True if transition successful, False otherwise
        """
        with self.lock:
            # Validate transition
            if not StateTransition.is_valid_transition(self.current_state, new_state):
                print(f"Invalid transition: {self.current_state.value} -> {new_state.value}")
                return False
            
            # Perform transition
            self.previous_state = self.current_state
            self.current_state = new_state
            self.transition_count += 1
            
            # Record state entry
            self._record_state_entry(new_state, reason)
            
            # Execute state callback
            if new_state in self.state_callbacks:
                self.state_callbacks[new_state]()
            
            print(f"State transition: {self.previous_state.value} -> {new_state.value} ({reason})")
            
            return True
    
    def register_callback(self, state: SystemState, callback: Callable):
        """Register callback function for state entry"""
        self.state_callbacks[state] = callback
    
    def get_current_state(self) -> SystemState:
        """Get current state (read state register)"""
        with self.lock:
            return self.current_state
    
    def get_time_in_state(self) -> float:
        """Get time elapsed in current state"""
        with self.lock:
            return time.time() - self.state_enter_time
    
    def _record_state_entry(self, state: SystemState, reason: str = ""):
        """Record state entry in history"""
        entry = {
            'state': state.value,
            'timestamp': time.time(),
            'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'reason': reason
        }
        self.state_history.append(entry)
        self.state_enter_time = time.time()
    
    def get_state_history(self) -> list:
        """Get state transition history"""
        with self.lock:
            return self.state_history.copy()
    
    def get_stats(self) -> dict:
        """Get state machine statistics"""
        with self.lock:
            return {
                'current_state': self.current_state.value,
                'time_in_state_s': self.get_time_in_state(),
                'transition_count': self.transition_count,
                'state_history_length': len(self.state_history)
            }


class AlarmSystem:
    """
    Alarm System with Audio Output
    
    COA Concepts:
    - I/O device control (speaker)
    - Interrupt-driven I/O simulation
    - Device state management
    """
    
    def __init__(self, config: dict):
        """
        Initialize alarm system
        
        Args:
            config: Configuration dictionary
        """
        self.enabled = config.get('enabled', True)
        self.sound_file = config.get('sound_file', None)
        self.duration = config.get('duration', 5)
        self.cooldown_period = config.get('cooldown_period', 10)
        
        self.is_active = False
        self.last_trigger_time = 0
        self.trigger_count = 0
        
        self.lock = threading.Lock()
        
        # Initialize pygame for audio
        if self.enabled:
            try:
                import pygame
                pygame.mixer.init()
                self.audio_available = True
                self.pygame = pygame
            except:
                print("Audio not available (pygame not installed), alarm will be silent")
                self.audio_available = False
                self.pygame = None
        else:
            self.audio_available = False
            self.pygame = None
    
    def can_trigger(self) -> bool:
        """
        Check if alarm can be triggered
        
        COA Concept: Cooldown timer (temporal logic)
        """
        with self.lock:
            if not self.enabled:
                return False
            
            current_time = time.time()
            time_since_last = current_time - self.last_trigger_time
            
            return time_since_last >= self.cooldown_period
    
    def trigger(self):
        """
        Trigger alarm
        
        COA Concept: I/O operation (output to speaker)
        """
        if not self.can_trigger():
            print("Alarm in cooldown period")
            return
        
        with self.lock:
            self.is_active = True
            self.last_trigger_time = time.time()
            self.trigger_count += 1
        
        print("🚨 ALARM TRIGGERED! 🚨")
        
        # Play alarm sound in separate thread
        if self.audio_available and self.sound_file and os.path.exists(self.sound_file):
            alarm_thread = threading.Thread(target=self._play_alarm, daemon=True)
            alarm_thread.start()
        else:
            # Generate beep sound programmatically
            alarm_thread = threading.Thread(target=self._generate_beep, daemon=True)
            alarm_thread.start()
    
    def _play_alarm(self):
        """Play alarm sound from file"""
        try:
            if self.pygame:
                self.pygame.mixer.music.load(self.sound_file)
                self.pygame.mixer.music.play()
                time.sleep(self.duration)
                self.pygame.mixer.music.stop()
            else:
                print("🚨 ALARM SOUND (pygame not available)")
                time.sleep(self.duration)
        except Exception as e:
            print(f"Error playing alarm sound: {e}")
        finally:
            with self.lock:
                self.is_active = False
    
    def _generate_beep(self):
        """Generate simple beep sound"""
        try:
            if self.pygame:
                import numpy as np
                # Generate square wave beep
                frequency = 1000  # Hz
                sample_rate = 22050
                duration_ms = self.duration * 1000
                
                # Generate samples
                num_samples = int(sample_rate * self.duration)
                samples = []
                
                for i in range(num_samples):
                    value = 32767 if (i // (sample_rate // frequency)) % 2 == 0 else -32767
                    samples.append([value, value])
                
                # Play sound
                sound = self.pygame.sndarray.make_sound(np.array(samples, dtype=np.int16))
                sound.play()
                time.sleep(self.duration)
                sound.stop()
            else:
                print("🚨 BEEP SOUND (pygame not available)")
                time.sleep(self.duration)
        except Exception as e:
            print(f"Error generating beep: {e}")
        finally:
            with self.lock:
                self.is_active = False
    
    def stop(self):
        """Stop alarm"""
        with self.lock:
            if self.audio_available and self.pygame:
                try:
                    self.pygame.mixer.music.stop()
                except:
                    pass
            self.is_active = False
    
    def get_stats(self) -> dict:
        """Get alarm statistics"""
        with self.lock:
            return {
                'enabled': self.enabled,
                'is_active': self.is_active,
                'trigger_count': self.trigger_count,
                'time_since_last_trigger_s': time.time() - self.last_trigger_time if self.last_trigger_time > 0 else None,
                'cooldown_period_s': self.cooldown_period
            }


class NotificationSystem:
    """
    Email/SMS Notification System
    
    COA Concepts:
    - Network I/O operations
    - Asynchronous communication
    - Message queue
    """
    
    def __init__(self, config: dict):
        """
        Initialize notification system
        
        Args:
            config: Configuration dictionary with email/SMS settings
        """
        self.email_enabled = config.get('email_enabled', False)
        self.sms_enabled = config.get('sms_enabled', False)
        
        self.email_settings = config.get('email_settings', {})
        
        self.notification_count = 0
        self.lock = threading.Lock()
    
    def send_email_alert(self, subject: str, body: str, image_path: Optional[str] = None):
        """
        Send email notification
        
        COA Concept: Network I/O operation
        """
        if not self.email_enabled:
            return
        
        # Send email in separate thread to avoid blocking
        email_thread = threading.Thread(
            target=self._send_email_internal,
            args=(subject, body, image_path),
            daemon=True
        )
        email_thread.start()
    
    def _send_email_internal(self, subject: str, body: str, image_path: Optional[str]):
        """Internal email sending function"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_settings.get('sender_email', '')
            msg['To'] = self.email_settings.get('recipient_email', '')
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Add image if provided
            if image_path and os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
                    msg.attach(img)
            
            # Send email
            smtp_server = self.email_settings.get('smtp_server', 'smtp.gmail.com')
            smtp_port = self.email_settings.get('smtp_port', 587)
            sender_email = self.email_settings.get('sender_email', '')
            sender_password = self.email_settings.get('sender_password', '')
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            with self.lock:
                self.notification_count += 1
            
            print(f"Email notification sent: {subject}")
            
        except Exception as e:
            print(f"Error sending email: {e}")
    
    def send_sms_alert(self, message: str):
        """
        Send SMS notification
        
        COA Concept: Network I/O operation
        Note: Requires SMS gateway service (not implemented in demo)
        """
        if not self.sms_enabled:
            return
        
        print(f"SMS notification (not implemented): {message}")
        
        with self.lock:
            self.notification_count += 1
    
    def get_stats(self) -> dict:
        """Get notification statistics"""
        with self.lock:
            return {
                'email_enabled': self.email_enabled,
                'sms_enabled': self.sms_enabled,
                'notification_count': self.notification_count
            }

