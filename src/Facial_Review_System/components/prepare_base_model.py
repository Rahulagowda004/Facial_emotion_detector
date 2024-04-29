import os
import gdown
from Facial_Review_System import logger
from Facial_Review_System.utils.common import get_size
from pathlib import Path
from Facial_Review_System.entity.config_entity import PrepareBaseModelConfig
import tensorflow as tf

#this class is for downloading model 
class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config

    
    def get_base_model(self):
        self.model = tf.keras.applications.DenseNet201(
            input_shape=self.config.params_image_size,
            weights=self.config.params_weights,
            include_top=self.config.params_include_top
        )

        self.save_model(path=self.config.base_model_path, model=self.model)

    

    @staticmethod
    def _prepare_full_model(model, classes, freeze_all, freeze_till, learning_rate):
        if freeze_all:
            for layer in model.layers:
                model.trainable = False
        elif (freeze_till is not None) and (freeze_till > 0):
            for layer in model.layers[:-freeze_till]:
                model.trainable = False
                
        x = tf.keras.layers.Conv2D(32,(3,3),padding = 'same')(model.output)
        x = tf.keras.layers.Dropout(0.45)(x)
        x = tf.keras.layers.Conv2D(16,(3,3),padding = 'same')(x)
        x = tf.keras.layers.MaxPooling2D((2,2),padding = 'same')(x)

        x = tf.keras.layers.Conv2D(32,(3,3),padding = 'same')(x)
        x = tf.keras.layers.Dropout(0.45)(x)
        x = tf.keras.layers.Conv2D(16,(3,3),padding = 'same')(x)
        x = tf.keras.layers.MaxPooling2D((2,2),padding = 'same')(x)

        flatten_in = tf.keras.layers.Flatten()(x)
        
        x = tf.keras.layers.Dense(512, activation='relu')(flatten_in)
        x = tf.keras.layers.Dropout(0.25)(x)
        x = tf.keras.layers.Dense(216, activation='relu')(x)
        
        prediction = tf.keras.layers.Dense(
            units=classes,
            activation="softmax"
        )(x)

        full_model = tf.keras.models.Model(
            inputs=model.input,
            outputs=prediction
        )

        full_model.compile(
            optimizer=tf.keras.optimizers.SGD(),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"]
        )

        full_model.summary()
        return full_model
    
    
    def update_base_model(self):
        self.full_model = self._prepare_full_model(
            model=self.model,
            classes=self.config.params_classes,
            freeze_all=True,
            freeze_till=None,
            learning_rate=self.config.params_learning_rate
        )

        self.save_model(path=self.config.updated_base_model_path, model=self.full_model)

    
        
    @staticmethod
    def save_model(path: Path , model: tf.keras.Model):
        model.save(path)