import os
import torch
import cv2
import numpy as np
import base64
from segment_anything import sam_model_registry, SamPredictor

class SAMService:
    _instance = None
    _predictor = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = SAMService()
        return cls._instance

    def __init__(self):
        # Initialize SAM model
        checkpoint_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'checkpoints', 'sam_vit_h_4b8939.pth')
        model_type = "vit_h"
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading SAM model on {device}...")
        
        sam = sam_model_registry[model_type](checkpoint=checkpoint_path)
        sam.to(device=device)
        
        self._predictor = SamPredictor(sam)
        print("SAM model loaded successfully")

    def predict(self, image_path, points=None, labels=None, box=None):
        """
        Run SAM prediction on an image
        :param image_path: Path to the image file
        :param points: List of [x, y] coordinates
        :param labels: List of labels (1 for foreground, 0 for background)
        :param box: List of [x1, y1, x2, y2] coordinates
        :return: Mask as base64 string and other metadata
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image from {image_path}")
            
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Set image for predictor
            self._predictor.set_image(image)
            
            # Prepare inputs
            input_point = np.array(points) if points else None
            input_label = np.array(labels) if labels else None
            
            # Important: SAM expects box to be None if not provided, or an array if provided
            # If box is provided, input_point/label can be None
            
            # Ensure box is a numpy array of shape (4,) if present
            input_box = None
            if box is not None:
                input_box = np.array(box)
                
            print(f"SAM Predict Input - Box: {input_box}, Points: {input_point}")

            # Run inference
            masks, scores, logits = self._predictor.predict(
                point_coords=input_point,
                point_labels=input_label,
                box=input_box,
                multimask_output=False,
            )
            
            print(f"SAM Predict Output - Masks shape: {masks.shape}, Scores: {scores}")

            # Get the best mask (though multimask_output=False returns only one)
            best_mask = masks[0]
            print(f"Best mask True count: {np.sum(best_mask)}")
            
            # Convert mask to base64 image for frontend display
            mask_image = (best_mask * 255).astype(np.uint8)
            # Make it transparent: white for mask, transparent for background
            rgba_mask = np.zeros((mask_image.shape[0], mask_image.shape[1], 4), dtype=np.uint8)
            rgba_mask[best_mask] = [0, 255, 0, 128] # Green with 50% opacity
            
            # Encode mask to png
            _, buffer = cv2.imencode('.png', rgba_mask)
            mask_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # Also save mask to disk (optional, depending on requirement)
            # mask_save_path = image_path.replace('.jpg', '_mask.png')
            # cv2.imwrite(mask_save_path, mask_image)
            
            return {
                'mask': f"data:image/png;base64,{mask_base64}",
                'score': float(scores[0]),
                'shape': best_mask.shape
            }
            
        except Exception as e:
            print(f"SAM Inference Error: {e}")
            raise e
