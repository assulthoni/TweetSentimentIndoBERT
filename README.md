# TweetSentimentIndoBERT
This repository is used to save django project that classify Tweet Using IndoBERT pre-trained model. Just need to input word as twitter query to know sentiment of tweet.

## How to Use
- Install dependencies in requirements.txt `pip install -r requirements.txt`
- Make .env file with Twitter API key and SECRET_KEY django
- Train your model (call me for PyTorch fine tuned model weights or look at https://github.com/indobenchmark/indonlu/blob/master/examples/finetune_smsa.ipynb)
- Put your model (model.bin) at sentiment django app
- Run your server with `python manage.py runserver --noreload`

## IndoBERT Paper

https://arxiv.org/abs/2009.05387
