import datetime
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

class IndustrialMagickImageIngest:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("image_path",)
    FUNCTION = "ingest"
    CATEGORY = "IndustrialMagick"

    def ingest(self, image):
        img_full_path = None
        for (batch_number, ii) in enumerate(image):
            i = 255. * ii.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            img_file_name = f'ImageMagick_{timestamp}.png'
            if not os.path.exists(tmp_path):
                os.makedirs(tmp_path)
            img_full_path = f'{tmp_path}/{img_file_name}'
            img_full_path = os.path.normpath(img_full_path)
            if os.path.exists(img_full_path):
                random_suffix = uuid.uuid4().hex
                img_file_name = f'ImageMagick_{timestamp}_{random_suffix}.png'
                img_full_path = os.path.join(tmp_path, img_file_name)
            img.save(img_full_path)
        return (img_full_path,)

NODE_CLASS_MAPPINGS = {
    "IndustrialMagick": IndustrialMagick,
    "IndustrialMagickImageIngest":IndustrialMagickImageIngest
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IndustrialMagick": "Industrial Magick",
    "IndustrialMagickImageIngest": "Industrial Magick Image Loader"
}