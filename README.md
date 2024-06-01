# Generating Novel Kanjis with Diffusion Model

In this project, I trained from scratch a pixel-level diffusion model to generate kanjis (Chinese characters used in Japanese) conditioned on their meaning. After training, we can ask the model to generate a plausible kanji that doesn't exist from a small description of our choice.

## Data

The data is from kanjidic2 and KanjiVG taken from [here](https://github.com/Gnurou/tagainijisho).

## Code

The code is modified from HuggingFace diffusers example code of training a text-to-image stable diffusion [here](https://github.com/huggingface/diffusers/blob/main/examples/text_to_image/train_text_to_image.py). I modified the code so that I could train the model directly on the pixels rather than the latents produced by the VAE's encoder, so that I don't need to train separetely a VAE from scratch.

## Samples

Here are some interesting samples of novel kanjis generated by the model I trained.

|               |               |               |               |               |
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
| Deep learning | Bitcoin | lol | Thank you | achieve <br> enlightenment |
| <img src="samples/Deep learning.png" width="100"> | <img src="samples/Bitcoin.png" width="100"> | <img src="samples/lol.png" width="100"> | <img src="samples/Thank you.png" width="100"> | <img src="samples/achieve enlightenment.png" width="100"> |
| paradise | Mount Fuji | plasma | the Big Bang | gravity |
| <img src="samples/paradise.png" width="100"> | <img src="samples/Mount Fuji.png" width="100"> | <img src="samples/plasma.png" width="100"> | <img src="samples/the Big Bang.png" width="100"> | <img src="samples/gravity.png" width="100"> |
| The answer to life,<br>the universe,<br>and everything | infinity | nightmare | a fluffy dog | Godzilla |
| <img src="samples/The answer to life, the universe, and everything.png" width="100"> | <img src="samples/infinity.png" width="100"> | <img src="samples/nightmare.png" width="100"> | <img src="samples/a fluffy dog.png" width="100"> | <img src="samples/Godzilla.png" width="100"> |
| Ultraman | samurai | rainbow unicorn | Jackie Chan | Twitter |
| <img src="samples/Ultraman.png" width="100"> | <img src="samples/samurai.png" width="100"> | <img src="samples/rainbow unicorn.png" width="100"> | <img src="samples/Jackie Chan.png" width="100"> | <img src="samples/Twitter.png" width="100"> |
| Instagram | Dragon Ball | manga | Pikachu | Mewtwo |
| <img src="samples/Instagram.png" width="100"> | <img src="samples/Dragon Ball.png" width="100"> | <img src="samples/manga.png" width="100"> | <img src="samples/Pikachu.png" width="100"> | <img src="samples/Mewtwo.png" width="100"> |
| super hero | ramen | piano | arctic | antarctica |
| <img src="samples/super hero.png" width="100"> | <img src="samples/ramen.png" width="100"> | <img src="samples/piano.png" width="100"> | <img src="samples/arctic.png" width="100"> | <img src="samples/antarctica.png" width="100"> |
| penguin | polar bear | crocodile | legendary sword | blood moon |
| <img src="samples/penguin.png" width="100"> | <img src="samples/polar bear.png" width="100"> | <img src="samples/crocodile.png" width="100"> | <img src="samples/legendary sword.png" width="100"> | <img src="samples/blood moon.png" width="100"> |