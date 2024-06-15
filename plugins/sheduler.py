from asyncio import sleep, gather, create_task
from random import shuffle
from typing import Coroutine
from aiofiles import open as aiopen

class AsyncSheduler:

	def __init__(self, queue:list=[], timeout:int=3600, queue_filename:str=""):
		self._q = queue
		self._qf = queue_filename
		self._timeout = timeout

	async def worker(self, func:Coroutine) -> None:
		while True:
			if len(self._q) == 0:
				await sleep(60)
			else:
				shuffle(self._q)
				await func(*self._q[0])
				await self._remove_from_queue(index=0)
				await sleep(self._timeout)

	async def mass_start(self, funcs:list[Coroutine], data:list) -> None: # For feature!
		if len(funcs) == len(data):
			tasks = []
			for func, dat in zip(funcs, data):
				tasks.append(create_task(funcs(dat)))
			await gather(*tasks)
		else:
			raise ShedulerError("Please, send more data/coro")

	async def add_to_queue(self, new_data) -> bool:
		try: self._q.index(new_data)
		except:
			self._q.append(new_data)
			ret = True
		else: ret = False
		async with aiopen(self._qf, 'w', encoding='utf-8') as file:
			await file.write(str(self._q))
		return ret

	async def _remove_from_queue(self, data_to_del=None, index:int=None) -> None:
		if (index is None) and (data_to_del is None):
			raise ShedulerError("Index and data is None")
		elif index is not None:
			del self._q[index]
		else:
			self._q.remove(data_to_del)
		async with aiopen(self._qf, 'w', encoding='utf-8') as file:
			await file.write(str(self._q))