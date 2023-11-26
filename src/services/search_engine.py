import httpx

from src.db.models import Link


class SearchEngine:
    """
    Класс SearchEngine предназначен для выполнения поиска никнейма на различных веб-ресурсах.

    Этот класс берет список ссылок и выполняет поиск заданного никнейма на каждом из этих ресурсов.
    Поиск осуществляется путем отправки HTTP-запросов на URL, соответствующие каждой ссылке, с добавлением никнейма.

    Методы:
    - search_nickname: Выполняет поиск по всем ссылкам, используя асинхронные HTTP-запросы.
    - _perform_request: Отправляет асинхронный HTTP-запрос на конкретный URL и определяет, был ли никнейм найден.
    - __build_search_url: Строит URL для поиска на основе ссылки и никнейма.
    """

    def __init__(self, links: list[Link] | None = None):
        if links is None:
            links = []

        self.links = links

    async def search_nickname(self, nickname: str):
        for link in self.links:
            found = await self._perform_request(link, nickname)
            yield link, self.__build_search_url(link, nickname) if found else None

    async def _perform_request(self, link, nickname) -> bool:
        url = self.__build_search_url(link, nickname)

        try:
            # logger.debug(f"{FINDING_BY_URL} {link.name}: {url}")

            async with httpx.AsyncClient(verify=False) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    # logger.info(f"{FOUND_IN} {link.name}: {url}")
                    return True
                else:
                    # logger.info(f"{link.name} {NOT_FOUND}")
                    return False
        except httpx.RequestError as e:
            # logger.error(f"{REQUEST_ERROR} {link.name}: {e}")
            return False

    @staticmethod
    def __build_search_url(link: Link, nickname: str):
        return f"{link.url}{nickname}"
