import json
import runpod
import torch
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler

# Load models
model_id = "stabilityai/stable-diffusion-2-1"
scheduler = EulerDiscreteScheduler.from_pretrained(model_id,
                                                   subfolder="scheduler",
                                                   local_files_only=True)
pipeline = StableDiffusionPipeline.from_pretrained(
    model_id,
    scheduler=scheduler,
    torch_dtype=torch.float16,
    local_files_only=True
)


def handler(payload):

    input_params = payload.get("input", None)
    if input is not None:
        image = pipeline(
            prompt=input_params.get("prompt", ""),
            height=512,
            width=768,
            num_inference_steps=input_params.get("epochs", 50),
            num_images_per_prompt=1,
            negative_prompt="No NSFW",
        ).images[0]
        image_s = json.dumps(image)
    else:
        image_s = ""

    return {"refresh_worker": True, "image": image_s}


runpod.serverless.start({"handler": handler})
