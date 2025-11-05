"""
Memory Management Module
Demonstrates COA concepts: Frame Buffering, Cache Memory, Memory Hierarchy

COA Concepts Implemented:
- Circular Buffer (FIFO Queue) - Simulates L1 Cache
- LRU Cache - Least Recently Used replacement policy
- Memory Hierarchy - RAM vs Disk storage simulation
"""

import threading
from collections import OrderedDict
from typing import Any, Optional
import time
import numpy as np


class CircularFrameBuffer:
    """
    Circular Buffer Implementation (Ring Buffer)
    
    COA Concepts:
    - FIFO (First In First Out) queue structure
    - Fixed memory allocation (simulates hardware buffer)
    - Overflow handling (buffer full condition)
    - Demonstrates sequential memory access patterns
    """
    
    def __init__(self, capacity: int):
        """
        Initialize circular buffer with fixed capacity
        
        Args:
            capacity: Maximum number of frames to store (buffer size)
        """
        self.capacity = capacity
        self.buffer = [None] * capacity  # Static memory allocation
        self.head = 0  # Write pointer
        self.tail = 0  # Read pointer
        self.size = 0  # Current number of elements
        self.lock = threading.Lock()  # Thread synchronization
        
        # Performance metrics
        self.write_count = 0
        self.read_count = 0
        self.overflow_count = 0
        
    def write(self, frame: np.ndarray) -> bool:
        """
        Write frame to buffer (Producer operation)
        
        COA Concept: Write operation with overflow checking
        Simulates memory write cycle
        """
        with self.lock:  # Critical section
            if self.size == self.capacity:
                # Buffer overflow - overwrite oldest frame
                self.overflow_count += 1
                self.tail = (self.tail + 1) % self.capacity
                self.size -= 1
            
            # Write to buffer at head position
            self.buffer[self.head] = frame.copy()  # Deep copy to simulate memory allocation
            self.head = (self.head + 1) % self.capacity  # Circular increment
            self.size += 1
            self.write_count += 1
            return True
    
    def read(self) -> Optional[np.ndarray]:
        """
        Read frame from buffer (Consumer operation)
        
        COA Concept: Read operation with underflow checking
        Simulates memory read cycle
        """
        with self.lock:  # Critical section
            if self.size == 0:
                # Buffer underflow
                return None
            
            # Read from buffer at tail position
            frame = self.buffer[self.tail]
            self.buffer[self.tail] = None  # Clear reference (simulate deallocation)
            self.tail = (self.tail + 1) % self.capacity  # Circular increment
            self.size -= 1
            self.read_count += 1
            return frame
    
    def peek(self) -> Optional[np.ndarray]:
        """
        Peek at next frame without removing it
        
        COA Concept: Non-destructive read (like cache lookup)
        """
        with self.lock:
            if self.size == 0:
                return None
            return self.buffer[self.tail]
    
    def get_latest(self) -> Optional[np.ndarray]:
        """
        Get most recent frame without removing it
        
        COA Concept: Random access to buffer (like register access)
        """
        with self.lock:
            if self.size == 0:
                return None
            # Access most recent write position
            latest_idx = (self.head - 1) % self.capacity
            return self.buffer[latest_idx]
    
    def is_full(self) -> bool:
        """Check if buffer is at capacity"""
        with self.lock:
            return self.size == self.capacity
    
    def is_empty(self) -> bool:
        """Check if buffer is empty"""
        with self.lock:
            return self.size == 0
    
    def clear(self):
        """Clear all buffer contents (simulate memory reset)"""
        with self.lock:
            self.buffer = [None] * self.capacity
            self.head = 0
            self.tail = 0
            self.size = 0
    
    def get_stats(self) -> dict:
        """Get buffer performance statistics"""
        with self.lock:
            return {
                'capacity': self.capacity,
                'current_size': self.size,
                'utilization': (self.size / self.capacity) * 100,
                'write_count': self.write_count,
                'read_count': self.read_count,
                'overflow_count': self.overflow_count,
                'head_position': self.head,
                'tail_position': self.tail
            }


class LRUCache:
    """
    Least Recently Used (LRU) Cache Implementation
    
    COA Concepts:
    - Cache replacement policy (LRU algorithm)
    - Cache hit/miss tracking
    - Temporal locality exploitation
    - Fast lookup using hash table (O(1) access)
    """
    
    def __init__(self, capacity: int):
        """
        Initialize LRU cache with fixed capacity
        
        Args:
            capacity: Maximum number of items to cache
        """
        self.capacity = capacity
        self.cache = OrderedDict()  # Maintains insertion order
        self.lock = threading.Lock()
        
        # Performance metrics
        self.hit_count = 0
        self.miss_count = 0
        self.eviction_count = 0
        self.access_count = 0
        
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve item from cache
        
        COA Concept: Cache lookup with hit/miss tracking
        Simulates cache access cycle
        """
        with self.lock:
            self.access_count += 1
            
            if key in self.cache:
                # Cache HIT - move to end (most recently used)
                self.cache.move_to_end(key)
                self.hit_count += 1
                return self.cache[key]
            else:
                # Cache MISS
                self.miss_count += 1
                return None
    
    def put(self, key: str, value: Any) -> None:
        """
        Insert item into cache
        
        COA Concept: Cache write with eviction policy
        Simulates cache replacement algorithm
        """
        with self.lock:
            if key in self.cache:
                # Update existing entry
                self.cache.move_to_end(key)
            else:
                # New entry
                if len(self.cache) >= self.capacity:
                    # Cache full - evict LRU item
                    self.cache.popitem(last=False)  # Remove oldest (FIFO)
                    self.eviction_count += 1
            
            self.cache[key] = value
    
    def remove(self, key: str) -> bool:
        """Remove item from cache"""
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False
    
    def clear(self):
        """Clear entire cache"""
        with self.lock:
            self.cache.clear()
            self.hit_count = 0
            self.miss_count = 0
            self.eviction_count = 0
            self.access_count = 0
    
    def get_hit_rate(self) -> float:
        """
        Calculate cache hit rate
        
        COA Concept: Cache performance metric
        Hit Rate = Hits / Total Accesses
        """
        with self.lock:
            if self.access_count == 0:
                return 0.0
            return (self.hit_count / self.access_count) * 100
    
    def get_stats(self) -> dict:
        """Get cache performance statistics"""
        with self.lock:
            return {
                'capacity': self.capacity,
                'current_size': len(self.cache),
                'utilization': (len(self.cache) / self.capacity) * 100,
                'hit_count': self.hit_count,
                'miss_count': self.miss_count,
                'eviction_count': self.eviction_count,
                'access_count': self.access_count,
                'hit_rate': self.get_hit_rate()
            }


class MemoryHierarchy:
    """
    Memory Hierarchy Simulation
    
    COA Concepts:
    - L1 Cache (Frame Buffer) - Fast, small capacity
    - L2 Cache (Face Database) - Medium speed, medium capacity
    - Main Memory (Recent frames in RAM) - Slower, larger capacity
    - Secondary Storage (Disk) - Slowest, unlimited capacity
    """
    
    def __init__(self, l1_size: int, l2_size: int):
        """
        Initialize memory hierarchy
        
        Args:
            l1_size: L1 cache size (frame buffer)
            l2_size: L2 cache size (face database)
        """
        self.l1_cache = CircularFrameBuffer(l1_size)  # L1: Frame buffer
        self.l2_cache = LRUCache(l2_size)  # L2: Face recognition cache
        self.main_memory = {}  # Main memory (dict for flexibility)
        self.lock = threading.Lock()
        
        # Access time simulation (in microseconds)
        self.l1_access_time = 1
        self.l2_access_time = 10
        self.main_memory_access_time = 100
        self.disk_access_time = 10000
        
        # Statistics
        self.total_accesses = 0
        self.average_access_time = 0
        
    def access_frame(self, operation: str) -> tuple:
        """
        Simulate memory access for frame operations
        
        Returns:
            (success, access_time_us)
        """
        with self.lock:
            self.total_accesses += 1
            
            if operation == "read":
                frame = self.l1_cache.read()
                if frame is not None:
                    return (True, self.l1_access_time)
                return (False, self.l1_access_time)
            
            elif operation == "write":
                success = self.l1_cache.write(None)  # Placeholder
                return (success, self.l1_access_time)
        
        return (False, 0)
    
    def get_memory_stats(self) -> dict:
        """Get comprehensive memory statistics"""
        return {
            'l1_cache': self.l1_cache.get_stats(),
            'l2_cache': self.l2_cache.get_stats(),
            'main_memory_size': len(self.main_memory),
            'total_memory_accesses': self.total_accesses,
            'access_times': {
                'l1_us': self.l1_access_time,
                'l2_us': self.l2_access_time,
                'main_memory_us': self.main_memory_access_time,
                'disk_us': self.disk_access_time
            }
        }


class MemoryMonitor:
    """
    Monitor system memory usage
    
    COA Concepts:
    - Memory utilization tracking
    - Memory allocation patterns
    - Memory performance metrics
    """
    
    def __init__(self):
        self.measurements = []
        self.lock = threading.Lock()
        
    def record_usage(self, allocated_bytes: int, operation: str):
        """Record memory usage measurement"""
        with self.lock:
            timestamp = time.time()
            self.measurements.append({
                'timestamp': timestamp,
                'allocated_bytes': allocated_bytes,
                'allocated_mb': allocated_bytes / (1024 * 1024),
                'operation': operation
            })
    
    def get_peak_usage(self) -> float:
        """Get peak memory usage in MB"""
        with self.lock:
            if not self.measurements:
                return 0.0
            return max(m['allocated_mb'] for m in self.measurements)
    
    def get_average_usage(self) -> float:
        """Get average memory usage in MB"""
        with self.lock:
            if not self.measurements:
                return 0.0
            return sum(m['allocated_mb'] for m in self.measurements) / len(self.measurements)
    
    def get_stats(self) -> dict:
        """Get memory monitoring statistics"""
        with self.lock:
            return {
                'measurement_count': len(self.measurements),
                'peak_usage_mb': self.get_peak_usage(),
                'average_usage_mb': self.get_average_usage()
            }
