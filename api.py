import json
import os
import base64

import runpod
from dotenv import load_dotenv
from elevenlabs import save

load_dotenv()
runpod.api_key = os.getenv("RUNPOD_API_KEY")


if __name__ == '__main__':
    endpoint = runpod.Endpoint(os.getenv("ENDPOINT_ID"))

    run_request = endpoint.run_sync(
        endpoint_input={"text": """Hello? Testing 1, 2, 3..."""}
    )

    encoded_audio = run_request.get("output").get("data", None)

    if encoded_audio is not None:
        audio = base64.b64decode(encoded_audio)

        audio_path = os.path.join(".", "audio")
        if not os.path.exists(audio_path):
            os.makedirs(audio_path)

        with open(os.path.join(audio_path, "log.txt"), "w") as file:
            json.dump(run_request, file)

        save(audio, os.path.join(audio_path, "voice.mp3"))

