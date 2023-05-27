<div align="center">

# Quora Poe <img src="https://qsf.cf2.quoracdn.net/-4-images.favicon-new.ico-26-07ecf7cd341b6919.ico" width="35px">
This is a reverse-engineered API for Quora's Poe that allows access to the following chatbots.

</div>

## **Available Bots**
1. Sage - OpenAI (capybara)
2. GPT-4 - OpenAI (beaver)
3. Claude+ - Anthropic (a2_2)
4. Claude - Anthropic (a2)
5. ChatGPT - OpenAI (chinchilla)
6. Dragonfly - OpenAI (nutria)

## **Requirements**
```sh
pip install -r requirements.txt
```

## **Authentication**

Sign in at https://www.quora.com/
-   F12 for console
-   Copy the values
    -   Session: Go to Storage → Cookies → `m-b`. Copy the value of that cookie. Put in the (_**config.json**_)

<img src="https://github.com/x404xx/POE-Api/assets/114883816/e306aebf-961b-4e69-9c6c-9214040c8124" width="auto" height="auto">

## **Usage**

You can find an example of how to use this API in the (_**example.py**_) file or you can do like the following code

```python
from json import load

from api import PoeApi


with open('config.json') as file:
    config = load(file)

client = PoeApi(cookie=config['m-b'])
bots = {
    1: 'capybara',
    2: 'beaver',
    3: 'a2_2',
    4: 'a2',
    5: 'chinchilla',
    6: 'nutria'
}
choice = input('Who do you want to talk to?\n'
            '1. Sage - OpenAI (capybara)\n'
            '2. GPT-4 - OpenAI (beaver)\n'
            '3. Claude+ - Anthropic (a2_2)\n'
            '4. Claude - Anthropic (a2)\n'
            '5. ChatGPT - OpenAI (chinchilla)\n'
            '6. Dragonfly - OpenAI (nutria)\n\n'
            'Your choice: ')

bot = bots[int(choice)]
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
```

## **Credits**

POE.com Reverse Engineered CLI - [Credits to Vaibhavk97](https://github.com/vaibhavk97/Poe)
- I made modifications to the original API. The formkey is no longer necessary; only the cookie is required.

## **Legal Disclaimer**

> **Note**
> This was made for educational purposes only, nobody which directly involved in this project is responsible for any damages caused. **_You are responsible for your actions._**
