import torch
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler


def preload_model(model_id: str = "stabilityai/stable-diffusion-2-1"):
    scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
    StableDiffusionPipeline.from_pretrained(
        model_id,
        scheduler=scheduler,
        torch_dtype=torch.float16,
    )


if __name__ == '__main__':
    preload_model()