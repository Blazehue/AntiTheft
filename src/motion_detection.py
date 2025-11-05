"""
Motion Detection Module
Demonstrates COA concepts: Boolean Logic, Arithmetic Operations, Instruction Processing

COA Concepts Implemented:
- Pixel-level arithmetic operations (ALU simulation)
- Boolean logic for thresholding (AND, OR, NOT gates)
- Bitwise operations for masking
- Frame differencing algorithm
"""

import cv2
import numpy as np
import time
from typing import Tuple, List, Optional


class BooleanLogic:
    """
    Boolean Logic Operations
    
    COA Concepts:
    - Logic gates (AND, OR, NOT, XOR)
    - Binary operations
    - Conditional logic circuits
    """
    
    @staticmethod
    def AND(a: bool, b: bool) -> bool:
        """
        AND gate operation
        COA: Output is 1 only if both inputs are 1
        """
        return a and b
    
    @staticmethod
    def OR(a: bool, b: bool) -> bool:
        """
        OR gate operation
        COA: Output is 1 if at least one input is 1
        """
        return a or b
    
    @staticmethod
    def NOT(a: bool) -> bool:
        """
        NOT gate operation
        COA: Output is inverse of input
        """
        return not a
    
    @staticmethod
    def XOR(a: bool, b: bool) -> bool:
        """
        XOR gate operation
        COA: Output is 1 if inputs are different
        """
        return a != b
    
    @staticmethod
    def NAND(a: bool, b: bool) -> bool:
        """NAND gate (NOT AND)"""
        return not (a and b)
    
    @staticmethod
    def NOR(a: bool, b: bool) -> bool:
        """NOR gate (NOT OR)"""
        return not (a or b)
    
    @staticmethod
    def threshold_comparison(value: float, threshold: float, operation: str = "greater") -> bool:
        """
        Threshold comparison using comparator circuit
        
        COA Concept: Digital comparator
        """
        if operation == "greater":
            return value > threshold
        elif operation == "less":
            return value < threshold
        elif operation == "equal":
            return value == threshold
        elif operation == "greater_equal":
            return value >= threshold
        elif operation == "less_equal":
            return value <= threshold
        return False
    
    @staticmethod
    def alarm_condition(motion_detected: bool, face_unknown: bool, system_armed: bool) -> bool:
        """
        Complex alarm logic using multiple gates
        
        COA Concept: Combinational logic circuit
        Alarm = (MotionDetected OR FaceUnknown) AND SystemArmed
        """
        detection = BooleanLogic.OR(motion_detected, face_unknown)
        alarm = BooleanLogic.AND(detection, system_armed)
        return alarm


class ArithmeticLogicUnit:
    """
    Arithmetic Logic Unit (ALU) Simulation
    
    COA Concepts:
    - Arithmetic operations (ADD, SUB, MUL, DIV)
    - Pixel-level operations
    - Image arithmetic
    """
    
    @staticmethod
    def pixel_subtraction(frame1: np.ndarray, frame2: np.ndarray) -> np.ndarray:
        """
        Pixel-wise subtraction (frame differencing)
        
        COA Concept: ALU subtraction operation
        Result = |Frame1 - Frame2|
        """
        # Absolute difference (arithmetic operation)
        diff = cv2.absdiff(frame1, frame2)
        return diff
    
    @staticmethod
    def pixel_addition(frame1: np.ndarray, frame2: np.ndarray) -> np.ndarray:
        """
        Pixel-wise addition
        
        COA Concept: ALU addition operation
        """
        return cv2.add(frame1, frame2)
    
    @staticmethod
    def pixel_multiplication(frame: np.ndarray, scalar: float) -> np.ndarray:
        """
        Scalar multiplication
        
        COA Concept: ALU multiplication operation
        """
        return cv2.multiply(frame, scalar)
    
    @staticmethod
    def bitwise_and(frame1: np.ndarray, frame2: np.ndarray) -> np.ndarray:
        """
        Bitwise AND operation
        
        COA Concept: Bitwise AND gate at pixel level
        """
        return cv2.bitwise_and(frame1, frame2)
    
    @staticmethod
    def bitwise_or(frame1: np.ndarray, frame2: np.ndarray) -> np.ndarray:
        """
        Bitwise OR operation
        
        COA Concept: Bitwise OR gate at pixel level
        """
        return cv2.bitwise_or(frame1, frame2)
    
    @staticmethod
    def bitwise_not(frame: np.ndarray) -> np.ndarray:
        """
        Bitwise NOT operation
        
        COA Concept: Bitwise NOT gate (complement)
        """
        return cv2.bitwise_not(frame)
    
    @staticmethod
    def bitwise_xor(frame1: np.ndarray, frame2: np.ndarray) -> np.ndarray:
        """
        Bitwise XOR operation
        
        COA Concept: Bitwise XOR gate at pixel level
        """
        return cv2.bitwise_xor(frame1, frame2)
    
    @staticmethod
    def apply_mask(frame: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """
        Apply binary mask to frame
        
        COA Concept: Masking operation using AND gate
        Masked = Frame AND Mask
        """
        return cv2.bitwise_and(frame, frame, mask=mask)


class MotionDetector:
    """
    Motion Detection System
    
    COA Concepts:
    - Frame differencing algorithm
    - Threshold-based detection (comparator)
    - Contour analysis
    - Performance measurement (execution time)
    """
    
    def __init__(self, config: dict):
        """
        Initialize motion detector
        
        Args:
            config: Configuration dictionary with detection parameters
        """
        self.threshold = config.get('threshold', 25)
        self.min_contour_area = config.get('min_contour_area', 500)
        self.blur_kernel_size = config.get('blur_kernel_size', 21)
        self.dilation_iterations = config.get('dilation_iterations', 2)
        
        # Previous frame for differencing
        self.previous_frame = None
        
        # Boolean logic and ALU instances
        self.boolean_logic = BooleanLogic()
        self.alu = ArithmeticLogicUnit()
        
        # Performance metrics
        self.total_frames_processed = 0
        self.total_processing_time = 0.0
        self.motion_detected_count = 0
        
    def preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Preprocess frame for motion detection
        
        COA Concept: Instruction pipeline - preprocessing stage
        
        Steps:
        1. Convert to grayscale (color space transformation)
        2. Apply Gaussian blur (noise reduction)
        """
        # Convert to grayscale (reduces data by ~66%)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur (smoothing operation)
        blurred = cv2.GaussianBlur(gray, (self.blur_kernel_size, self.blur_kernel_size), 0)
        
        return blurred
    
    def compute_frame_difference(self, current_frame: np.ndarray) -> Optional[np.ndarray]:
        """
        Compute frame difference
        
        COA Concept: ALU subtraction operation
        Difference = |Current - Previous|
        """
        if self.previous_frame is None:
            self.previous_frame = current_frame
            return None
        
        # ALU operation: Frame subtraction
        frame_diff = self.alu.pixel_subtraction(current_frame, self.previous_frame)
        
        # Update previous frame
        self.previous_frame = current_frame
        
        return frame_diff
    
    def apply_threshold(self, frame_diff: np.ndarray) -> np.ndarray:
        """
        Apply threshold to difference frame
        
        COA Concept: Comparator circuit
        Output = 1 if pixel > threshold, else 0
        """
        # Binary threshold operation (comparator)
        _, thresh = cv2.threshold(frame_diff, self.threshold, 255, cv2.THRESH_BINARY)
        
        return thresh
    
    def morphological_operations(self, thresh: np.ndarray) -> np.ndarray:
        """
        Apply morphological operations
        
        COA Concept: Image processing operations
        - Dilation: Expand white regions
        - Erosion: Shrink white regions
        """
        # Dilation to fill gaps
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=self.dilation_iterations)
        
        return dilated
    
    def find_contours(self, processed_frame: np.ndarray) -> List[np.ndarray]:
        """
        Find contours in processed frame
        
        COA Concept: Edge detection and boundary tracing
        """
        contours, _ = cv2.findContours(
            processed_frame,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        return contours
    
    def filter_contours(self, contours: List[np.ndarray]) -> List[np.ndarray]:
        """
        Filter contours by area
        
        COA Concept: Conditional filtering using comparator
        """
        filtered = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Boolean comparison: area > min_area
            if self.boolean_logic.threshold_comparison(area, self.min_contour_area, "greater"):
                filtered.append(contour)
        
        return filtered
    
    def detect_motion(self, frame: np.ndarray) -> Tuple[bool, dict]:
        """
        Main motion detection pipeline
        
        COA Concept: Complete instruction pipeline
        Stages: Fetch → Decode → Execute → Write-back
        
        Returns:
            (motion_detected, detection_info)
        """
        start_time = time.time()
        
        # Stage 1: Preprocessing (DECODE)
        processed = self.preprocess_frame(frame)
        
        # Stage 2: Frame differencing (EXECUTE - ALU operation)
        frame_diff = self.compute_frame_difference(processed)
        
        if frame_diff is None:
            # First frame - no motion
            return False, {'reason': 'first_frame'}
        
        # Stage 3: Thresholding (EXECUTE - Comparator)
        thresh = self.apply_threshold(frame_diff)
        
        # Stage 4: Morphological operations (EXECUTE)
        morphed = self.morphological_operations(thresh)
        
        # Stage 5: Contour detection (EXECUTE)
        contours = self.find_contours(morphed)
        
        # Stage 6: Contour filtering (EXECUTE - Boolean logic)
        filtered_contours = self.filter_contours(contours)
        
        # Stage 7: Motion decision (WRITE-BACK)
        motion_detected = len(filtered_contours) > 0
        
        # Calculate processing time (CPI equivalent)
        processing_time = time.time() - start_time
        
        # Update metrics
        self.total_frames_processed += 1
        self.total_processing_time += processing_time
        if motion_detected:
            self.motion_detected_count += 1
        
        # Detection info
        detection_info = {
            'motion_detected': motion_detected,
            'num_contours': len(filtered_contours),
            'processing_time_ms': processing_time * 1000,
            'frame_diff': frame_diff,
            'threshold_frame': thresh,
            'morphed_frame': morphed,
            'contours': filtered_contours
        }
        
        return motion_detected, detection_info
    
    def draw_motion_boxes(self, frame: np.ndarray, contours: List[np.ndarray]) -> np.ndarray:
        """
        Draw bounding boxes around detected motion
        
        COA Concept: Output rendering
        """
        output_frame = frame.copy()
        
        for contour in contours:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            
            # Draw rectangle
            cv2.rectangle(output_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Add area label
            area = cv2.contourArea(contour)
            cv2.putText(
                output_frame,
                f"Area: {int(area)}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )
        
        return output_frame
    
    def get_performance_metrics(self) -> dict:
        """
        Get performance metrics
        
        COA Concepts:
        - Average execution time (CPI equivalent)
        - Throughput (frames per second)
        - Detection rate
        """
        if self.total_frames_processed == 0:
            return {
                'frames_processed': 0,
                'average_processing_time_ms': 0,
                'fps': 0,
                'motion_detected_count': 0,
                'detection_rate': 0
            }
        
        avg_processing_time = self.total_processing_time / self.total_frames_processed
        fps = 1.0 / avg_processing_time if avg_processing_time > 0 else 0
        detection_rate = (self.motion_detected_count / self.total_frames_processed) * 100
        
        return {
            'frames_processed': self.total_frames_processed,
            'average_processing_time_ms': avg_processing_time * 1000,
            'fps': fps,
            'motion_detected_count': self.motion_detected_count,
            'detection_rate_percent': detection_rate,
            'total_processing_time_s': self.total_processing_time
        }
    
    def reset_metrics(self):
        """Reset performance metrics"""
        self.total_frames_processed = 0
        self.total_processing_time = 0.0
        self.motion_detected_count = 0
    
    def reset(self):
        """Reset detector state"""
        self.previous_frame = None
        self.reset_metrics()
