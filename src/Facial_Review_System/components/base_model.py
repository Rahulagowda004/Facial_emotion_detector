import os
import gdown
from Facial_Review_System import logger
from Facial_Review_System.utils.common import get_size
from Facial_Review_System.entity.config_entity import (PrepareBaseModelConfig)

class ModelDownload:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config

    def download_file(self) -> str:
        '''
        Fetch data from the url
        '''

        try: 
            dataset_url = self.config.source_URL
            os.makedirs(self.config.root_dir, exist_ok=True)  # Updated directory path
            logger.info(f"Downloading data from {dataset_url} into file {self.config.local_data_file}")

            file_id = dataset_url.split("/")[-2]
            prefix = 'https://drive.google.com/uc?/export=download&id='
            gdown.download(prefix + file_id, self.config.local_data_file)  # Save to local_data_file

            logger.info(f"Downloaded data from {dataset_url} into file {self.config.local_data_file}")

        except Exception as e:
            raise e
