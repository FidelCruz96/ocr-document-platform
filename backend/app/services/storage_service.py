from io import BytesIO

from minio import Minio

from app.core.config import get_settings


def get_minio_client() -> Minio:
    settings = get_settings()
    return Minio(
        endpoint=settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
    )


def ensure_bucket_exists() -> None:
    settings = get_settings()
    client = get_minio_client()
    if not client.bucket_exists(settings.minio_bucket):
        client.make_bucket(settings.minio_bucket)


def upload_file(object_name: str, file_bytes: bytes, content_type: str) -> None:
    settings = get_settings()
    ensure_bucket_exists()
    get_minio_client().put_object(
        bucket_name=settings.minio_bucket,
        object_name=object_name,
        data=BytesIO(file_bytes),
        length=len(file_bytes),
        content_type=content_type,
    )


def download_file(bucket_name: str, object_name: str) -> bytes:
    response = get_minio_client().get_object(bucket_name, object_name)
    try:
        return response.read()
    finally:
        response.close()
        response.release_conn()


def delete_file(bucket_name: str, object_name: str) -> None:
    get_minio_client().remove_object(bucket_name, object_name)
