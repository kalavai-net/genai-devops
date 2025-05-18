import httpx


def speech_to_text(audio_file, base_url, api_key):
    client = httpx.Client(base_url=base_url)
    files = {
        'file': audio_file
    }
    data = {
        "model": "tiny-en"
    }
    response = client.post(
        "audio/transcriptions",
        data=data,
        files=files,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=60
    )
    print("----->", response.text)
    return response.json()["text"]