from aiogram import Bot
from aiogram.types import Message

from plugins.binder import ConfigBinder

class TelegramError(Exception): pass

class TelegramSender:

	def __init__(self, bot:Bot=None, token:str=None, config_binder:ConfigBinder=None):
		if (token is None) and (bot is None):
			raise TelegramError("Укажите бота или токен!")
		elif (token is None):
			self._bot = bot
		elif (bot is None):
			self._bot = Bot(token=token)
		if config_binder is None:
			raise TelegramError("Укажите конфигурационный связыватель!")
		self._cb = config_binder

	async def add_new_group_to_repost(self, new_domain:str) -> str:
		if (await self._cb.add_new_domain(new_domain)):
			return "Успешно!"
		else:
			return "Похоже данная запись уже есть!"

	async def remove_group_from_reposts(self, old_domain:str) -> None:
		if (await self._cb.del_new_group(old_domain)):
			return "Успешно!"
		else:
			return "Похоже данной записи не было!"

	async def post(self, text:str, photos:str) -> bool:
		pass