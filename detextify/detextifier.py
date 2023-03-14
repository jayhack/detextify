from detextify.inpainter import Inpainter
from detextify.inpainter import Inpainter
from detextify.text_detector import TextDetector

import cv2

class Detextifier:
    def __init__(self, text_detector: TextDetector, inpainter: Inpainter):
        self.text_detector = text_detector
        self.inpainter = inpainter

    def detextify(self, in_image_path: str, out_image_path: str, prompt=Inpainter.DEFAULT_PROMPT, max_retries=5):
        to_inpaint_path = in_image_path
        replace_text = None
        for i in range(max_retries):
            print(f"Iteration {i} of {max_retries} for image {in_image_path}:")

            print(f"\tCalling text detector...")
            text_boxes = self.text_detector.detect_text(to_inpaint_path)
            print(f"\tDetected {len(text_boxes)} text boxes.")
            if prompt is not None:
                for text_box in text_boxes:
                    cv2.putText(to_inpaint_path, prompt, (text_box.x, text_box.y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            if not text_boxes:
            if not text_boxes:
                break

            if replace_text is not None:
                for text_box in text_boxes:
                    cv2.putText(to_inpaint_path, replace_text, (text_box.x, text_box.y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            print(f"\tCalling in-painting model...")
            self.inpainter.inpaint(to_inpaint_path, text_boxes, prompt, out_image_path)
            import os
            assert os.path.exists(out_image_path)
            to_inpaint_path = out_image_path

