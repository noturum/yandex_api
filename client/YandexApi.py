from typing import Union, Optional
from aiohttp import ClientSession
from .types import YandexPublicFiles, YandexFileList, MediaType
from async_lru import alru_cache

BASE_URL = lambda path: f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={path}'


class YandexApi:
    @classmethod
    def filter(
            cls,
            data: list[YandexFileList],
            filter: Optional[MediaType],
    ):
        filtered = []
        for item in data:
            if str(item.media_type) == filter and item.media_type:
                filtered.append(item)
        return filtered

    @staticmethod
    @alru_cache(maxsize=32)
    async def get_file_list(
            url, path,
    ) -> Union[list, list[YandexFileList]]:
        url = BASE_URL(url)
        if path:
            url += f'&path={path}'
        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return []
                public_dir = YandexPublicFiles.model_validate(
                    await response.json()
                )
                return public_dir.embedded.items

    @staticmethod
    async def downloads_file(url: str, file_name: str):
        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                with open(file_name, "wb") as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                    return file_name
