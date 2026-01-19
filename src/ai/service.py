import cv2
import numpy as np
from PIL import Image
from starlette.concurrency import run_in_threadpool

from ai.ai_client import AIClient


class ImageAnalysisService:
    def __init__(self, ai: AIClient):
        self.ai = ai

    async def analyze_and_describe(self, image: Image.Image) -> str:
        analysis = await run_in_threadpool(self._analyze_image, image)
        description = await self.ai.generate(self._generate_description(analysis))
        return description

    # --- private ---

    def _analyze_image(self, image: Image.Image) -> dict:
        img = np.array(image)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

        mean_lab = lab.mean(axis=(0, 1))
        brightness = mean_lab[0]

        brightness_level = (
            "light" if brightness > 180 else "medium" if brightness > 120 else "dark"
        )

        undertone = "warm" if mean_lab[2] > mean_lab[1] else "cool"

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        contrast = gray.std()

        contrast_level = (
            "low" if contrast < 30 else "medium" if contrast < 60 else "high"
        )

        return {
            "brightness_level": brightness_level,
            "brightness": float(brightness),
            "undertone": undertone,
            "contrast_level": contrast_level,
            "contrast": float(contrast),
            "mean_color_lab": mean_lab.tolist(),
        }

    def _generate_description(self, data: dict) -> str:
        return f"""
Данные анализа:
- Подтон кожи: {data["undertone"]}
- Яркость кожи: {data["brightness_level"]}
- Контраст внешности: {data["contrast_level"]}
- LAB цвет кожи: {data["mean_color_lab"]}
"""
