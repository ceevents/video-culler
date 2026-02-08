"""Focus detection using Laplacian variance algorithm."""
import cv2
import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class FocusScore:
    """Focus score for a single frame."""
    frame_number: int
    timestamp: float
    score: float  # 0-100
    variance: float  # Raw Laplacian variance


class FocusDetector:
    """Detect focus quality in video frames using Laplacian variance."""
    
    def __init__(self, threshold: float = 100.0):
        """
        Initialize focus detector.
        
        Args:
            threshold: Laplacian variance threshold for focus detection
        """
        self.threshold = threshold
        self._min_variance = None
        self._max_variance = None
    
    def calculate_laplacian_variance(self, frame: np.ndarray) -> float:
        """
        Calculate Laplacian variance for a frame.
        
        Args:
            frame: BGR image frame
            
        Returns:
            Laplacian variance value
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate Laplacian
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        
        # Calculate variance
        variance = laplacian.var()
        
        return variance
    
    def normalize_score(self, variance: float) -> float:
        """
        Normalize variance to 0-100 scale.
        
        Args:
            variance: Raw Laplacian variance
            
        Returns:
            Normalized score (0-100)
        """
        if self._min_variance is None or self._max_variance is None:
            # If we haven't calibrated yet, use a simple threshold-based approach
            return min(100.0, (variance / self.threshold) * 100.0)
        
        # Normalize using min-max scaling
        if self._max_variance == self._min_variance:
            return 50.0
        
        normalized = ((variance - self._min_variance) / 
                     (self._max_variance - self._min_variance)) * 100.0
        
        return max(0.0, min(100.0, normalized))
    
    def analyze_frame(self, frame: np.ndarray, frame_number: int, 
                     timestamp: float) -> FocusScore:
        """
        Analyze a single frame for focus quality.
        
        Args:
            frame: BGR image frame
            frame_number: Frame index
            timestamp: Timestamp in seconds
            
        Returns:
            FocusScore object
        """
        variance = self.calculate_laplacian_variance(frame)
        score = self.normalize_score(variance)
        
        return FocusScore(
            frame_number=frame_number,
            timestamp=timestamp,
            score=score,
            variance=variance
        )
    
    def analyze_video(self, video_path: str, 
                     sample_rate: int = 1,
                     progress_callback: Optional[callable] = None) -> List[FocusScore]:
        """
        Analyze focus quality for entire video.
        
        Args:
            video_path: Path to video file
            sample_rate: Analyze every Nth frame (1 = every frame)
            progress_callback: Optional callback(current, total) for progress
            
        Returns:
            List of FocusScore objects
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        scores = []
        frame_number = 0
        variances = []
        
        # First pass: collect all variances for normalization
        print(f"First pass: calculating variances for {total_frames} frames...")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_number % sample_rate == 0:
                variance = self.calculate_laplacian_variance(frame)
                variances.append(variance)
            
            frame_number += 1
            
            if progress_callback and frame_number % 100 == 0:
                progress_callback(frame_number, total_frames * 2)  # *2 for two passes
        
        # Calibrate normalization
        if variances:
            self._min_variance = min(variances)
            self._max_variance = max(variances)
            print(f"Variance range: {self._min_variance:.2f} - {self._max_variance:.2f}")
        
        # Second pass: calculate normalized scores
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frame_number = 0
        variance_idx = 0
        
        print(f"Second pass: calculating normalized scores...")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_number % sample_rate == 0:
                timestamp = frame_number / fps
                variance = variances[variance_idx]
                score = self.normalize_score(variance)
                
                scores.append(FocusScore(
                    frame_number=frame_number,
                    timestamp=timestamp,
                    score=score,
                    variance=variance
                ))
                variance_idx += 1
            
            frame_number += 1
            
            if progress_callback and frame_number % 100 == 0:
                progress_callback(total_frames + frame_number, total_frames * 2)
        
        cap.release()
        
        return scores
    
    def get_best_frames(self, scores: List[FocusScore], 
                       top_n: int = 10) -> List[FocusScore]:
        """
        Get the N frames with best focus scores.
        
        Args:
            scores: List of FocusScore objects
            top_n: Number of top frames to return
            
        Returns:
            List of top N FocusScore objects, sorted by score descending
        """
        return sorted(scores, key=lambda x: x.score, reverse=True)[:top_n]
    
    def get_poor_focus_segments(self, scores: List[FocusScore], 
                               threshold: float = 30.0,
                               min_duration: float = 1.0) -> List[Tuple[float, float]]:
        """
        Identify segments with poor focus quality.
        
        Args:
            scores: List of FocusScore objects
            threshold: Score below which is considered poor focus
            min_duration: Minimum duration (seconds) for a segment
            
        Returns:
            List of (start_time, end_time) tuples
        """
        segments = []
        current_segment_start = None
        
        for i, score in enumerate(scores):
            if score.score < threshold:
                if current_segment_start is None:
                    current_segment_start = score.timestamp
            else:
                if current_segment_start is not None:
                    duration = score.timestamp - current_segment_start
                    if duration >= min_duration:
                        segments.append((current_segment_start, score.timestamp))
                    current_segment_start = None
        
        # Handle case where video ends with poor focus
        if current_segment_start is not None:
            segments.append((current_segment_start, scores[-1].timestamp))
        
        return segments


def analyze_focus(video_path: str, sample_rate: int = 1) -> List[FocusScore]:
    """
    Convenience function to analyze video focus.
    
    Args:
        video_path: Path to video file
        sample_rate: Analyze every Nth frame
        
    Returns:
        List of FocusScore objects
    """
    detector = FocusDetector()
    return detector.analyze_video(video_path, sample_rate)
