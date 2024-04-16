from io import BytesIO

from minio import Minio


class MinioStorage:

    def __init__(self, client: Minio, pictures_bucket_name: str):
        self.pictures_bucket_name = pictures_bucket_name
        self.client = client

    def upload_file(self, filename: str, file: bytes) -> None:
        self.client.put_object(
            self.pictures_bucket_name,
            filename,
            BytesIO(file),
            len(file),
        )
