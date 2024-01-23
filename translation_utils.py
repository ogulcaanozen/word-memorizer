from googletrans import Translator

def translate(word):
    translator = Translator()
    translation = translator.translate(word, dest='tr')
    return translation.text