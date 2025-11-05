"""
Face Recognition Module
Demonstrates COA concepts: Cache Memory, Pattern Matching, Data Retrieval

COA Concepts Implemented:
- Face database with LRU cache
- Pattern recognition algorithm
- Cache hit/miss tracking
- Fast lookup using hash-based indexing
"""

import cv2
import numpy as np
import os
import pickle
from typing import List, Tuple, Optional
import time


class FaceRecognizer:
    """
    Face Recognition System with Cache Integration
    
    COA Concepts:
    - Face database (secondary storage simulation)
    - LRU cache for face encodings (cache memory)
    - Fast lookup (hash table indexing)
    - Pattern matching algorithm
    """
    
    def __init__(self, config: dict, cache):
        """
        Initialize face recognizer
        
        Args:
            config: Configuration dictionary
            cache: LRU cache instance from memory management
        """
        self.config = config
        self.cache = cache  # L2 cache for face encodings
        
        self.tolerance = config.get('tolerance', 0.6)
        self.model = config.get('model', 'hog')
        self.detection_interval = config.get('detection_interval', 1)  # Check every frame for maximum responsiveness
        
        # Face database (simulates secondary storage)
        self.known_face_encodings = []
        self.known_face_names = []
        self.face_database_path = config.get('authorized_faces_path', 'storage/authorized_faces')
        
        # Haar Cascade for face detection (alternative method)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Performance metrics
        self.total_recognitions = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.recognition_time_total = 0.0
        self.frame_counter = 0
        
        # Stability and accuracy improvements
        self.face_history = []  # Track face detections over time
        self.history_length = 5  # Number of frames to track
        self.min_confidence_frames = 3  # Minimum frames to confirm a face
        self.last_stable_faces = []  # Last confirmed face locations
        self.last_stable_names = []  # Last confirmed face names
        
        # Try to use face_recognition library if available
        self.use_face_recognition = False
        try:
            import face_recognition
            self.face_recognition = face_recognition
            self.use_face_recognition = True
            print("Using face_recognition library for advanced recognition")
        except ImportError:
            print("face_recognition not available, using OpenCV Haar Cascade")
    
    def load_authorized_faces(self):
        """
        Load authorized faces from storage
        
        COA Concept: Loading data from secondary storage to main memory
        Simulates disk I/O operations
        """
        if not os.path.exists(self.face_database_path):
            os.makedirs(self.face_database_path, exist_ok=True)
            print(f"Created face database directory: {self.face_database_path}")
            return
        
        # Scan directory for face images
        for filename in os.listdir(self.face_database_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                filepath = os.path.join(self.face_database_path, filename)
                name = os.path.splitext(filename)[0]
                
                try:
                    # Load image from disk (disk I/O)
                    image = cv2.imread(filepath)
                    
                    if self.use_face_recognition:
                        # Convert BGR to RGB
                        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        
                        # Encode face (computationally expensive)
                        encodings = self.face_recognition.face_encodings(rgb_image)
                        
                        if len(encodings) > 0:
                            encoding = encodings[0]
                            self.known_face_encodings.append(encoding)
                            self.known_face_names.append(name)
                            
                            # Store in cache for fast access
                            cache_key = f"face_encoding_{name}"
                            self.cache.put(cache_key, encoding)
                            
                            print(f"Loaded authorized face: {name}")
                    else:
                        # Store image directly for Haar Cascade method
                        self.known_face_encodings.append(image)
                        self.known_face_names.append(name)
                        print(f"Loaded authorized face (Haar): {name}")
                        
                except Exception as e:
                    print(f"Error loading face {filename}: {e}")
        
        print(f"Total authorized faces loaded: {len(self.known_face_names)}")
    
    def save_face_encoding(self, name: str, encoding: np.ndarray, image: np.ndarray):
        """
        Save face encoding to database
        
        COA Concept: Writing data to secondary storage
        """
        # Save image to disk
        filepath = os.path.join(self.face_database_path, f"{name}.jpg")
        cv2.imwrite(filepath, image)
        
        # Add to in-memory database
        self.known_face_encodings.append(encoding)
        self.known_face_names.append(name)
        
        # Store in cache
        cache_key = f"face_encoding_{name}"
        self.cache.put(cache_key, encoding)
        
        print(f"Saved face encoding for: {name}")
    
    def detect_faces_opencv(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces using OpenCV Haar Cascade
        
        COA Concept: Pattern matching algorithm
        
        Returns:
            List of (x, y, w, h) face locations
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply histogram equalization to improve contrast
        gray = cv2.equalizeHist(gray)
        
        # Apply Gaussian blur to reduce noise
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Detect faces with optimized parameters for accuracy
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.08,      # Balanced scale factor for accuracy vs speed
            minNeighbors=4,        # Higher threshold for better accuracy (was 2)
            minSize=(30, 30),      # Reasonable minimum size to avoid false positives
            maxSize=(400, 400),    # Maximum size limit
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # Filter overlapping detections using Non-Maximum Suppression
        faces = self._filter_overlapping_faces(faces)
        
        return faces
    
    def _filter_overlapping_faces(self, faces: np.ndarray) -> np.ndarray:
        """
        Filter overlapping face detections to prevent duplicates
        Uses Non-Maximum Suppression (NMS)
        """
        if len(faces) == 0:
            return faces
        
        # Convert to (x1, y1, x2, y2) format
        boxes = []
        for (x, y, w, h) in faces:
            boxes.append([x, y, x + w, y + h])
        boxes = np.array(boxes)
        
        # Calculate areas
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]
        areas = (x2 - x1) * (y2 - y1)
        
        # Sort by area (larger boxes first)
        indices = np.argsort(areas)[::-1]
        
        keep = []
        while len(indices) > 0:
            # Keep the largest box
            current = indices[0]
            keep.append(current)
            
            if len(indices) == 1:
                break
            
            # Calculate IoU with remaining boxes
            xx1 = np.maximum(x1[current], x1[indices[1:]])
            yy1 = np.maximum(y1[current], y1[indices[1:]])
            xx2 = np.minimum(x2[current], x2[indices[1:]])
            yy2 = np.minimum(y2[current], y2[indices[1:]])
            
            w = np.maximum(0, xx2 - xx1)
            h = np.maximum(0, yy2 - yy1)
            
            overlap = (w * h) / areas[indices[1:]]
            
            # Keep only boxes with low overlap (< 30%)
            indices = indices[np.concatenate([[0], np.where(overlap < 0.3)[0] + 1])]
            indices = indices[1:]
        
        # Return filtered faces
        return faces[keep]
    
    def recognize_faces(self, frame: np.ndarray) -> Tuple[List[str], List[Tuple]]:
        """
        Recognize faces in frame with temporal smoothing
        
        COA Concepts:
        - Cache lookup (check cache first)
        - Pattern matching (face comparison)
        - Cache hit/miss tracking
        - Temporal filtering for stability
        
        Returns:
            (names, face_locations)
        """
        start_time = time.time()
        
        # Only process every Nth frame (optimization)
        self.frame_counter += 1
        if self.frame_counter % self.detection_interval != 0:
            # Return last stable results instead of empty
            return self.last_stable_names.copy(), self.last_stable_faces.copy()
        
        names = []
        locations = []
        
        if self.use_face_recognition and len(self.known_face_encodings) > 0:
            # Use face_recognition library
            names, locations = self._recognize_with_face_recognition(frame)
        else:
            # Use OpenCV Haar Cascade
            names, locations = self._recognize_with_opencv(frame)
        
        # Apply temporal smoothing to reduce fluctuations
        names, locations = self._apply_temporal_smoothing(names, locations)
        
        # Update performance metrics
        recognition_time = time.time() - start_time
        self.total_recognitions += 1
        self.recognition_time_total += recognition_time
        
        return names, locations
        self.recognition_time_total += recognition_time
        
        return names, locations
    
    def _recognize_with_face_recognition(self, frame: np.ndarray) -> Tuple[List[str], List[Tuple]]:
        """
        Recognize faces using face_recognition library
        
        COA Concept: Cache-aware algorithm
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find faces in frame
        face_locations = self.face_recognition.face_locations(rgb_frame, model=self.model)
        
        if len(face_locations) == 0:
            return [], []
        
        # Encode faces
        face_encodings = self.face_recognition.face_encodings(rgb_frame, face_locations)
        
        names = []
        
        for face_encoding in face_encodings:
            # Try cache lookup first (cache hit optimization)
            cache_key = self._generate_encoding_hash(face_encoding)
            cached_name = self.cache.get(cache_key)
            
            if cached_name is not None:
                # Cache HIT
                self.cache_hits += 1
                names.append(cached_name)
            else:
                # Cache MISS - perform full comparison
                self.cache_misses += 1
                name = self._match_face(face_encoding)
                names.append(name)
                
                # Store in cache for future lookups
                if name != "Unknown":
                    self.cache.put(cache_key, name)
        
        return names, face_locations
    
    def _recognize_with_opencv(self, frame: np.ndarray) -> Tuple[List[str], List[Tuple]]:
        """
        Recognize faces using OpenCV Haar Cascade
        (Simplified version without encoding comparison)
        """
        faces = self.detect_faces_opencv(frame)
        
        names = []
        locations = []
        
        for (x, y, w, h) in faces:
            # For Haar Cascade, we just detect presence
            # Real recognition requires training or template matching
            names.append("Detected")
            locations.append((y, x+w, y+h, x))  # Convert to face_recognition format
        
        return names, locations
    
    def _apply_temporal_smoothing(self, names: List[str], locations: List[Tuple]) -> Tuple[List[str], List[Tuple]]:
        """
        Apply temporal smoothing to reduce fluctuations in face detection
        
        Uses a voting system over recent frames to confirm face detections
        """
        # Add current detection to history
        self.face_history.append({
            'names': names.copy(),
            'locations': locations.copy(),
            'count': len(names)
        })
        
        # Keep only recent history
        if len(self.face_history) > self.history_length:
            self.face_history.pop(0)
        
        # If we don't have enough history yet, use current detection
        if len(self.face_history) < self.min_confidence_frames:
            self.last_stable_faces = locations.copy()
            self.last_stable_names = names.copy()
            return names, locations
        
        # Count face detections across recent frames
        face_counts = [frame_data['count'] for frame_data in self.face_history]
        
        # Use median count to determine stable face count (reduces fluctuation)
        stable_count = int(np.median(face_counts))
        
        # If current detection matches stable count (or is close), accept it
        current_count = len(names)
        
        if abs(current_count - stable_count) <= 1:
            # Accept current detection
            self.last_stable_faces = locations.copy()
            self.last_stable_names = names.copy()
            return names, locations
        else:
            # Return last stable detection to prevent flickering
            return self.last_stable_names.copy(), self.last_stable_faces.copy()
    
    def _match_face(self, face_encoding: np.ndarray) -> str:
        """
        Match face encoding against known faces
        
        COA Concept: Pattern matching with distance calculation
        Uses Euclidean distance (arithmetic operations)
        """
        if len(self.known_face_encodings) == 0:
            return "Unknown"
        
        # Compare with all known faces
        matches = self.face_recognition.compare_faces(
            self.known_face_encodings,
            face_encoding,
            tolerance=self.tolerance
        )
        
        # Calculate distances (similarity metric)
        face_distances = self.face_recognition.face_distance(
            self.known_face_encodings,
            face_encoding
        )
        
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                return self.known_face_names[best_match_index]
        
        return "Unknown"
    
    def _generate_encoding_hash(self, encoding: np.ndarray) -> str:
        """
        Generate hash key for face encoding
        
        COA Concept: Hash function for cache indexing
        """
        # Use first few values as hash key (simplified)
        hash_values = encoding[:5]
        hash_key = "face_" + "_".join([f"{v:.2f}" for v in hash_values])
        return hash_key
    
    def draw_face_boxes(self, frame: np.ndarray, names: List[str], locations: List[Tuple]) -> np.ndarray:
        """
        Draw bounding boxes and names on detected faces
        
        COA Concept: Output rendering
        """
        output_frame = frame.copy()
        
        for name, (top, right, bottom, left) in zip(names, locations):
            # Determine color based on recognition
            if name == "Unknown" or name == "Detected":
                color = (0, 0, 255)  # Red for unknown
            else:
                color = (0, 255, 0)  # Green for known
            
            # Draw rectangle
            cv2.rectangle(output_frame, (left, top), (right, bottom), color, 2)
            
            # Draw label background
            cv2.rectangle(output_frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            
            # Draw name
            cv2.putText(
                output_frame,
                name,
                (left + 6, bottom - 6),
                cv2.FONT_HERSHEY_DUPLEX,
                0.6,
                (255, 255, 255),
                1
            )
        
        return output_frame
    
    def is_unknown_face_detected(self, names: List[str]) -> bool:
        """
        Check if any unknown faces detected
        
        COA Concept: Boolean logic for alarm trigger
        """
        return "Unknown" in names
    
    def get_performance_metrics(self) -> dict:
        """
        Get face recognition performance metrics
        
        COA Concepts:
        - Cache hit rate (cache performance)
        - Average recognition time
        - Recognition throughput
        """
        if self.total_recognitions == 0:
            return {
                'total_recognitions': 0,
                'cache_hits': 0,
                'cache_misses': 0,
                'cache_hit_rate': 0,
                'average_recognition_time_ms': 0,
                'known_faces_count': len(self.known_face_names)
            }
        
        cache_hit_rate = (self.cache_hits / (self.cache_hits + self.cache_misses)) * 100 if (self.cache_hits + self.cache_misses) > 0 else 0
        avg_time = self.recognition_time_total / self.total_recognitions
        
        return {
            'total_recognitions': self.total_recognitions,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'cache_hit_rate_percent': cache_hit_rate,
            'average_recognition_time_ms': avg_time * 1000,
            'known_faces_count': len(self.known_face_names),
            'using_advanced_recognition': self.use_face_recognition
        }
    
    def reset_metrics(self):
        """Reset performance metrics"""
        self.total_recognitions = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.recognition_time_total = 0.0
        self.frame_counter = 0
