import base64
import os
import requests
from datetime import datetime

def list_stability_engines():
    """
    List models available on Stability.ai
    https://platform.stability.ai/pricing
    """
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    url = f"{api_host}/v1/engines/list"

    api_key = os.getenv("STABILITY_API_KEY")
    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.get(url, headers={
        "Authorization": f"Bearer {api_key}"
    })

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    # Do something with the payload...
    payload = response.json()
    return payload

def generate_stability_image(
        prompt, n_images=1,
        engine_id = "stable-diffusion-v1-6",
        filename=None, filepath='../ai_images/'
        ):
    
    """
    Generate images from Stable Diffusion
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    
    api_host = 'https://api.stability.ai'
    api_key = os.getenv("STABILITY_API_KEY")

    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": prompt
                }
            ],
            "samples": n_images,
            # "cfg_scale": 7,
            # "height": 512,
            # "width": 512,
            # "steps": 30,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    if len(data["artifacts"]) == 1:
        full_filename = f"{filepath}/{filename if filename else engine_id}_{timestamp}.png"
        with open(full_filename, "wb") as f:
            f.write(base64.b64decode(image["base64"]))
        print(f'Image saved as {full_filename}')
    elif len(data["artifacts"]) > 1:
        for i, image in enumerate(data["artifacts"]):
            full_filename = f"{filepath}/{filename if filename else engine_id}_{timestamp}_{i}.png"
            with open(full_filename, "wb") as f:
                f.write(base64.b64decode(image["base64"]))
            print(f'Image saved as {full_filename}')