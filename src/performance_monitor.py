"""
Performance Monitoring Module
Demonstrates COA concepts: Performance Metrics, Benchmarking, System Monitoring

COA Concepts Implemented:
- FPS (Frames Per Second) measurement
- CPU utilization tracking
- Memory usage monitoring
- Throughput and latency calculation
- Performance profiling
"""

import time
import psutil
import threading
from typing import Dict, Any, List
from datetime import datetime
import json


class FPSCounter:
    """
    Frames Per Second Counter
    
    COA Concept: Throughput measurement
    FPS = Number of frames / Time elapsed
    """
    
    def __init__(self, window_size: int = 30):
        """
        Initialize FPS counter
        
        Args:
            window_size: Number of frames for moving average
        """
        self.window_size = window_size
        self.frame_times = []
        self.frame_count = 0
        self.start_time = time.time()
        self.lock = threading.Lock()
    
    def tick(self):
        """
        Register frame processed
        
        COA Concept: Increment instruction counter
        """
        with self.lock:
            current_time = time.time()
            self.frame_times.append(current_time)
            self.frame_count += 1
            
            # Keep only recent frames in window
            if len(self.frame_times) > self.window_size:
                self.frame_times.pop(0)
    
    def get_fps(self) -> float:
        """
        Calculate current FPS
        
        COA Concept: Throughput calculation
        """
        with self.lock:
            if len(self.frame_times) < 2:
                return 0.0
            
            time_diff = self.frame_times[-1] - self.frame_times[0]
            if time_diff == 0:
                return 0.0
            
            return (len(self.frame_times) - 1) / time_diff
    
    def get_average_fps(self) -> float:
        """
        Calculate average FPS since start
        
        COA Concept: Overall throughput
        """
        with self.lock:
            elapsed = time.time() - self.start_time
            if elapsed == 0:
                return 0.0
            return self.frame_count / elapsed
    
    def get_stats(self) -> dict:
        """Get FPS statistics"""
        return {
            'current_fps': self.get_fps(),
            'average_fps': self.get_average_fps(),
            'total_frames': self.frame_count,
            'runtime_seconds': time.time() - self.start_time
        }


class PerformanceMonitor:
    """
    System Performance Monitor
    
    COA Concepts:
    - CPU utilization
    - Memory usage
    - System resource monitoring
    - Performance profiling
    """
    
    def __init__(self):
        """Initialize performance monitor"""
        self.start_time = time.time()
        self.samples = []
        self.lock = threading.Lock()
        
        # Get process handle
        import os
        self.process = psutil.Process(os.getpid())
        
        # Monitoring thread
        self.monitoring = False
        self.monitor_thread = None
        self.sample_interval = 1.0  # seconds
    
    def start_monitoring(self, interval: float = 1.0):
        """
        Start continuous performance monitoring
        
        Args:
            interval: Sampling interval in seconds
        """
        self.sample_interval = interval
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True
        )
        self.monitor_thread.start()
        print("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
        print("Performance monitoring stopped")
    
    def _monitor_loop(self):
        """Monitoring loop (runs in separate thread)"""
        while self.monitoring:
            self.sample()
            time.sleep(self.sample_interval)
    
    def sample(self):
        """
        Take performance sample
        
        COA Concept: System state snapshot
        """
        try:
            # CPU metrics
            cpu_percent = self.process.cpu_percent(interval=0.1)
            cpu_times = self.process.cpu_times()
            
            # Memory metrics
            memory_info = self.process.memory_info()
            memory_percent = self.process.memory_percent()
            
            # Thread metrics
            num_threads = self.process.num_threads()
            
            # System-wide metrics
            system_cpu = psutil.cpu_percent(percpu=False)
            system_memory = psutil.virtual_memory()
            
            sample = {
                'timestamp': time.time(),
                'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                
                # Process CPU
                'cpu_percent': cpu_percent,
                'cpu_user_time': cpu_times.user,
                'cpu_system_time': cpu_times.system,
                
                # Process Memory
                'memory_rss_mb': memory_info.rss / (1024 * 1024),
                'memory_vms_mb': memory_info.vms / (1024 * 1024),
                'memory_percent': memory_percent,
                
                # Threads
                'num_threads': num_threads,
                
                # System-wide
                'system_cpu_percent': system_cpu,
                'system_memory_percent': system_memory.percent,
                'system_memory_available_mb': system_memory.available / (1024 * 1024)
            }
            
            with self.lock:
                self.samples.append(sample)
            
        except Exception as e:
            print(f"Error sampling performance: {e}")
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        with self.lock:
            if not self.samples:
                return {}
            return self.samples[-1].copy()
    
    def get_average_metrics(self) -> Dict[str, Any]:
        """
        Calculate average metrics
        
        COA Concept: Statistical performance analysis
        """
        with self.lock:
            if not self.samples:
                return {}
            
            num_samples = len(self.samples)
            
            avg_metrics = {
                'num_samples': num_samples,
                'avg_cpu_percent': sum(s['cpu_percent'] for s in self.samples) / num_samples,
                'avg_memory_mb': sum(s['memory_rss_mb'] for s in self.samples) / num_samples,
                'avg_threads': sum(s['num_threads'] for s in self.samples) / num_samples,
                'avg_system_cpu': sum(s['system_cpu_percent'] for s in self.samples) / num_samples,
                'avg_system_memory': sum(s['system_memory_percent'] for s in self.samples) / num_samples
            }
            
            return avg_metrics
    
    def get_peak_metrics(self) -> Dict[str, Any]:
        """
        Get peak resource usage
        
        COA Concept: Worst-case performance
        """
        with self.lock:
            if not self.samples:
                return {}
            
            peak_metrics = {
                'peak_cpu_percent': max(s['cpu_percent'] for s in self.samples),
                'peak_memory_mb': max(s['memory_rss_mb'] for s in self.samples),
                'peak_threads': max(s['num_threads'] for s in self.samples),
                'peak_system_cpu': max(s['system_cpu_percent'] for s in self.samples)
            }
            
            return peak_metrics
    
    def get_all_samples(self) -> List[Dict]:
        """Get all performance samples"""
        with self.lock:
            return self.samples.copy()
    
    def clear_samples(self):
        """Clear all samples"""
        with self.lock:
            self.samples.clear()
    
    def get_runtime(self) -> float:
        """Get total runtime in seconds"""
        return time.time() - self.start_time


class PerformanceBenchmark:
    """
    Performance Benchmarking Tool
    
    COA Concepts:
    - Execution time measurement
    - Cycle counting
    - Performance comparison
    """
    
    def __init__(self):
        """Initialize benchmark"""
        self.benchmarks = {}
        self.lock = threading.Lock()
    
    def start_benchmark(self, name: str):
        """Start timing a benchmark"""
        with self.lock:
            self.benchmarks[name] = {
                'start_time': time.time(),
                'end_time': None,
                'duration': None,
                'iterations': 0
            }
    
    def end_benchmark(self, name: str):
        """End timing a benchmark"""
        with self.lock:
            if name in self.benchmarks:
                end_time = time.time()
                start_time = self.benchmarks[name]['start_time']
                duration = end_time - start_time
                
                self.benchmarks[name]['end_time'] = end_time
                self.benchmarks[name]['duration'] = duration
                
                return duration
            return None
    
    def record_iteration(self, name: str):
        """Record an iteration for benchmark"""
        with self.lock:
            if name in self.benchmarks:
                self.benchmarks[name]['iterations'] += 1
    
    def get_benchmark(self, name: str) -> Dict:
        """Get benchmark results"""
        with self.lock:
            if name not in self.benchmarks:
                return {}
            
            benchmark = self.benchmarks[name].copy()
            
            # Calculate iterations per second
            if benchmark['duration'] and benchmark['duration'] > 0:
                benchmark['iterations_per_second'] = benchmark['iterations'] / benchmark['duration']
            else:
                benchmark['iterations_per_second'] = 0
            
            return benchmark
    
    def get_all_benchmarks(self) -> Dict:
        """Get all benchmark results"""
        with self.lock:
            return {name: self.get_benchmark(name) for name in self.benchmarks}


class PerformanceReport:
    """
    Performance Report Generator
    
    COA Concepts:
    - Performance analysis
    - Metrics aggregation
    - Report generation
    """
    
    @staticmethod
    def generate_report(
        fps_stats: Dict,
        monitor_stats: Dict,
        memory_stats: Dict,
        pipeline_stats: Dict,
        motion_stats: Dict,
        face_stats: Dict,
        io_stats: Dict
    ) -> Dict[str, Any]:
        """
        Generate comprehensive performance report
        
        Args:
            Various statistics dictionaries from different modules
        
        Returns:
            Complete performance report
        """
        report = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'report_date': datetime.now().strftime("%Y-%m-%d"),
            
            # Video Processing Performance
            'video_processing': {
                'fps': fps_stats,
                'pipeline': pipeline_stats
            },
            
            # Detection Performance
            'detection': {
                'motion_detection': motion_stats,
                'face_recognition': face_stats
            },
            
            # System Resources
            'system_resources': {
                'cpu': {
                    'average_percent': monitor_stats.get('avg_cpu_percent', 0),
                    'peak_percent': monitor_stats.get('peak_cpu_percent', 0)
                },
                'memory': {
                    'average_mb': monitor_stats.get('avg_memory_mb', 0),
                    'peak_mb': monitor_stats.get('peak_memory_mb', 0),
                    'cache_stats': memory_stats
                },
                'threads': {
                    'average': monitor_stats.get('avg_threads', 0),
                    'peak': monitor_stats.get('peak_threads', 0)
                }
            },
            
            # I/O Performance
            'io_performance': io_stats,
            
            # COA Metrics
            'coa_metrics': {
                'throughput_fps': fps_stats.get('current_fps', 0),
                'average_latency_ms': pipeline_stats.get('average_latency_ms', 0),
                'cpi_equivalent': pipeline_stats.get('cpi', 0),
                'cache_hit_rate': face_stats.get('cache_hit_rate_percent', 0),
                'memory_efficiency': memory_stats.get('l1_cache', {}).get('utilization', 0)
            }
        }
        
        return report
    
    @staticmethod
    def save_report(report: Dict, filepath: str):
        """Save report to JSON file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Performance report saved: {filepath}")
        except Exception as e:
            print(f"Error saving report: {e}")
    
    @staticmethod
    def print_report_summary(report: Dict):
        """Print report summary to console"""
        print("\n" + "="*60)
        print("PERFORMANCE REPORT SUMMARY")
        print("="*60)
        
        # Video Processing
        fps = report['video_processing']['fps'].get('current_fps', 0)
        print(f"\n📹 Video Processing:")
        print(f"   Current FPS: {fps:.2f}")
        print(f"   Average FPS: {report['video_processing']['fps'].get('average_fps', 0):.2f}")
        
        # Detection
        print(f"\n🔍 Detection Performance:")
        motion_fps = report['detection']['motion_detection'].get('fps', 0)
        print(f"   Motion Detection FPS: {motion_fps:.2f}")
        
        # System Resources
        print(f"\n💻 System Resources:")
        print(f"   CPU Usage: {report['system_resources']['cpu']['average_percent']:.1f}%")
        print(f"   Memory Usage: {report['system_resources']['memory']['average_mb']:.1f} MB")
        
        # COA Metrics
        print(f"\n📊 COA Metrics:")
        print(f"   Throughput: {report['coa_metrics']['throughput_fps']:.2f} FPS")
        print(f"   Average Latency: {report['coa_metrics']['average_latency_ms']:.2f} ms")
        print(f"   Cache Hit Rate: {report['coa_metrics']['cache_hit_rate']:.1f}%")
        
        print("="*60 + "\n")
