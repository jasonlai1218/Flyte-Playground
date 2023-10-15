import requests
import tempfile
from flytekit import task, workflow
from flytekit.types.file import FlyteFile, JPEGImageFile


@task
def get_image(image_url: str) -> str:
    response = requests.get(image_url, stream=True)
    temp_file = tempfile.NamedTemporaryFile(dir='/tmp/', delete=False, suffix=".png", prefix='downloaded')
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            temp_file.write(chunk)
    return temp_file.name

@workflow
def wf(image_url: str = "https://i.imgur.com/GtolBwW.png") -> str:
    png_image: JPEGImageFile = get_image(image_url=image_url)
    print(png_image)
    return png_image

print(f"my_workflow output: {wf()}")