import os
import typing as t
from functools import cached_property
from io import BytesIO, StringIO

import pandas as pd
from azure.core.paging import ItemPaged
from azure.identity import DefaultAzureCredential
from azure.storage.blob import (
    BlobClient,
    BlobProperties,
    BlobServiceClient,
    BlobType,
    ContainerClient,
    StorageStreamDownloader,
)
from pandas import DataFrame

__DEFAULT_CREDENTIALS__ = DefaultAzureCredential(
    exclude_visual_studio_code_credential=True,
    exclude_interactive_browser_credential=True,
)


class AzureBlob:
    def __init__(
        self,
        url: str,
        credential=__DEFAULT_CREDENTIALS__,
    ):
        self.url = url
        self.credential = credential

    def _get_blob_url(self, blob_name: str) -> str:
        return os.path.join(self.url, blob_name)

    @cached_property
    def container_client(self) -> ContainerClient:
        url = self.url
        # cut last character if it is a '/'
        if url[-1] == "/":
            url = url[:-1]

        account_url, container_name = url.rsplit("/", 1)
        blob_service_client = BlobServiceClient(
            account_url=account_url, credential=self.credential
        )
        return blob_service_client.get_container_client(container_name)

    def download_blob(
        self, blob_name: str, readall: bool = True, **kwargs
    ) -> t.Union[str, bytes, StorageStreamDownloader]:
        blob_client = BlobClient.from_blob_url(
            blob_url=self._get_blob_url(blob_name), credential=self.credential, **kwargs
        )
        stream = blob_client.download_blob(offset=None, length=None)
        if readall:
            return stream.readall()
        else:
            return stream

    def list_blobs(self, **kwargs) -> ItemPaged[BlobProperties]:
        return self.container_client.list_blobs(**kwargs)

    def get_max_blob_name(self):
        blob_list_iterator = self.list_blobs()
        return max([blob.name for blob in blob_list_iterator], default=None)

    def read_latest_blob_to_df(
        self,
        sep: str = ";",
        **kwargs,
    ) -> DataFrame:

        blob_client = BlobClient.from_blob_url(
            blob_url=self._get_blob_url(self.get_max_blob_name()),
            credential=self.credential,
        )

        download_blob = blob_client.download_blob(offset=None, length=None)

        downloaded_stream = StringIO(str(download_blob.readall().decode("utf-8")))
        return_df = pd.read_csv(downloaded_stream, sep=sep, dtype="str", **kwargs)
        return return_df

    def write_blob(
        self,
        blob_name: str,
        blob_data: t.Union[t.Iterable[t.AnyStr], t.IO[t.AnyStr]],
        blob_type: BlobType = BlobType.BlockBlob,
    ):
        blob_client = BlobClient.from_blob_url(
            blob_url=self._get_blob_url(blob_name), credential=self.credential
        )
        if blob_type == BlobType.BlockBlob:
            overwrite = True
        elif blob_type == BlobType.AppendBlob:
            overwrite = False
        else:
            raise RuntimeError(f"Blob Type '{blob_type}' is not supported")

        blob_client.upload_blob(
            data=blob_data, blob_type=blob_type, overwrite=overwrite
        )

    def write_df_to_blob(self, blob_name: str, df: DataFrame, **kwargs):
        with BytesIO() as bio:
            df.to_csv(bio, **kwargs)
            bio.seek(0)
            self.write_blob(blob_name=blob_name, blob_data=bio)

