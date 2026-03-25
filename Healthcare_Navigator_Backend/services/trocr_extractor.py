from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

processor = None
model = None
device = "cuda" if torch.cuda.is_available() else "cpu"


def load_model():
    global processor, model
    if processor is None or model is None:
        processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
        model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
        model.to(device)


def extract_text_trocr(image_path: str) -> dict:
    try:
        load_model()  # load only when needed

        image = Image.open(image_path).convert("RGB")

        pixel_values = processor(images=image, return_tensors="pt").pixel_values.to(device)

        generated_ids = model.generate(pixel_values)

        text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        print("OCR TEXT:", text)

        return {"raw_text": text}

    except Exception as e:
        return {"error": str(e)}