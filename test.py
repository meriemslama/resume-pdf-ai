import requests
def translate_text_multilingual(text, source_lang, target_lang):
    model_name = "facebook/nllb-200-3.3B"
    url = f"https://api-inference.huggingface.co/models/{model_name}"

    headers = {
        "Authorization": "Bearer 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"
    }

    # Format requis : "<src> <text> </src>"
    lang_map = {
        "fr": "fra_Latn",
        "en": "eng_Latn",
        "es": "spa_Latn",
        "de": "deu_Latn"
    }

    src_code = lang_map[source_lang]
    tgt_code = lang_map[target_lang]

    payload = {
        "inputs": text,
        "parameters": {
            "src_lang": src_code,
            "tgt_lang": tgt_code
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]['translation_text']
    else:
        return f"Erreur traduction : {response.status_code} - {response.text}"
translate_text_multilingual("Ceci est un test.", source_lang="fr", target_lang="es")


print("Vers Espagnol :",translate_text_multilingual("Ceci est un test.", source_lang="fr", target_lang="es"))

