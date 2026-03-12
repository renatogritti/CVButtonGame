import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import os
from config import *

class CVHandler:
    def __init__(self):
        # Path to the model file
        model_path = os.path.join('assets', 'hand_landmarker.task')
        
        # Initialize the hand landmarker
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.5
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        
        self.cap = cv2.VideoCapture(0)
        
        # Smoothing and state
        self.finger_pos = [0, 0] # Current smoothed position
        self.raw_pinch = False
        self.is_pinching = False
        self.pinch_frames_counter = 0

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        detection_result = self.detector.detect(mp_image)
        
        self.raw_pinch = False
        
        if detection_result.hand_landmarks:
            hand_landmarks = detection_result.hand_landmarks[0]
            index_tip = hand_landmarks[8]
            thumb_tip = hand_landmarks[4]
            
            # 1. Coordinate Fetch with Safe Zone Mapping
            # Maps camera [margin, 1-margin] to field [0, 1]
            raw_x = index_tip.x
            raw_y = index_tip.y
            
            # Linear mapping: f(t) = (t - margin) / (1 - 2*margin)
            map_x = (raw_x - CV_SAFE_ZONE) / (1 - 2 * CV_SAFE_ZONE)
            map_y = (raw_y - CV_SAFE_ZONE) / (1 - 2 * CV_SAFE_ZONE)
            
            # Clamp to [0, 1] then scale to screen
            target_x = int(np.clip(map_x, 0, 1) * WIDTH)
            target_y = int(np.clip(map_y, 0, 1) * HEIGHT)
            
            # 2. Apply EMA Smoothing
            # New = (1-a) * Old + a * Target
            self.finger_pos[0] = int((1 - CV_SMOOTH_FACTOR) * self.finger_pos[0] + CV_SMOOTH_FACTOR * target_x)
            self.finger_pos[1] = int((1 - CV_SMOOTH_FACTOR) * self.finger_pos[1] + CV_SMOOTH_FACTOR * target_y)
            
            # 3. Pinch Detection with Hysteresis
            dist = np.sqrt((index_tip.x - thumb_tip.x)**2 + (index_tip.y - thumb_tip.y)**2)
            
            if not self.is_pinching:
                if dist < PINCH_THRESHOLD:
                    self.raw_pinch = True
            else:
                if dist < PINCH_RELEASE_THRESHOLD:
                    self.raw_pinch = True
            
            # 4. Stabilization (Debounce)
            if self.raw_pinch != self.is_pinching:
                self.pinch_frames_counter += 1
                if self.pinch_frames_counter >= PINCH_STABILIZATION_FRAMES:
                    self.is_pinching = self.raw_pinch
                    self.pinch_frames_counter = 0
            else:
                self.pinch_frames_counter = 0
            
            # Visualization
            color = (0, 255, 0) if not self.is_pinching else (0, 0, 255)
            thickness = 2 if not self.is_pinching else 4
            ix, iy = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])
            tx, ty = int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0])
            cv2.line(frame, (ix, iy), (tx, ty), color, thickness)
            for lm in hand_landmarks:
                cx, cy = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
                cv2.circle(frame, (cx, cy), 3, color, -1)
        else:
            if self.is_pinching:
                self.pinch_frames_counter += 1
                if self.pinch_frames_counter >= PINCH_STABILIZATION_FRAMES:
                    self.is_pinching = False
                    self.pinch_frames_counter = 0
        
        return frame

    def close(self):
        self.cap.release()
