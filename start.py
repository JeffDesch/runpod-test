import os
import runpod
from elevenlabs import set_api_key, generate

# Load models
set_api_key(os.getenv("XI_API_KEY"))


def handler(event):

    audio = generate(
        text=event.get("text"),
        voice="Rachel",
        model="eleven_monolingual_v1",
    )

    return {"refresh_worker": True, "data": audio}


runpod.serverless.start({"handler": handler})
