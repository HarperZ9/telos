import requests


def run(demoValue: str) -> str:
    response = requests.get(
        "https://example.invalid/synthetic",
        params={"demo": demoValue},
        timeout=1,
    )
    return response.text
