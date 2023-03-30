from auto_translate.utils import chunks, create_session
import httpx
import tqdm
import asyncio
import bs4
import re

TOKEN_PATTERN = re.compile(r'(?:\[[^\]]+\])|(?:\$[^$]+\$)')


class GoogleTranslator:
    """
    | Translator class which uses the Google Translator to translate given text into the desired language.
    """

    __slots__ = ["client", "url", "source", "target", "params", "size", "token_pattern",
                 "extra_placeholder", "placeholder", "current_release"]

    def __init__(
            self,
            client: httpx.AsyncClient | httpx.Client = None,
            size: int = 15,
            source: str = "auto",
            target: str = "de",
    ):
        #: HTTPX Client (synchronous or asynchronous)
        self.client: httpx.AsyncClient | httpx.Client = client
        #: Google Translator URL
        self.url = "https://translate.google.com/m"
        #: Source language. Default is automatic language detection 'auto'
        self.source: str = source
        #: Target language. Default is german 'de'.
        self.target: str = target
        #: Google Translator basic parameters for the translation requests
        self.params = {"sl": self.source, "tl": self.target, "hl": "de"}
        #: Chunk size for the batch translation. Default is 10
        self.size = size
        self.token_pattern = re.compile(r'(?:\[[^\]]+\])|(?:\$[^$]+\$)')
        self.placeholder = '@'
        self.extra_placeholder = re.compile(r'\s*' + self.placeholder)
        self.current_release = 'V1.5 - Dies Natalis'

    def gather_tokens(self, text):
        if not text:
            return
        return re.sub(self.token_pattern, self.placeholder, text), re.findall(self.token_pattern, text)

    def fill_back_tokens(self, text, tokens):
        new_text = ''
        x = 0
        for c in text:
            if c == self.placeholder and x < len(tokens):
                new_text += tokens[x]
                x += 1
            else:
                new_text += c
        return re.sub(self.extra_placeholder, "", new_text)

    async def translate_batch(self, texts: dict) -> dict:
        """
        | Translates a given dict of texts asynchronously while taking care of the client management.
        | Ensures to switch up the client regularly for new proxies and user agents.

        :param dict texts: Dict of texts to translate
        :return: Translated results
        :rtype: list
        """
        key_order = texts.keys()
        pieces = list(chunks(texts, self.size))
        result: dict = {}
        # disable progress bar on translation for now
        progress = tqdm.tqdm(total=len(pieces), desc="Translating batches", disable=True)
        for piece in pieces:
            async with create_session() as client:
                self.client = client
                tasks = [self.translate_async(key, value) for key, value in piece.items()]
                _result = await asyncio.gather(*tasks)
                _result = {key: value for key, value in _result}
                result = _result | result
                progress.update(1)
        progress.close()
        # get back original key order
        final = {key: result[key] for key in key_order}
        return final

    async def translate_async(self, key: str, text: str) -> tuple[str, str]:
        """
        | Translates a given text asynchronously.
        If no client is set yet, an asynchronous client will be created.

        :param str key: Key of the text
        :param str text: Text to translate
        :return: Translated text
        :rtype: str
        """
        if not text:
            return key, text
        if text.startswith(self.current_release):  # patch notes, skip
            return key, text
        if not self.client:
            self.client = create_session()
        self.__check_async_client()
        cleaned_text, tokens = self.gather_tokens(text)
        response = await self.client.get(
            self.url,
            params={
                **self.params, "q": cleaned_text
            })
        content = bs4.BeautifulSoup(response.content, 'lxml')
        translation = self.__extract_translation(content)
        return key, self.fill_back_tokens(translation, tokens)

    def __check_async_client(self) -> None:
        """
        | Check that the client is asynchronous.

        :raises AttributeError: If the client is not asynchronous or not set yet
        :return: None
        """
        if not isinstance(self.client, httpx.AsyncClient):
            raise AttributeError(
                "You need to provide an asynchronous client to translate asynchronously!"
            )

    @staticmethod
    def __extract_translation(content: bs4.BeautifulSoup) -> str:
        """
        | Extracts the translated text out of the Google Translator's HTML content

        :param bs4 content: HTML content of Google Translator
        :return: Translated text
        :rtype: str
        """
        return content.select_one('div[class="result-container"]').get_text().strip()
