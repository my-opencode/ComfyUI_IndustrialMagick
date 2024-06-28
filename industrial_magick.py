import folder_paths
import os
comfy_path = os.path.dirname(folder_paths.__file__)
tmp_path = f'{comfy_path}/temp'

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
    CATEGORY = "IndustrialMagick"

NODE_CLASS_MAPPINGS = {
    "IndustrialMagick": IndustrialMagick,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IndustrialMagick": "Industrial Magick",
}