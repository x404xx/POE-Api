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

You can find an example of how to use this API in the _**example.py**_ file.

## **Credits**

POE.com Reverse Engineered CLI - [Credits to Vaibhavk97](https://github.com/vaibhavk97/Poe)
- I made modifications to the original API. The formkey is no longer necessary; only the cookie is required.

## **Legal Disclaimer**

> **Note**
> This was made for educational purposes only, nobody which directly involved in this project is responsible for any damages caused. **_You are responsible for your actions._**
