from asyncio import gather, create_task, run

from plugins.binder import Binder
from plugins.totg import TGBot
from plguins.fromvk import UserBot
from plugins.middleware import check_to_stop, replace_word
from plugins.sheduler import AsyncSheduler

def_binder = Binder("config.json")
filter_binder = Binder("filters.json")
vkbind = Binder("vkontakte.json")
tgbind = Binder("telegram.json")
vkbot = UserBot(
	token=vkbind.sync_get_config()['token'],
	config_getter=vkbind
)
tgbot = TGBot(
	token=tgbind.sync_get_config()['token'],
	config=tgbind
)
startup_config = def_binder.sync_get_config()
with open(startup_config['queue'], 'r', encoding='utf-8') as file:
	shed = AsyncSheduler(queue=eval(file.read()), timeout=startup_config['timeout'], queue_filename=startup_config['queue'])

async def do_work():
	while True:
		filters_config = await filter_binder.get_config()
		data = await vkbot.worker()
		for text_index, text_data in enumerate(data['texts']):
			if check_to_stop(text_data, filters_config['stop']):
				del data['texts'][text_index]
				del data['photos'][text_index]
			else:
				data['texts'][text_index] = replace_word(data['texts'][text_index], filters_config['replace'])
		for text, photos in zip(data['texts'], data['photos']):
			await shed.add_to_queue([text, photos])

async def start():
	await gather(
		create_task(do_work()),
		create_task(shed.worker(tgbot.post))
	)

if __name__ == '__main__':
	run(start())