"""
Основной модуль бота.

• Хранит шаг каждого пользователя в памяти (dict user_id → step_index).
• Каждый ответ бота предваряется chat_action «typing» с паузой.
• После шага 5 (видео) сначала отправляется текст, затем «upload_video» + пауза + видео.
• Параллельно крутится лёгкий HTTP-сервер для Render (health-check).
"""

import asyncio
import logging
import os
import pathlib

from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ChatAction, ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    FSInputFile,
)
from dotenv import load_dotenv

from config.settings import TYPING_DELAY, VIDEO_UPLOAD_DELAY, VIDEO_PATH
from dialogue.scenario import STEPS

# ── Загружаем .env ─────────────────────────────────────────────
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в .env!")

# Render передаёт порт через переменную окружения PORT
WEB_PORT = int(os.getenv("PORT", "10000"))

# ── Логирование ────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
)
log = logging.getLogger("birthday_bot")

# ── Инициализация ──────────────────────────────────────────────
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# user_id → текущий индекс шага
user_state: dict[int, int] = {}

# Абсолютный путь к видео
BASE_DIR = pathlib.Path(__file__).resolve().parent
VIDEO_ABS = BASE_DIR / VIDEO_PATH


# ── Хелперы ────────────────────────────────────────────────────
def make_keyboard(buttons: list[str] | None) -> ReplyKeyboardMarkup | ReplyKeyboardRemove:
    """Создаёт ReplyKeyboard из списка строк или убирает клавиатуру."""
    if not buttons:
        return ReplyKeyboardRemove()
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=btn)] for btn in buttons],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


async def send_step(message: types.Message, step_index: int) -> None:
    """
    Отправляет один шаг сценария:
      1. chat_action «typing» + пауза
      2. текст бота
      3. (опционально) chat_action «upload_video» + пауза + видео
      4. клавиатура следующего шага
    """
    step = STEPS[step_index]

    # --- «Печатает…» ---
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(TYPING_DELAY)

    # --- Текст бота ---
    if step["bot_text"]:
        await message.answer(
            step["bot_text"],
            reply_markup=make_keyboard(step["buttons"]),
        )

    # --- Видео ---
    if step["send_video"]:
        await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO)
        await asyncio.sleep(VIDEO_UPLOAD_DELAY)

        if VIDEO_ABS.exists():
            video = FSInputFile(VIDEO_ABS)
            await message.answer_video(video=video)
        else:
            log.warning("Видео не найдено: %s", VIDEO_ABS)
            await message.answer("🎬 [видео будет здесь]")

    # --- Обновляем состояние ---
    if step["next"] is not None:
        user_state[message.from_user.id] = step_index
    else:
        # Сценарий окончен — сбрасываем
        user_state.pop(message.from_user.id, None)


# ── Хендлеры ───────────────────────────────────────────────────
@dp.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    """Запуск сценария по /start."""
    log.info("Пользователь %s запустил бота", message.from_user.id)
    user_state[message.from_user.id] = 0
    await send_step(message, step_index=0)


@dp.message(F.text)
async def handle_reply(message: types.Message) -> None:
    """Обрабатывает ответы по Reply Keyboard."""
    uid = message.from_user.id
    step_index = user_state.get(uid)

    if step_index is None:
        # Пользователь ещё не начал или уже закончил — предлагаем /start
        await message.answer("Напиши /start, чтобы начать 💌")
        return

    current_step = STEPS[step_index]

    # Проверяем, что ответ совпадает с одной из кнопок (если кнопки есть)
    if current_step.get("buttons"):
        # Принимаем любой текст из предложенных кнопок
        valid = [btn.strip() for btn in current_step["buttons"]]
        if message.text.strip() not in valid:
            await message.answer("Выбери один из вариантов ответа 👇")
            return

    # Переходим к следующему шагу
    next_index = current_step["next"]
    if next_index is not None:
        await send_step(message, step_index=next_index)
    else:
        user_state.pop(uid, None)


# ── Health-check веб-сервер для Render ─────────────────────────
async def health_handler(request: web.Request) -> web.Response:
    """Эндпоинт /health — отвечает 200 OK, чтобы Render не убил сервис."""
    return web.json_response({"status": "ok", "bot": "running"})


async def start_web_server() -> None:
    """Запускает лёгкий HTTP-сервер на PORT для Render health-check."""
    app = web.Application()
    app.router.add_get("/", health_handler)
    app.router.add_get("/health", health_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", WEB_PORT)
    await site.start()
    log.info("Health-check сервер запущен на порту %s", WEB_PORT)


# ── Точка входа ────────────────────────────────────────────────
async def main() -> None:
    log.info("Бот запускается…")

    # Запускаем веб-сервер и polling параллельно
    await asyncio.gather(
        start_web_server(),
        dp.start_polling(bot),
    )


if __name__ == "__main__":
    asyncio.run(main())
