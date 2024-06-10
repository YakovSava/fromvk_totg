from os import remove
from asyncio import gather, create_task, run
from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from plugins.binder import Binder

class TGBotError(Exception): pass

class TGBot:

	def __init__(self, token:str=None, config:Binder=None):
		if token is None:
			raise TGBotError("Token not found!")
		if config is None:
			raise TGBotError("Config binder not found!")
		self._bot = Bot(token=token)
		self._config = config

	async def post(self, text:str, photos:list=[]) -> None:
		config = await self._config.get_config()
		if len(photos) == 0:
			await self._bot.send_message(
				chat_id=config['channel_id'],
				text=text
			)
		elif len(photos) == 1:
			await self._bot.send_photo(
				chat_id=config['channel_id'],
				photo=(await self._download_photo(photos[0])),
				caption=text
			)
			await self._remove_photo(photos[0])
		else:
			mediagroup = MediaGroupBuilder(caption=text)
			for photo in photos:
				mediagroup.add(
					type="photo",
					media=(await self._download_photo(photo))
				)
			await self._bot.send_media_group(
				chat_id=config['channel_id'],
				media=mediagroup.build()
			)
			await gather(
				*[create_task(self._remove_photo(photo)) for photo in photos]
			)

	async def _download_photo(self, photo_path:str) -> FSInputFile:
		return FSInputFile(path=photo_path)

	async def _remove_photo(self, photo_path:str) -> None:
		remove(photo_path)

if __name__ == '__main__':
	tg = TGBot(token=open('tested_token.txt', 'r', encoding='utf-8').read(), config=Binder('configuration.json'))
	run(tg.post("Тестовый текст!", ["./vwehr3710.jpg", "./odsryjxawitnp4201.jpg"]))