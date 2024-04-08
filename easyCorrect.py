import json
import webbrowser
import pyperclip
from pynput import keyboard
import pyautogui
import os


class Feeder:
    def __init__(self):
        with open('config.json', 'r') as file:
            config = json.load(file)
        
        if not os.path.isfile('input.txt'):
            with open('input.txt', 'w', encoding='UTF-8') as file:
                file.write('')
        with open('input.txt', 'r', encoding='UTF-8') as file:
            inputContent = file.read()

        with open('output.txt', 'w', encoding='UTF-8') as file:
            file.write('')
        
        self.iterator = self.split(inputContent, config['separator'], config['maxCharacterCount'])
        self.firstIteration = True

        webbrowser.open(config['url'])


    def split(self, text:str, sep:str, maxCharacterCount:int):
        content = ''
        for sentence in text.split(sep):
            if len(content) + len(sentence) > maxCharacterCount:
                yield content
                content = ''
            content += sentence + sep
        yield content


    def step(self):
        # append corrected text to output
        if not self.firstIteration:
            pyautogui.hotkey('ctrl', 'x')
            with open('output.txt', 'a', encoding='UTF-8') as file:
                file.write(pyperclip.paste())
        else:
            self.firstIteration = False

        # paste following content into text field
        content = next(self.iterator)
        pyperclip.copy(content)
        pyautogui.hotkey('ctrl', 'v')



def main():
    feeder = Feeder()

    def for_canonical(f):
        return lambda k: f(listener.canonical(k))
    
    hotkey = keyboard.HotKey(keyboard.HotKey.parse('<ctrl>+a'), feeder.step)
    with keyboard.Listener(on_press=for_canonical(hotkey.press), on_release=for_canonical(hotkey.release)) as listener:
        try:
            listener.join()
        except StopIteration:
            pass



if __name__ == '__main__':
    main()