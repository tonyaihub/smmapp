import deepl
import config

translator = deepl.Translator(config.DEEPL_API_KEY)

def localize(content, target_lang='ES'):  # e.g., Spanish
    result = translator.translate_text(content, target_lang=target_lang)
    return result.text