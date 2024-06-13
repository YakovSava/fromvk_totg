print('Начало импортов')

from asyncio import gather, create_task, run, sleep
from aiogram import Dispatcher, F 
from aiogram.types import Message

from plugins.binder import Binder, FilterBinder, VKBinder
from plugins.totg import TGBot
from plugins.fromvk import UserBot
from plugins.middleware import check_to_stop, replace_word
from plugins.sheduler import AsyncSheduler

print('Импорты завершены. Начало инциализации...')

def_binder = Binder("config.json")
filter_binder = FilterBinder("filters.json")
vkbind = VKBinder("vkontakte.json")
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
	shed = AsyncSheduler(
		queue=eval(file.read()),
		timeout=startup_config['timeout'],
		queue_filename=startup_config['queue']
	)
dp = Dispatcher()
print('Инциализация завершена')

@dp.message(F.text.lower().startswith('правило'))
async def add_new_rule(message:Message):
	msg = 'Неизвестная команда. Искомая команда:\n\n\
Правило [удалить/добавить] [стоп/фильтр] [стоп_слово ИЛИ фильтр_заменяемое фильтр_замеить_на]\n\n\
Пример:\n\
Правило добавить фильтр кирпич бетон\n\
Правило добавить стоп Реклама\n\
Правило добавить фильтр баня дом'
	parts = message.text.lower().split(maxsplit=3)
	if message.from_user.id in (await tgbind.get_config())['admins']:
		if parts[1] == 'добавить':
			if parts[2] == 'стоп':
				if (await filter_binder.new_stop(parts[3])):
					await message.answer('Успешно!')
				else:
					await message.answer('Не успешно! Возможно, данное слово уже существует')
			elif parts[2] == 'фильтр':
				if (await filter_binder.new_repl(parts[3].split())):
					await message.answer('Успешно!')
				else:
					await message.answer('Не успешно! Возможно, данная замена и так есть!')
			else:
				await message.answer(msg)
		elif parts[1] == 'удалить':
			if parts[2] == 'стоп':
				if (await filter_binder.del_stop(parts[3])):
					await message.answer('Успешно!')
				else:
					await message.answer('Не успешно! Возможно, данного слова и так не существует')
			elif parts[2] == 'фильтр':
				if (await filter_binder.del_repl(parts[3].split())):
					await message.answer('Успешно!')
				else:
					await message.answer('Не успешно! Возможно, данной замены и так нет!')
			else:
				await message.answer(msg)
		else:
			await message.answer(msg)

@dp.message(F.text.lower().startswith('домен'))
async def add_new_domain(message:Message):
	msg = '''Неизвестная командаю Пример команды:
домен [добавить/удалить] [домен в вк, например ndma_taxi]\n
Использование:
Домен добавить ndma_taxi
Домен удалить ndma_taxi'''
	parts = message.text.lower().split(maxsplit=2)
	if message.from_user.id in (await tgbind.get_config())['admins']:
		if parts[1] == 'добавить':
			if (await vkbind.new_domain(parts[2])):
				await message.answer('Домен добавлен!')
			else:
				await message.answer('Домен и так был!')
		elif parts[1] == 'удалить':
			if (await vkbind.del_domain(parts[2])):
				await message.answer('Домен удалён!')
			else:
				await message.answer('Домена и так не было!')
		else:
			await message.answer(msg)

async def do_work():
	while True:
		filters_config = await filter_binder.get_config()
		data = await vkbot.worker()
		# print(data)
		for text_index, text_data in enumerate(data['texts']):
			if check_to_stop(text_data, filters_config['stop']):
				del data['texts'][text_index]
				del data['photos'][text_index]
			else:
				data['texts'][text_index] = replace_word(data['texts'][text_index], filters_config['replace'])
		for text, photos in zip(data['texts'], data['photos']):
			await shed.add_to_queue([text, photos])
		await sleep(startup_config['timeout'])

async def start():
	print('Старт программы!')
	await gather(
		create_task(do_work()),
		create_task(shed.worker(tgbot.post)),
		create_task(dp.start_polling(tgbot.bot))
	)

async def test_vk():
	data = await vkbot.worker()
	print(data)

if __name__ == '__main__':
	run(start())