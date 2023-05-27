from json import load

from api import PoeApi

class Poe:
    @staticmethod
    def load_config():
        with open('config.json') as file:
            return load(file)

    @staticmethod
    def select_bot():
        bots = {
            1: 'capybara',
            2: 'beaver',
            3: 'a2_2',
            4: 'a2',
            5: 'chinchilla',
            6: 'nutria'
        }
        while True:
            choice = input('Who do you want to talk to?\n'
                        '1. Sage - OpenAI (capybara)\n'
                        '2. GPT-4 - OpenAI (beaver)\n'
                        '3. Claude+ - Anthropic (a2_2)\n'
                        '4. Claude - Anthropic (a2)\n'
                        '5. ChatGPT - OpenAI (chinchilla)\n'
                        '6. Dragonfly - OpenAI (nutria)\n\n'
                        'Your choice: ')
            if choice.isdigit() and int(choice) in bots:
                return bots[int(choice)]
            print('Invalid choice. Please select a valid option.')

    @classmethod
    def chat_with_bot(cls):
        config = cls.load_config()
        client = PoeApi(cookie=config['m-b'])
        bot = cls.select_bot()
        print(f'The selected bot is: {bot}')
        chat_id = client.get_chatid(bot)
        client.clear_context(chat_id)
        print("Context is now cleared")

        while True:
            message = input('\033[38;5;121mYou\033[0m : ').lower()
            if message == '!clear':
                client.clear_context(chat_id)
                print("Context is now cleared")
            elif message == '!exit':
                break
            else:
                client.send_message(message, bot, chat_id)
                result = client.get_latest_message(bot)
                print(f'\033[38;5;20m{bot}\033[0m : {result.strip()}')


if __name__ =='__main__':
    Poe().chat_with_bot()
