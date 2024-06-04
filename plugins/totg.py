from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

class TelegramError(Exception): pass

class TelegramSender:

	def __init__(self, bot:Bot=None, dp:Dispatcher=None, token:str=None):
		if (token is None) and (bot is None):
			raise TelegramError("Укажите бота или токен!")
		elif dp is None:
			raise TelegramError("Укажите диспечтер!")
		elif (token is None):
			self._bot = bot
		elif (bot is None):
			self._bot = Bot(token=token)
		self._dp = dp

	async def add_new_group_to_repost(self, new_domain:str) -> None:
		pass

	async def remove_group_from_reposts(self, old_domain:str) -> None:
		pass

	async def post(self, text:str, photos:str) -> bool:
		pass