# ═══════════════════════════════════════════════════════════════
# Все эмодзи централизованы здесь.
# Чтобы заменить на кастомные премиум эмодзи, просто поменяй
# значение на формат: "<emoji id=\"CUSTOM_EMOJI_ID\">PLACEHOLDER</emoji>"
# или tg-формат строки с custom_emoji_id
#
# Пример кастомного премиум эмодзи:
#   HEART = "5449505950283078474"
# ═══════════════════════════════════════════════════════════════

# --- Сердечки и любовь ---
HEART = "<tg-emoji emoji-id=\"5449505950283078474\">❤️</tg-emoji>"
KISS_MARK = "<tg-emoji emoji-id=\"5253823632504804390\">💋</tg-emoji>"
SMILING_HEARTS = "<tg-emoji emoji-id=\"5445350981741077343\">🥰</tg-emoji>"
KISS_FACE = "<tg-emoji emoji-id=\"5379553147918258286\">😚</tg-emoji>"
KISS_FACE_2 = "<tg-emoji emoji-id=\"5251384542052242131\">😙</tg-emoji>"
HEART_EYES = "<tg-emoji emoji-id=\"5266960167936743640\">😍</tg-emoji>"
BLOWING_KISS = "<tg-emoji emoji-id=\"5251384542052242131\">😘</tg-emoji>"

# --- Праздник ---
PARTY = "<tg-emoji emoji-id=\"5461151367559141950\">🎉</tg-emoji>"
GIFT = "<tg-emoji emoji-id=\"5193085063998224234\">🎁</tg-emoji>"

# --- Эмоции ---
FLUSHED = "😳"
QUESTION_RED = "<tg-emoji emoji-id=\"5397924488274783318\">❓</tg-emoji>"
INTERROBANG = "<tg-emoji emoji-id=\"5467596412663372909\">⁉️</tg-emoji>"


def e(*emojis: str) -> str:
    """Склеивает эмодзи в строку без пробелов."""
    return "".join(emojis)
