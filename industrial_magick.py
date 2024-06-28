import folder_paths
import numpy as np
import os
import subprocess
import torch
from PIL import Image, ImageOps, ImageSequence

comfy_path = os.path.dirname(folder_paths.__file__)
tmp_path = f'{comfy_path}/temp'

def read_image_from_path(image_path):
    img = Image.open(image_path)
    image = None
    for i in ImageSequence.Iterator(img):
        i = ImageOps.exif_transpose(i)
        if i.mode == 'I':
            i = i.point(lambda i: i * (1 / 255))
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
    return image

class IndustrialMagick:
    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "return_image": ("BOOLEAN", {"default": False}),
                "param_count": ("INT", {"default": 5, "min": 0, "max": 50, "step": 1})
            }
        }
        for i in range(1, 50):
            inputs["required"][f"param_{i}"] = ("STRING", {"default": ""})
        return inputs

    RETURN_TYPES = ("IMAGE","STRING","STRING",)
    RETURN_NAMES = ("image","image_path","error",)
    FUNCTION = "execute"
    CATEGORY = "IndustrialMagick"

    def execute(self, return_image, param_count, **kwargs):
        # Extract values from kwargs
        params = [kwargs.get(f"param_{i}") for i in range(1, param_count + 1)]

        params.insert(0,"magick")

        filtered_params = [param for param in params if param not in ["",None]]

        print(filtered_params)

        result = subprocess.run(filtered_params)

        if result.returncode == 0:
            image = None if return_image is False else read_image_from_path(filtered_params[-1])
            return (image,filtered_params[-1],"",)
        else:
            return (image,"","Error processing your command. Check ComfyUI logs.",)
    CATEGORY = "IndustrialMagick"

NODE_CLASS_MAPPINGS = {
    "IndustrialMagick": IndustrialMagick,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IndustrialMagick": "Industrial Magick",
}