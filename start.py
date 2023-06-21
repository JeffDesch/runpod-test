import runpod


# Load models


def handler(event):
    # print(event)

    # do the things

    return {"refresh_worker": True, "event_data": event}


runpod.serverless.start({"handler": handler})
