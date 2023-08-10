import os
import time
import datetime
import runpod
from file_kit import RemoteFileStore
from diffusers import DiffusionPipeline
import torch

# preload models
base = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    cache_dir="./models",
    local_files_only=True,
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True
)
refiner = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0",
    cache_dir="./models",
    local_files_only=True,
    text_encoder_2=base.text_encoder_2,
    vae=base.vae,
    torch_dtype=torch.float16,
    use_safetensors=True,
    variant="fp16",
)


def handler(payload):
    input_params = payload.get("input", None)
    if input_params is None:
        return {"refresh_worker": True, "status": "payload error"}
    job_id = input_params.get("job_id", None)
    prompt = input_params.get("prompt", None)
    if job_id is None or prompt is None:
        return {"refresh_worker": True, "status": "input error"}
    image_h = input_params.get("height", 1024)
    image_w = input_params.get("width", 1024)
    num_steps = input_params.get("num_steps", 50)
    guidance_scale = input_params.get("guidance_scale", 7)
    neg_prompt = input_params.get("neg_prompt", "No NSFW")
    noise_frac = input_params.get("noise_fraction", 0.8)
    offload_cpu = input_params.get("offload_cpu", False)
    torch_optimize = input_params.get("torch_optimize", False)

    begin = time.perf_counter()

    if not offload_cpu:
        if torch_optimize:
            base.unet = torch.compile(base.unet, mode="reduce-overhead", fullgraph=True)
            refiner.unet = torch.compile(refiner.unet, mode="reduce-overhead", fullgraph=True)
        base.to("cuda")
        refiner.to("cuda")
    else:
        base.enable_model_cpu_offload()
        refiner.enable_model_cpu_offload()

    print(f"Generating Image Latent...")
    start = time.perf_counter()
    image, *_ = base(
        prompt=prompt,
        denoising_end=noise_frac,
        output_type="latent",
        num_inference_steps=num_steps,
        num_images_per_prompt=1,
        negative_prompt=neg_prompt,
        guidance_scale=guidance_scale,
    ).images
    stop = time.perf_counter()
    duration = datetime.timedelta(seconds=stop - start)
    print(f"\tCreated Image Latent in: {duration}")
    print(f"Generating Final Image...")
    start = time.perf_counter()
    image, *_ = refiner(
        prompt=prompt,
        num_inference_steps=num_steps,
        denoising_start=noise_frac,
        image=image,
    ).images
    stop = time.perf_counter()
    duration = datetime.timedelta(seconds=stop - start)
    print(f"\tCreated Final Image in: {duration}")
    image.save("image.png")
    end = time.perf_counter()
    print(f"\nJob Completed in: {datetime.timedelta(seconds=end - begin)}")

    s3_client = RemoteFileStore()
    job_path = os.path.join("jobs", job_id)
    image_path = os.path.join(job_path, "image.png")
    s3_client.upload("image.png", image_path)
    log_path = os.path.join(job_path, "log.txt")
    s3_client.upload("log.txt", log_path)

    return {"refresh_worker": False, "status": "success"}


runpod.serverless.start({"handler": handler})
