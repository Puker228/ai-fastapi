import httpx
from fastapi import APIRouter, Depends, File, Request, UploadFile
from PIL import Image

from ai.ai_client import AIClient
from ai.schemas import AnalyzeResponse
from ai.service import ImageAnalysisService

router = APIRouter()


def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client


def get_image_service(
    client: httpx.AsyncClient = Depends(get_http_client),
) -> ImageAnalysisService:
    return ImageAnalysisService(AIClient(client))


@router.post(path="/analyze", response_model=AnalyzeResponse)
async def analyze_image(
    file: UploadFile = File(...),
    service: ImageAnalysisService = Depends(get_image_service),
):
    image = Image.open(file.file).convert("RGB")
    description = await service.analyze_and_describe(image)
    return AnalyzeResponse(description=description)
