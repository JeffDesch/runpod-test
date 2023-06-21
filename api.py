import os

import runpod
from dotenv import load_dotenv

load_dotenv()
runpod.api_key = os.getenv("RUNPOD_API_KEY")


if __name__ == '__main__':
    endpoint = runpod.Endpoint(os.getenv("ENDPOINT_ID"))

    run_request = endpoint.run(
        endpoint_input={"test_input": "1234"}
    )

    print(run_request)

    # Check the status of the endpoint run request
    print(run_request.status())

    # Get the output of the endpoint run request, blocking until the endpoint run is complete.
    print(run_request.output())
