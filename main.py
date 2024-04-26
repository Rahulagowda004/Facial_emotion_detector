from Facial_Review_System import logger
from Facial_Review_System.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from Facial_Review_System.pipeline.stage_02_model_weight import ModelWeightDownloadPipeline



# STAGE_NAME = "Data Ingestion stage"
# try:
#    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
#    data_ingestion = DataIngestionTrainingPipeline()
#    data_ingestion.main()
#    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
# except Exception as e:
#         logger.exception(e)
#         raise e
     
STAGE_NAME = "Model and Weight downloading stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   obj = ModelWeightDownloadPipeline()
   obj.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
   logger.exception(e)
   raise e
