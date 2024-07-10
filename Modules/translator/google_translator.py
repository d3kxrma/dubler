from deep_translator import GoogleTranslator

class Translator:
    def __init__(self, source:str, target:str):
        self.translator = GoogleTranslator(source=source, target=target)

    def translate(self, text):
        return self.translator.translate(text)
    
if __name__ == "__main__":
    translator = Translator("en", "uk")
    print(translator.translate("Hello, World!"))