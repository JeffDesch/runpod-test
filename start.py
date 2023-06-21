import runpod


# Load models


def handler(event):
    # print(event)

    # do the things

    return {"event_data": event}


runpod.serverless.start({"handler": handler})
