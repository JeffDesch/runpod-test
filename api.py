import os

import runpod
from dotenv import load_dotenv

load_dotenv()
runpod.api_key = os.getenv("RUNPOD_API_KEY")

endpoint = runpod.Endpoint(os.getenv("ENDPOINT_ID"))


if __name__ == '__main__':

    run_request = endpoint.run(
        {"test_input": "1234"}
    )

    # Check the status of the endpoint run request
    print(run_request.status())

    # Get the output of the endpoint run request, blocking until the endpoint run is complete.
    print(run_request.output())

