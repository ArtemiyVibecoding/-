"""
Dialogue-сценарий поздравительного бота.

Каждый шаг — dict с ключами:
  bot_text   — текст, который отправляет бот (None, если бот ничего не пишет)
  send_video — True, если после bot_text нужно отправить видео
  buttons    — список строк для ReplyKeyboard (None → бот ждёт любого текста)
  next       — индекс следующего шага (или None, если это конец)
"""

from config.emojis import (
    HEART, KISS_MARK, SMILING_HEARTS, KISS_FACE, KISS_FACE_2,
    HEART_EYES, BLOWING_KISS, PARTY, GIFT, FLUSHED,
    QUESTION_RED, INTERROBANG, e,
)

STEPS = [
    # ── 0: Приветствие (стартовое сообщение) ───────────────────────
    {
        "bot_text": (
            f"Привет, красотка!!!{e(SMILING_HEARTS, SMILING_HEARTS)} "
            f"Сегодня твой день рождения{e(PARTY, PARTY)} "
            f"Готова к поздравлению?"
        ),
        "send_video": False,
        "buttons": [
            "Да!!",
            "Конечно!!",
            "Еще как готова!!",
        ],
        "next": 1,
    },

    # ── 1: Как настроение? ─────────────────────────────────────────
    {
        "bot_text": f"Для начала, как твое настроение{e(QUESTION_RED, QUESTION_RED)}",
        "send_video": False,
        "buttons": [
            "Привееет! Всё просто супер🥰🥰",
            "Привееееет!!! Всё замечательно!!! 💋💋❤️",
            "Привееет!!! Шикарнооо💋🥰❤️🥰",
        ],
        "next": 2,
    },

    # ── 2: Распаковывала подарки? ──────────────────────────────────
    {
        "bot_text": f"Уже распаковывала подарки{e(QUESTION_RED)}",
        "send_video": False,
        "buttons": [
            "Конечно!!",
        ],
        "next": 3,
    },

    # ── 3: А знаешь, что я хочу сказать? ──────────────────────────
    {
        "bot_text": f"А знаешь, что я хочу тебе сказать{e(INTERROBANG)}",
        "send_video": False,
        "buttons": [
            "Чтоо😳😳",
            "Ого, что же 😳😳",
        ],
        "next": 4,
    },

    # ── 4: Главное поздравление ────────────────────────────────────
    {
        "bot_text": (
            "Спасибо тебе огромное, любимая, что появилась в моей жизни, "
            "я безумно благодарен тебе в том, что ты изменила мою жизнь в лучшую сторону, "
            "и вот ты уже стала почти совершеннолетней девочкой, которую я так сильно "
            f"люблю и безумно ценю!!! "
            f"{e(KISS_MARK, KISS_FACE, KISS_MARK, KISS_FACE_2, KISS_MARK, KISS_FACE, KISS_MARK, KISS_FACE, KISS_MARK, HEART_EYES, KISS_MARK, KISS_FACE, KISS_FACE, BLOWING_KISS, BLOWING_KISS)}"
        ),
        "send_video": False,
        "buttons": [
            "Спасибооо, любимый!!💋❤️❤️💋❤️💋 Я тебя люблюююю!!! ❤️❤️💋💋❤️",
        ],
        "next": 5,
    },

    # ── 5: Поздравление + видео-подарок ────────────────────────────
    {
        "bot_text": (
            "И в такой знаменательный день я хочу поздравить тебя от всего сердца "
            f"с днём рождения!!! {e(KISS_MARK, SMILING_HEARTS, KISS_FACE, SMILING_HEARTS, KISS_MARK, SMILING_HEARTS, KISS_FACE, SMILING_HEARTS, KISS_MARK, KISS_FACE, SMILING_HEARTS)} "
            f"Держи небольшой подарок{e(GIFT)}!!"
        ),
        "send_video": True,
        "buttons": [
            "ВААААУ, СПАСИБООО, ЛЮБИМЫЫЫЙ❤️❤️🥰❤️❤️🥰",
        ],
        "next": 6,
    },

    # ── 6: Финал ───────────────────────────────────────────────────
    {
        "bot_text": (
            "Ну что ж, а теперь пора вернуться в Макс, ведь там тебя уже буду ждать я, "
            f"твой будущий муж! {e(HEART, KISS_MARK, SMILING_HEARTS, KISS_MARK, HEART)}"
        ),
        "send_video": False,
        "buttons": None,   # Диалог окончен
        "next": None,
    },
]
