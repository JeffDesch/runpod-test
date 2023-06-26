import os
import json

import runpod
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
runpod.api_key = os.getenv("RUNPOD_API_KEY")


if __name__ == '__main__':
    endpoint = runpod.Endpoint(os.getenv("ENDPOINT_ID"))

    run_request = endpoint.run(
        endpoint_input={"prompt": "A black cat sitting in a field of pumpkins",
                        "epochs": 50}
    )

    image_path = os.path.join(".", "images")
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    output_data = run_request.output().get("output")
    image = Image.open(json.loads(output_data.get("image")))
    image.save(os.path.join(image_path, "image.png"))

