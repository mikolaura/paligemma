from typing import Dict, List, Optional, Union, Tuple, Iterable
from matplotlib.image import resample
import numpy as np
from PIL import Image
import torch

IMAGENET_STANDARD_MEAN = [0.5, 0.5, 0.5]
IMAGENET_STANDARD_STD = [0.5, 0.5, 0.5]

def proccess_image(images: List[Image.Image],
                size: Dict[str , int] = None,#type: ignore
                   resample:Image.Resampling = None, # type: ignore
                    rescale_factor:float = None,#type: ignore
                     image_mean: Optional[Union[float, List[float]]]=None,
                     image_std: Optional[Union[float, List[float]]]=None):
    height, width = size[0], size[1]
    images = [
        resize(image=image, size=(height,width), resample=resample) for image in images
    ]
    images = [np.array([image]) for image in images]
    images = [rescale(image,scale=rescale_factor) for image in images]
    images = [normalize(image, mean=image_mean, std = image_std) for image in images]
    images = [image.transpose(2, 0, 1) for image in images]

    return images    


class PaliGemmaProcessor:

    IMAGE_TOKEN = "<image>"

    def __init__(self, tokenizer, num_image_tokens: int, image_size: int):
        super().__init__()

        self.image_seq_length = num_image_tokens
        self.image_size = image_size
        tokens_to_add = {"additional_special_tokens": [self.IMAGE_TOKEN]}
        tokenizer.add_special_tokens(tokens_to_add)
        EXTRA_TOKENS = [f"<loc{i:04d}>" for i in range(1024)]
        EXTRA_TOKENS += [f"<seg{i:03d}>" for i in range(128)]
        tokenizer.add_tokens(EXTRA_TOKENS)
        self.image_token_id = tokenizer.convert_tokens_to_ids(self.IMAGE_TOKEN)
        tokenizer.add_bos_token = False
        tokenizer.add_eos_token = False
        self.tokenizer = tokenizer

    def __call__(
        self,
        text: List[str],
        images: List[Image.Image],
        padding: str = "longest",
        truncation: bool = True,
    ) -> dict:
        assert len(images) == 1 and len(text) == 1, f"Received {len(images)} images for {len(text)} prompts."
        
        pixel_values = proccess_images(
            images,
            size=(self.image_size, self.image_size),
            resample=Image.Resampling.BICUBIC,
            rescale_factor = 1 / 255.0
            image_mean = IMAGENET_STANDARD_MEAN,
            image_std = IMAGENET_STANDARD_STD

        )
        pixel_values = np.stack(pixel_values, axis=0)
        pixel_values = torch.tensor(pixel_values)
        input_strings = [
            add_image_tokens_to_prompt(
                prefix_prompt=prompt,
                bos_token = self.tokenizer.bos_token,
                image_seq_len = self.image_seq_length,
                image_token = self.IMAGE_TOKEN
            )
            for prompt in text
        ]
        inputs = self.tokenizer(
            input_strings,
            return_tensors='pt',
            padding=padding,
            truncation=truncation
        )
        return_data={"pixel_values":pixel_values, **inputs}
        return return_data