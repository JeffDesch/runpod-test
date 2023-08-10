from diffusers import DiffusionPipeline
import torch


def preload_model():
    base = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16,
        variant="fp16",
        cache_dir="./models",
        use_safetensors=True
    )

    base.unet = torch.compile(base.unet, mode="reduce-overhead", fullgraph=True)

    refiner = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-refiner-1.0",
        text_encoder_2=base.text_encoder_2,
        vae=base.vae,
        torch_dtype=torch.float16,
        cache_dir="./models",
        use_safetensors=True,
        variant="fp16",
    )

    refiner.unet = torch.compile(refiner.unet, mode="reduce-overhead", fullgraph=True)


if __name__ == '__main__':
    preload_model()
