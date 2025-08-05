from typing import AsyncGenerator
from typing import BinaryIO
from minio import Minio
from storage.config import storage_settings as settings
from math import ceil
from uuid import uuid4


class Storage:

    def __init__(self):
        self.client = Minio(
            endpoint=settings.URL,
            access_key=settings.ACCESS_KEY,
            secret_key=settings.SECRET_KEY,
            secure=settings.SECURE)

        self.bucket = settings.BUCKET
        self.location = settings.REGION_NAME
        self.chunk_size = settings.CHUNK_SIZE

    def upload(self, file: BinaryIO, length: int) -> str:
        storage_id = str(uuid4())
        self.client.put_object(self.bucket, storage_id, file, length=length)
        return storage_id

    def stats(self, name: str):
        return self.client.stat_object(self.bucket, name)

    async def download(self, name: str) -> AsyncGenerator:
        total_size = self.stats(name).size
        chunks = ceil(total_size / self.chunk_size)

        for chunk in range(chunks):
            offset = chunk * self.chunk_size
            response = self.client.get_object(
                self.bucket, name, offset=offset, length=self.chunk_size)

            yield response.read()

    def delete(self, name: str):
        self.client.remove_object(self.bucket, name)

    def make_bucket(self):
        if self.client.bucket_exists(self.bucket):
            return False

        self.client.make_bucket(self.bucket, self.location)
        return True
