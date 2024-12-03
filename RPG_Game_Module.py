
import random
from telethon import events

players = {}
items = {
    "sword": {"price": 50, "power": 10},
    "shield": {"price": 30, "defense": 5},
}

@hikka.on(events.NewMessage(pattern=r'/profile'))
async def show_profile(event):
    user_id = event.sender_id
    if user_id not in players:
        players[user_id] = {"level": 1, "exp": 0, "gold": 100, "items": []}
    profile = players[user_id]
    response = (
        f"🎮 Профиль игрока:\n"
        f"👤 Игрок: {event.sender.first_name}\n"
        f"⭐ Уровень: {profile['level']}\n"
        f"⚡ Опыт: {profile['exp']}\n"
        f"💰 Золото: {profile['gold']}\n"
        f"🎒 Предметы: {', '.join(profile['items']) or 'нет'}"
    )
    await event.reply(response)

@hikka.on(events.NewMessage(pattern=r'/quest start'))
async def start_quest(event):
    question = random.choice([
        {"q": "Я без рук и без ног, но всех обнимаю. Что я?", "a": "кровать"},
        {"q": "Что всегда идёт, но никогда не приходит?", "a": "время"},
    ])
    await event.reply(f"🎲 Новый квест!\nЗагадка: {question['q']}")
    
    @hikka.on(events.NewMessage)
    async def check_answer(inner_event):
        if inner_event.text.lower() == question['a']:
            winner = inner_event.sender.first_name
            await inner_event.reply(f"🎉 {winner} правильно ответил на загадку!")
            players[inner_event.sender_id]["gold"] += 10
            hikka.remove_event_handler(check_answer)

@hikka.on(events.NewMessage(pattern=r'/shop'))
async def open_shop(event):
    shop_items = "\n".join([f"{name} - {data['price']} золота" for name, data in items.items()])
    await event.reply(f"🛒 Магазин:\n{shop_items}\n\nДля покупки используйте /buy <предмет>")

@hikka.on(events.NewMessage(pattern=r'/buy (.+)'))
async def buy_item(event):
    item_name = event.pattern_match.group(1).lower()
    user_id = event.sender_id
    if item_name not in items:
        await event.reply("❌ Предмет не найден!")
        return
    if players[user_id]["gold"] >= items[item_name]["price"]:
        players[user_id]["gold"] -= items[item_name]["price"]
        players[user_id]["items"].append(item_name)
        await event.reply(f"🎉 Вы купили {item_name}!")
    else:
        await event.reply("❌ У вас недостаточно золота!")
