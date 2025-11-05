"""
I/O and Storage System
Demonstrates COA concepts: File System, I/O Operations, Storage Hierarchy

COA Concepts Implemented:
- File system operations (create, read, write, delete)
- Sequential vs random access patterns
- Data compression (JPEG)
- Storage hierarchy (RAM to Disk)
- Logging system with timestamps
"""

import os
import cv2
import json
import time
from datetime import datetime
from typing import Optional, Dict, Any
import threading


class FileSystem:
    """
    File System Management
    
    COA Concepts:
    - File system operations
    - Directory structure
    - Storage organization
    """
    
    def __init__(self, config: dict):
        """
        Initialize file system
        
        Args:
            config: Configuration dictionary with storage paths
        """
        self.base_path = config.get('base_path', 'storage')
        self.intruder_images_path = config.get('intruder_images_path', 'storage/intruders')
        self.logs_path = config.get('logs_path', 'storage/logs')
        self.authorized_faces_path = config.get('authorized_faces_path', 'storage/authorized_faces')
        self.compression_quality = config.get('compression_quality', 85)
        self.max_storage_mb = config.get('max_storage_mb', 1000)
        
        # Statistics
        self.files_written = 0
        self.files_read = 0
        self.bytes_written = 0
        self.bytes_read = 0
        self.write_operations_time = 0.0
        self.read_operations_time = 0.0
        
        self.lock = threading.Lock()
        
        # Initialize directory structure
        self._initialize_directories()
    
    def _initialize_directories(self):
        """
        Initialize directory structure
        
        COA Concept: File system initialization
        Creates directory tree structure
        """
        directories = [
            self.base_path,
            self.intruder_images_path,
            self.logs_path,
            self.authorized_faces_path
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        print(f"File system initialized at: {self.base_path}")
    
    def save_image(self, image, filename: str, subdir: str = "intruders") -> Optional[str]:
        """
        Save image to disk
        
        COA Concepts:
        - Disk write operation (I/O)
        - Data compression (JPEG encoding)
        - Sequential write access
        
        Returns:
            Full path to saved file
        """
        start_time = time.time()
        
        try:
            # Determine target directory
            if subdir == "intruders":
                target_dir = self.intruder_images_path
            elif subdir == "authorized":
                target_dir = self.authorized_faces_path
            else:
                target_dir = os.path.join(self.base_path, subdir)
                os.makedirs(target_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            full_filename = f"{timestamp}_{filename}"
            filepath = os.path.join(target_dir, full_filename)
            
            # Compress and write to disk (I/O operation)
            success = cv2.imwrite(
                filepath,
                image,
                [cv2.IMWRITE_JPEG_QUALITY, self.compression_quality]
            )
            
            if success:
                # Get file size
                file_size = os.path.getsize(filepath)
                
                # Update statistics
                write_time = time.time() - start_time
                with self.lock:
                    self.files_written += 1
                    self.bytes_written += file_size
                    self.write_operations_time += write_time
                
                print(f"Image saved: {full_filename} ({file_size} bytes, {write_time*1000:.2f}ms)")
                return filepath
            else:
                print(f"Failed to save image: {filepath}")
                return None
                
        except Exception as e:
            print(f"Error saving image: {e}")
            return None
    
    def read_image(self, filepath: str):
        """
        Read image from disk
        
        COA Concepts:
        - Disk read operation (I/O)
        - Random access (direct file access by path)
        
        Returns:
            Image data or None
        """
        start_time = time.time()
        
        try:
            if not os.path.exists(filepath):
                print(f"File not found: {filepath}")
                return None
            
            # Get file size
            file_size = os.path.getsize(filepath)
            
            # Read from disk (I/O operation)
            image = cv2.imread(filepath)
            
            # Update statistics
            read_time = time.time() - start_time
            with self.lock:
                self.files_read += 1
                self.bytes_read += file_size
                self.read_operations_time += read_time
            
            return image
            
        except Exception as e:
            print(f"Error reading image: {e}")
            return None
    
    def delete_old_files(self, days: int = 7):
        """
        Delete files older than specified days
        
        COA Concept: File system maintenance
        Storage management and cleanup
        """
        current_time = time.time()
        cutoff_time = current_time - (days * 24 * 60 * 60)
        
        deleted_count = 0
        deleted_bytes = 0
        
        for root, dirs, files in os.walk(self.base_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                
                try:
                    # Get file modification time
                    file_mtime = os.path.getmtime(filepath)
                    
                    if file_mtime < cutoff_time:
                        file_size = os.path.getsize(filepath)
                        os.remove(filepath)
                        deleted_count += 1
                        deleted_bytes += file_size
                except Exception as e:
                    print(f"Error deleting file {filepath}: {e}")
        
        print(f"Deleted {deleted_count} old files ({deleted_bytes} bytes)")
        return deleted_count, deleted_bytes
    
    def get_storage_usage(self) -> dict:
        """
        Get current storage usage
        
        COA Concept: Storage monitoring
        """
        total_size = 0
        file_count = 0
        
        for root, dirs, files in os.walk(self.base_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    total_size += os.path.getsize(filepath)
                    file_count += 1
                except:
                    pass
        
        total_size_mb = total_size / (1024 * 1024)
        usage_percent = (total_size_mb / self.max_storage_mb) * 100 if self.max_storage_mb > 0 else 0
        
        return {
            'total_files': file_count,
            'total_size_bytes': total_size,
            'total_size_mb': total_size_mb,
            'max_storage_mb': self.max_storage_mb,
            'usage_percent': usage_percent
        }
    
    def get_io_stats(self) -> dict:
        """
        Get I/O performance statistics
        
        COA Concepts:
        - I/O throughput
        - Average access time
        - Read/write performance
        """
        with self.lock:
            avg_write_time = (self.write_operations_time / self.files_written) if self.files_written > 0 else 0
            avg_read_time = (self.read_operations_time / self.files_read) if self.files_read > 0 else 0
            
            write_throughput = (self.bytes_written / self.write_operations_time) if self.write_operations_time > 0 else 0
            read_throughput = (self.bytes_read / self.read_operations_time) if self.read_operations_time > 0 else 0
            
            return {
                'files_written': self.files_written,
                'files_read': self.files_read,
                'bytes_written': self.bytes_written,
                'bytes_read': self.bytes_read,
                'avg_write_time_ms': avg_write_time * 1000,
                'avg_read_time_ms': avg_read_time * 1000,
                'write_throughput_mbps': (write_throughput / (1024 * 1024)),
                'read_throughput_mbps': (read_throughput / (1024 * 1024))
            }


class Logger:
    """
    Logging System
    
    COA Concepts:
    - Sequential write operations
    - Buffered I/O
    - Timestamp generation
    """
    
    def __init__(self, log_dir: str, log_name: str = "system"):
        """
        Initialize logger
        
        Args:
            log_dir: Directory for log files
            log_name: Base name for log files
        """
        self.log_dir = log_dir
        self.log_name = log_name
        self.lock = threading.Lock()
        
        os.makedirs(log_dir, exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d")
        self.log_file = os.path.join(log_dir, f"{log_name}_{timestamp}.log")
        
        # Statistics
        self.log_entries = 0
    
    def log(self, level: str, message: str, data: Optional[Dict[Any, Any]] = None):
        """
        Write log entry
        
        COA Concept: Sequential write with timestamp
        
        Args:
            level: Log level (INFO, WARNING, ERROR, etc.)
            message: Log message
            data: Optional dictionary of additional data
        """
        with self.lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            
            log_entry = f"[{timestamp}] [{level}] {message}"
            
            if data:
                log_entry += f" | Data: {json.dumps(data)}"
            
            # Write to file (sequential I/O)
            try:
                with open(self.log_file, 'a') as f:
                    f.write(log_entry + '\n')
                
                self.log_entries += 1
                
                # Also print to console
                print(log_entry)
            except Exception as e:
                print(f"Error writing to log: {e}")
    
    def info(self, message: str, data: Optional[Dict[Any, Any]] = None):
        """Log info message"""
        self.log("INFO", message, data)
    
    def warning(self, message: str, data: Optional[Dict[Any, Any]] = None):
        """Log warning message"""
        self.log("WARNING", message, data)
    
    def error(self, message: str, data: Optional[Dict[Any, Any]] = None):
        """Log error message"""
        self.log("ERROR", message, data)
    
    def debug(self, message: str, data: Optional[Dict[Any, Any]] = None):
        """Log debug message"""
        self.log("DEBUG", message, data)
    
    def get_stats(self) -> dict:
        """Get logging statistics"""
        with self.lock:
            file_size = 0
            if os.path.exists(self.log_file):
                file_size = os.path.getsize(self.log_file)
            
            return {
                'log_file': self.log_file,
                'log_entries': self.log_entries,
                'log_file_size_bytes': file_size,
                'log_file_size_kb': file_size / 1024
            }


class EventRecorder:
    """
    Event Recording System
    
    COA Concepts:
    - Event logging with structured data
    - JSON serialization
    - Sequential write operations
    """
    
    def __init__(self, log_dir: str):
        """
        Initialize event recorder
        
        Args:
            log_dir: Directory for event logs
        """
        self.log_dir = log_dir
        self.lock = threading.Lock()
        
        os.makedirs(log_dir, exist_ok=True)
        
        # Event log file
        timestamp = datetime.now().strftime("%Y%m%d")
        self.event_file = os.path.join(log_dir, f"events_{timestamp}.json")
        
        # Initialize events list
        self.events = []
        
        # Load existing events if file exists
        if os.path.exists(self.event_file):
            try:
                with open(self.event_file, 'r') as f:
                    self.events = json.load(f)
            except:
                self.events = []
    
    def record_event(self, event_type: str, description: str, metadata: Optional[Dict] = None):
        """
        Record system event
        
        Args:
            event_type: Type of event (MOTION, FACE_DETECTED, ALARM, etc.)
            description: Event description
            metadata: Additional event data
        """
        with self.lock:
            event = {
                'timestamp': time.time(),
                'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'event_type': event_type,
                'description': description,
                'metadata': metadata or {}
            }
            
            self.events.append(event)
            
            # Write to file (persistent storage)
            try:
                with open(self.event_file, 'w') as f:
                    json.dump(self.events, f, indent=2)
            except Exception as e:
                print(f"Error recording event: {e}")
    
    def get_recent_events(self, count: int = 10) -> list:
        """Get most recent events"""
        with self.lock:
            return self.events[-count:]
    
    def get_events_by_type(self, event_type: str) -> list:
        """Get all events of specific type"""
        with self.lock:
            return [e for e in self.events if e['event_type'] == event_type]
    
    def get_stats(self) -> dict:
        """Get event statistics"""
        with self.lock:
            event_types = {}
            for event in self.events:
                event_type = event['event_type']
                event_types[event_type] = event_types.get(event_type, 0) + 1
            
            return {
                'total_events': len(self.events),
                'event_types': event_types,
                'event_file': self.event_file
            }
