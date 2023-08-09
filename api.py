import os
import time

import runpod
from dotenv import load_dotenv
from file_kit import RemoteFileStore

load_dotenv()
runpod.api_key = os.getenv("RUNPOD_API_KEY")

if __name__ == '__main__':
    job_id = "test_job_01"
    prompt = "A black cat sitting in a field of pumpkins"
    neg_prompt = "nsfw, ugly, flat, low resolution, blurry"
    height = 1024
    width = 1024
    num_steps = 50
    guidance_scale = 7

    endpoint = runpod.Endpoint(os.getenv("ENDPOINT_ID"))
    run_request = endpoint.run(
        endpoint_input={"job_id": job_id,
                        "prompt": prompt,
                        "neg_prompt": neg_prompt,
                        "num_steps": num_steps,
                        "height": height,
                        "width": width,
                        "guidance_scale": guidance_scale,
                        "noise_fraction": 0.8,
                        "torch_optimize": False}
    )

    # The .output() will automatically poll-and-wait for the worker to finish
    message = run_request.output().get("message", "runpod error")
    if message != "success":
        print(message)
    else:
        s3_client = RemoteFileStore()

        local_path = os.path.join("jobs", job_id)
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        image_path = os.path.join(local_path, "image.png")
        log_path = os.path.join(local_path, "log.txt")
        prev_path = os.path.join(local_path, "thumbnail.gif")

        remote_path = "/".join(["jobs", job_id, "image.png"])
        s3_client.download_to_dir(remote_path, image_path)
        s3_client.delete(remote_path)

        remote_path = "/".join(["jobs", job_id, "log.txt"])
        s3_client.download_to_dir(remote_path, log_path)
        s3_client.delete(remote_path)
