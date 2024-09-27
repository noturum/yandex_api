from typing import Union

from pydantic import BaseModel, Field
from enum import StrEnum


class MediaType(StrEnum):
    ALL = 'all'
    TEXT = 'text'
    DEVELOPMENT = 'development'
    IMAGE = 'image'


class YandexFileList(BaseModel):
    name: str
    file: str = None
    type: str
    path: str
    media_type: Union[MediaType, str, None] = None


class ListItems(BaseModel):
    items: list[YandexFileList]


class YandexPublicFiles(BaseModel):
    public_key: str
    public_url: str = None
    embedded: ListItems = Field(alias='_embedded')


class FileInfo(BaseModel):
    file_name: str
    file_path: str


class DownloadsFile(BaseModel):
    files: list[FileInfo]
