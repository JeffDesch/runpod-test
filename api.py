import os
import json

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

    if run_request is not None:
        with open("log.txt", "w") as file:
            json.dump(run_request, file)

        output = run_request.get("data", None)

        if output is not None:
            audio = output

            audio_path = os.path.join(".", "audio")
            if not os.path.exists(audio_path):
                os.makedirs(audio_path)

            save(audio, os.path.join(audio_path, "voice.mp3"))

