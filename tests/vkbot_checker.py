from asyncio import run
from fromvk import UserBot
from binder import Binder

with open("tokenvk.txt", "r", encoding="utf-8") as file:
    us = UserBot(token=file.read(), config_getter=Binder)
print(
    run(us._work('yakovsava'))
)
