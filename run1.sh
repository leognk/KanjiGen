export MODEL_NAME="CompVis/stable-diffusion-v1-4"
export TRAIN_DIR="data/images"

accelerate launch --mixed_precision="fp16" train_text_to_image.py \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --train_data_dir=$TRAIN_DIR \
  --use_ema \
  --resolution=128 --center_crop --random_flip \
  --train_batch_size=32 \
  --num_train_epochs=2 \
  --checkpointing_steps=10000 \
  --learning_rate=1e-05 \
  --max_grad_norm=1 \
  --lr_scheduler="constant" --lr_warmup_steps=0 \
  --output_dir="exp/model1" \
  --report_to="wandb"