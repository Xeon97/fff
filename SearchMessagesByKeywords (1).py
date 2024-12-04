
# -*- coding: utf-8 -*-
# meta developer: @YourTelegramUsername
# meta description: Поиск сообщений по ключевым словам во всех чатах.
# meta license: MIT

from .. import loader, utils

@loader.tds
class SearchMessagesByKeywordsMod(loader.Module):
    """Модуль для поиска сообщений по ключевым словам во всех чатах."""

    strings = {"name": "SearchMessagesByKeywords"}

    async def poisksocmd(self, message):
        """
        .poiskso (@username) (ключевые слова) - Поиск сообщений по ключевым словам.
        """
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ Укажите: (@username или пропустите) (ключевые слова)")
            return

        args_split = args.split(" ", 1)
        target_user = None
        keywords = ""

        # Определение пользователя и ключевых слов
        if len(args_split) == 2 and args_split[0].startswith("@"):
            target_user = args_split[0].strip("@")
            keywords = args_split[1].strip()
        else:
            keywords = args.strip()

        if not keywords:
            await utils.answer(message, "❌ Укажите ключевые слова для поиска.")
            return

        await utils.answer(message, f"🔍 Начинаю поиск по ключевым словам: '{keywords}'...")

        results = []
        async for dialog in self._client.iter_dialogs():
            chat_id = dialog.id
            async for msg in self._client.iter_messages(chat_id, search=keywords, from_user=target_user):
                results.append(f"📍 [{utils.escape_html(msg.text[:50])}](https://t.me/c/{chat_id}/{msg.id})")

        if results:
            await utils.answer(
                message,
                f"✅ Найдено {len(results)} сообщений:
" + "\n".join(results[:50]) +
                ("\n\nИ многое другое..." if len(results) > 50 else "")
            )
        else:
            await utils.answer(message, "❌ Сообщения с такими ключевыми словами не найдены.")
