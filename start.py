import os
import base64
import runpod
from elevenlabs import set_api_key, generate

# Load models
set_api_key(os.getenv("XI_API_KEY"))


def handler(event):

    input_data = event.get("input", None)
    if input_data is not None:
        text = input_data.get("text")
    else:
        text = "Test text is missing!"

    audio = generate(
        text=text,
        voice="Rachel",
        model="eleven_monolingual_v1",
    )

    encoded_audio = base64.b64encode(audio)
    encoded_audio = str(encoded_audio, 'ascii')

    return {"refresh_worker": True, "data": encoded_audio}


runpod.serverless.start({"handler": handler})
