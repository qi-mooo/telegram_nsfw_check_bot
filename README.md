# telegram_nsfw_check_bot
一个telegram bot，利用[nsfwjs-api](https://github.com/qi-mooo/nsfwjs-api)检测图片是否是nsfw，可选自动打码重发(群内发送 /toggle_spoiler 设置)
## docker
```
docker pull qimooo/telegram_nsfw_check_bot:latest
```
```
docker run -d -e API_HASH=your_api_hash -e API_ID=your_api_id -e API_URL=your_api_url -e BOT_TOKEN=your_bot_token qimooo/telegram_nsfw_check_bot:latest

```
