import os
from pathlib import Path
from tqdm import tqdm
from datetime import datetime
import torch
import torch.nn as nn
from diffusers import StableDiffusionPipeline, UNet2DConditionModel, AutoencoderKL


model_dir = os.path.join("exp", "model2")
checkpoint = 200000

prompts = [
    "armed fish",
    "language model",
    "climate change",
    "baby robot",
]
num_inference_steps = 200
num_images_per_prompt = 10


# Load UNet
ckpt_path = os.path.join(model_dir, f"checkpoint-{checkpoint}" if checkpoint else "")
unet = UNet2DConditionModel.from_pretrained(os.path.join(ckpt_path, "unet"), torch_dtype=torch.float16)

# Define identity VAE
vae = AutoencoderKL()
vae.encoder = nn.Identity()
vae.decoder = nn.Identity()
vae.quant_conv = nn.Identity()
vae.post_quant_conv = nn.Identity()

# Load pipeline
pipe = StableDiffusionPipeline.from_pretrained(
    model_dir, vae=vae, unet=unet, torch_dtype=torch.float16, safety_checker=None,
)
pipe.to("cuda")

# Generate and save images for each prompt
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
save_path = os.path.join(model_dir, "images", timestamp)
Path(save_path).mkdir(parents=True, exist_ok=True)
for prompt in tqdm(prompts):
    imgs = pipe(
        prompt=prompt, num_inference_steps=num_inference_steps,
        num_images_per_prompt=num_images_per_prompt, 
    ).images
    for i, img in enumerate(imgs):
        img.save(os.path.join(save_path, f"{prompt}-{i + 1}.png"))