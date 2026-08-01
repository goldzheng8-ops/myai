from pydantic import BaseModel

class PipelineConfig(BaseModel):

    deduplicate:bool=True

    download_images:bool=False

    image_dir:str="images"

    download_files:bool=False

    file_dir:str="downloads"