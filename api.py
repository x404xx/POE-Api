from re import search
from time import sleep

from httpx import Client


class PoeApi:
    BASE_URL = 'https://www.quora.com'
    HEADERS = {
        'Host': 'www.quora.com',
        'Accept': '*/*',
        'apollographql-client-version': '1.1.6-65',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Poe 1.1.6 rv:65 env:prod (iPhone14,2; iOS 16.2; en_US)',
        'apollographql-client-name': 'com.quora.app.Experts-apollo-ios',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
    }
    FORMKEY_PATTERN = r'formkey": "(.*?)"'
    GRAPHQL_QUERIES = {
        'ChatFragment': '''
            fragment ChatFragment on Chat {
                __typename
                id
                chatId
                defaultBotNickname
                shouldShowDisclaimer
            }
        ''',
        'MessageFragment': '''
            fragment MessageFragment on Message {
                id
                __typename
                messageId
                text
                linkifiedText
                authorNickname
                state
                vote
                voteReason
                creationTime
                suggestedReplies
            }
        '''
    }

    def __init__(self, cookie: str):
        self.client = Client(timeout=180)
        self.client.cookies.set('m-b', cookie)
        self.client.headers.update({
            **self.HEADERS,
            'Quora-Formkey': self.get_formkey(),
        })
   
    def __del__(self):
        self.client.close()

    def get_formkey(self):
        response = self.client.get(self.BASE_URL)
        formkey = search(self.FORMKEY_PATTERN, response.text)[1]
        return formkey

    def send_request(self, path: str, data: dict):
        response = self.client.post(f'{self.BASE_URL}/poe_api/{path}', json=data)
        return response.json()

    def get_chatid(self, bot: str='a2'):
        query = f'''
            query ChatViewQuery($bot: String!) {{
                chatOfBot(bot: $bot) {{
                    __typename
                    ...ChatFragment
                }}
            }}
            {self.GRAPHQL_QUERIES['ChatFragment']}
        '''
        variables = {'bot': bot}
        data = {'operationName': 'ChatViewQuery', 'query': query, 'variables': variables}
        response_json = self.send_request('gql_POST', data)
        chat_data = response_json.get('data')
        if chat_data is None:
            raise ValueError('Chat data not found!')
        return chat_data['chatOfBot']['chatId']

    def send_message(self, message: str, bot='a2', chat_id: str=''):
        query = f'''
            mutation AddHumanMessageMutation($chatId: BigInt!, $bot: String!, $query: String!, $source: MessageSource, $withChatBreak: Boolean! = false) {{
                messageCreate(
                    chatId: $chatId
                    bot: $bot
                    query: $query
                    source: $source
                    withChatBreak: $withChatBreak
                ) {{
                    __typename
                    message {{
                        __typename
                        ...MessageFragment
                        chat {{
                            __typename
                            id
                            shouldShowDisclaimer
                        }}
                    }}
                    chatBreak {{
                        __typename
                        ...MessageFragment
                    }}
                }}
            }}
            {self.GRAPHQL_QUERIES['MessageFragment']}
        '''
        variables = {'bot': bot, 'chatId': chat_id, 'query': message, 'source': None, 'withChatBreak': False}
        data = {'operationName': 'AddHumanMessageMutation', 'query': query, 'variables': variables}
        self.send_request('gql_POST', data)

    def clear_context(self, chat_id: str):
        query = f'''
            mutation AddMessageBreakMutation($chatId: BigInt!) {{
                messageBreakCreate(chatId: $chatId) {{
                    __typename
                    message {{
                        __typename
                        ...MessageFragment
                    }}
                }}
            }}
            {self.GRAPHQL_QUERIES['MessageFragment']}
        '''
        variables = {'chatId': chat_id}
        data = {'operationName': 'AddMessageBreakMutation', 'query': query, 'variables': variables}
        self.send_request('gql_POST', data)

    def get_latest_message(self, bot: str):
        query = f'''
            query ChatPaginationQuery($bot: String!, $before: String, $last: Int! = 10) {{
                chatOfBot(bot: $bot) {{
                    id
                    __typename
                    messagesConnection(before: $before, last: $last) {{
                        __typename
                        pageInfo {{
                            __typename
                            hasPreviousPage
                        }}
                        edges {{
                            __typename
                            node {{
                                __typename
                                ...MessageFragment
                            }}
                        }}
                    }}
                }}
            }}
            {self.GRAPHQL_QUERIES['MessageFragment']}
        '''
        variables = {'before': None, 'bot': bot, 'last': 1}
        data = {'operationName': 'ChatPaginationQuery', 'query': query, 'variables': variables}

        author_nickname = ''
        state = 'incomplete'
        while True:
            sleep(2)
            response_json = self.send_request('gql_POST', data)
            edges = response_json['data']['chatOfBot']['messagesConnection']['edges']
            if edges:
                latest_message = edges[-1]['node']
                text = latest_message['text']
                state = latest_message['state']
                author_nickname = latest_message['authorNickname']
                if author_nickname == bot and state == 'complete':
                    break
            else:
                text = 'Fail to get a message. Please try again!'
                break

        return text
