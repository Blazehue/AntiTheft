"""
CPU Architecture Module
Demonstrates COA concepts: Pipelining, Multi-threading, Parallel Processing

COA Concepts Implemented:
- Pipeline stages (Fetch, Decode, Execute, Write-back)
- Multi-threading with thread synchronization
- Instruction-level parallelism
- Performance monitoring (CPI, throughput, latency)
"""

import threading
import time
import queue
from typing import Callable, Any, Optional
from enum import Enum
import psutil
import os


class PipelineStage(Enum):
    """
    Pipeline stages for frame processing
    
    COA Concept: Instruction pipeline stages
    """
    FETCH = "FETCH"  # Frame acquisition from camera
    DECODE = "DECODE"  # Frame preprocessing
    EXECUTE = "EXECUTE"  # Motion/face detection
    WRITEBACK = "WRITEBACK"  # Alert/storage operations


class PipelineHazard(Enum):
    """
    Pipeline hazards
    
    COA Concept: Pipeline stalls and hazards
    """
    DATA_HAZARD = "DATA_HAZARD"  # Dependency between stages
    STRUCTURAL_HAZARD = "STRUCTURAL_HAZARD"  # Resource conflict
    CONTROL_HAZARD = "CONTROL_HAZARD"  # Branch/control flow change


class Pipeline:
    """
    Processing Pipeline Implementation
    
    COA Concepts:
    - Multi-stage pipeline
    - Throughput measurement (frames per second)
    - Latency measurement (time per frame)
    - Pipeline hazard detection and handling
    """
    
    def __init__(self, name: str, stages: list):
        """
        Initialize pipeline with stages
        
        Args:
            name: Pipeline identifier
            stages: List of processing functions (one per stage)
        """
        self.name = name
        self.stages = stages
        self.num_stages = len(stages)
        
        # Inter-stage queues (pipeline registers)
        self.stage_queues = [queue.Queue(maxsize=10) for _ in range(self.num_stages + 1)]
        
        # Performance metrics
        self.frames_processed = 0
        self.total_latency = 0.0
        self.pipeline_start_time = None
        self.hazard_count = {hazard: 0 for hazard in PipelineHazard}
        self.stall_count = 0
        
        self.lock = threading.Lock()
        self.running = False
        
    def execute_stage(self, stage_id: int, stage_func: Callable):
        """
        Execute single pipeline stage
        
        COA Concept: Pipeline stage execution
        Each stage reads from input queue, processes, writes to output queue
        """
        input_queue = self.stage_queues[stage_id]
        output_queue = self.stage_queues[stage_id + 1]
        
        while self.running:
            try:
                # Fetch from previous stage (pipeline register read)
                data = input_queue.get(timeout=0.1)
                
                if data is None:  # Poison pill
                    output_queue.put(None)
                    break
                
                start_time = time.time()
                
                # Execute stage function
                result = stage_func(data)
                
                stage_time = time.time() - start_time
                
                # Write to next stage (pipeline register write)
                if result is not None:
                    result['stage_time'] = stage_time
                    result['stage_id'] = stage_id
                    output_queue.put(result)
                else:
                    # Pipeline bubble (NOP)
                    self.stall_count += 1
                    
            except queue.Empty:
                # No data available - pipeline stall
                time.sleep(0.01)
                continue
            except Exception as e:
                print(f"Pipeline stage {stage_id} error: {e}")
    
    def start(self):
        """Start pipeline execution"""
        self.running = True
        self.pipeline_start_time = time.time()
        
        # Create thread for each pipeline stage
        self.stage_threads = []
        for i, stage_func in enumerate(self.stages):
            thread = threading.Thread(
                target=self.execute_stage,
                args=(i, stage_func),
                name=f"Pipeline-{self.name}-Stage{i}",
                daemon=True
            )
            thread.start()
            self.stage_threads.append(thread)
    
    def stop(self):
        """Stop pipeline execution"""
        self.running = False
        # Send poison pills
        self.stage_queues[0].put(None)
        
        # Wait for all stages to complete
        for thread in self.stage_threads:
            thread.join(timeout=2.0)
    
    def feed(self, data: dict):
        """Feed data into pipeline (first stage)"""
        data['pipeline_entry_time'] = time.time()
        self.stage_queues[0].put(data)
    
    def get_output(self, timeout: float = 0.1) -> Optional[dict]:
        """Get processed output from pipeline (last stage)"""
        try:
            result = self.stage_queues[self.num_stages].get(timeout=timeout)
            
            if result is not None:
                # Calculate pipeline latency
                latency = time.time() - result['pipeline_entry_time']
                with self.lock:
                    self.frames_processed += 1
                    self.total_latency += latency
                result['pipeline_latency'] = latency
            
            return result
        except queue.Empty:
            return None
    
    def get_throughput(self) -> float:
        """
        Calculate pipeline throughput (frames per second)
        
        COA Concept: Throughput = Instructions / Time
        """
        with self.lock:
            if self.pipeline_start_time is None:
                return 0.0
            elapsed = time.time() - self.pipeline_start_time
            if elapsed == 0:
                return 0.0
            return self.frames_processed / elapsed
    
    def get_average_latency(self) -> float:
        """
        Calculate average pipeline latency
        
        COA Concept: Latency = Time per instruction
        """
        with self.lock:
            if self.frames_processed == 0:
                return 0.0
            return self.total_latency / self.frames_processed
    
    def get_cpi(self) -> float:
        """
        Calculate Cycles Per Instruction (CPI) equivalent
        
        COA Concept: CPI = Clock Cycles / Instructions Executed
        In our context: Average time per frame / ideal time per frame
        """
        avg_latency = self.get_average_latency()
        ideal_latency = 1.0 / 30.0  # Assuming 30 FPS ideal
        
        if ideal_latency == 0:
            return 0.0
        return avg_latency / ideal_latency
    
    def record_hazard(self, hazard_type: PipelineHazard):
        """Record pipeline hazard occurrence"""
        with self.lock:
            self.hazard_count[hazard_type] += 1
    
    def get_stats(self) -> dict:
        """Get pipeline performance statistics"""
        with self.lock:
            return {
                'name': self.name,
                'num_stages': self.num_stages,
                'frames_processed': self.frames_processed,
                'throughput_fps': self.get_throughput(),
                'average_latency_ms': self.get_average_latency() * 1000,
                'cpi': self.get_cpi(),
                'stall_count': self.stall_count,
                'hazards': {hazard.value: count for hazard, count in self.hazard_count.items()}
            }


class WorkerThread:
    """
    Worker Thread with performance monitoring
    
    COA Concepts:
    - Thread lifecycle management
    - Thread synchronization (locks, semaphores)
    - CPU affinity and priority
    """
    
    def __init__(self, name: str, target_func: Callable, priority: str = "normal"):
        """
        Initialize worker thread
        
        Args:
            name: Thread identifier
            target_func: Function to execute in thread
            priority: Thread priority (high, normal, low)
        """
        self.name = name
        self.target_func = target_func
        self.priority = priority
        
        self.thread = None
        self.running = False
        self.lock = threading.Lock()
        self.semaphore = threading.Semaphore(1)
        
        # Performance metrics
        self.execution_count = 0
        self.total_cpu_time = 0.0
        self.start_time = None
        
    def start(self):
        """Start thread execution"""
        self.running = True
        self.start_time = time.time()
        self.thread = threading.Thread(
            target=self._run,
            name=self.name,
            daemon=True
        )
        self.thread.start()
        
        # Set thread priority (OS-dependent)
        try:
            if self.priority == "high":
                # Note: Thread priority manipulation is limited in Python
                pass
        except:
            pass
    
    def _run(self):
        """Internal thread execution loop"""
        process = psutil.Process(os.getpid())
        
        while self.running:
            try:
                cpu_before = process.cpu_percent()
                exec_start = time.time()
                
                # Execute target function
                self.target_func()
                
                exec_time = time.time() - exec_start
                cpu_after = process.cpu_percent()
                
                with self.lock:
                    self.execution_count += 1
                    self.total_cpu_time += exec_time
                    
            except Exception as e:
                print(f"Thread {self.name} error: {e}")
    
    def stop(self):
        """Stop thread execution"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
    
    def acquire(self, timeout: float = None) -> bool:
        """Acquire semaphore (mutex lock)"""
        return self.semaphore.acquire(timeout=timeout)
    
    def release(self):
        """Release semaphore"""
        self.semaphore.release()
    
    def get_stats(self) -> dict:
        """Get thread performance statistics"""
        with self.lock:
            runtime = time.time() - self.start_time if self.start_time else 0
            return {
                'name': self.name,
                'priority': self.priority,
                'execution_count': self.execution_count,
                'total_cpu_time_s': self.total_cpu_time,
                'runtime_s': runtime,
                'avg_execution_time_ms': (self.total_cpu_time / self.execution_count * 1000) if self.execution_count > 0 else 0,
                'is_alive': self.thread.is_alive() if self.thread else False
            }


class CPUMonitor:
    """
    CPU Performance Monitor
    
    COA Concepts:
    - CPU utilization measurement
    - Per-core usage tracking
    - Process-level performance metrics
    """
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.measurements = []
        self.lock = threading.Lock()
        
    def record_usage(self):
        """Record current CPU usage"""
        with self.lock:
            cpu_percent = self.process.cpu_percent(interval=0.1)
            memory_info = self.process.memory_info()
            num_threads = self.process.num_threads()
            
            measurement = {
                'timestamp': time.time(),
                'cpu_percent': cpu_percent,
                'memory_rss_mb': memory_info.rss / (1024 * 1024),
                'memory_vms_mb': memory_info.vms / (1024 * 1024),
                'num_threads': num_threads,
                'cpu_count': psutil.cpu_count(),
                'per_cpu_percent': psutil.cpu_percent(percpu=True)
            }
            
            self.measurements.append(measurement)
    
    def get_average_cpu_usage(self) -> float:
        """Get average CPU utilization"""
        with self.lock:
            if not self.measurements:
                return 0.0
            return sum(m['cpu_percent'] for m in self.measurements) / len(self.measurements)
    
    def get_peak_cpu_usage(self) -> float:
        """Get peak CPU utilization"""
        with self.lock:
            if not self.measurements:
                return 0.0
            return max(m['cpu_percent'] for m in self.measurements)
    
    def get_stats(self) -> dict:
        """Get CPU performance statistics"""
        with self.lock:
            return {
                'measurement_count': len(self.measurements),
                'average_cpu_percent': self.get_average_cpu_usage(),
                'peak_cpu_percent': self.get_peak_cpu_usage(),
                'current_threads': self.process.num_threads() if self.measurements else 0,
                'cpu_count': psutil.cpu_count()
            }


class ThreadPool:
    """
    Simple Thread Pool Implementation
    
    COA Concepts:
    - Resource pooling and reuse
    - Task scheduling
    - Load balancing across cores
    """
    
    def __init__(self, num_workers: int):
        """
        Initialize thread pool
        
        Args:
            num_workers: Number of worker threads
        """
        self.num_workers = num_workers
        self.task_queue = queue.Queue()
        self.workers = []
        self.running = False
        
        # Statistics
        self.tasks_completed = 0
        self.lock = threading.Lock()
    
    def _worker(self):
        """Worker thread function"""
        while self.running:
            try:
                task = self.task_queue.get(timeout=0.1)
                if task is None:
                    break
                
                func, args, kwargs = task
                func(*args, **kwargs)
                
                with self.lock:
                    self.tasks_completed += 1
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Worker error: {e}")
    
    def start(self):
        """Start thread pool"""
        self.running = True
        for i in range(self.num_workers):
            worker = threading.Thread(
                target=self._worker,
                name=f"PoolWorker-{i}",
                daemon=True
            )
            worker.start()
            self.workers.append(worker)
    
    def submit(self, func: Callable, *args, **kwargs):
        """Submit task to thread pool"""
        self.task_queue.put((func, args, kwargs))
    
    def shutdown(self):
        """Shutdown thread pool"""
        self.running = False
        
        # Send poison pills
        for _ in range(self.num_workers):
            self.task_queue.put(None)
        
        # Wait for workers
        for worker in self.workers:
            worker.join(timeout=2.0)
    
    def get_stats(self) -> dict:
        """Get thread pool statistics"""
        with self.lock:
            return {
                'num_workers': self.num_workers,
                'tasks_completed': self.tasks_completed,
                'pending_tasks': self.task_queue.qsize()
            }
