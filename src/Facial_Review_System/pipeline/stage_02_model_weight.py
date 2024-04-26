from Facial_Review_System.config.configuration import ConfigurationManager
from Facial_Review_System.components.base_model import ModelDownload
from Facial_Review_System.components.prepare_weights import WeightsDownload
from Facial_Review_System import logger

STAGE_NAME = "Model and Weight downloading stage"


class ModelWeightDownloadPipeline:
    def __init__(self):
        pass

    def main(self):
        
        config = ConfigurationManager()
        model_config = config.get_model_config()  
        vgg_model = ModelDownload(config = model_config)
        zip_download_dir = model_config.local_data_file  
        vgg_model.download_file()
        
        weight_config = config.prepare_get_weights_config()  
        comp_weights = WeightsDownload(config=weight_config)
        zip_download_dir = weight_config.local_data_file 
        comp_weights.download_file()


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelWeightDownloadPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e