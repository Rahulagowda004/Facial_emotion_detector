import os
import gdown
from pathlib import Path
from Facial_Review_System import logger
from Facial_Review_System.utils.common import get_size
from Facial_Review_System.entity.config_entity import (PrepareBaseModelConfig)
import tensorflow as tf


class PrepareBaseModel:
    def __init__(self, config:PrepareBaseModelConfig):
        self.config = config

    def get_base_model(self):
        
        self.model = tf.keras.models.load_model("artifacts/prepare_base_model/base_model.h5")

        self.save_model(path=self.config.base_model_path, model=self.model)


    @staticmethod
    def _prepare_full_model(model, classes):
        
        for layer in model.layers:
            model.trainable = False
            
        Input = tf.keras.layers.Input(shape=(224, 224, 3))
        
        vgg = model(Input)
        
        flatten_in = tf.keras.layers.Flatten()(vgg)
        
        dense1 = tf.keras.layers.Dense(
            units=512,
            activation="relu"
        )(flatten_in)
        
        dense2 = tf.keras.layers.Dense(
            units=206,
            activation="relu"
        )(dense1)
        
        dropout = tf.keras.layers.Dropout(0.25)(dense2)
        
        prediction = tf.keras.layers.Dense(
            units=classes,
            activation="softmax"
        )(dropout)
        
        full_model = tf.keras.models.Model(
            inputs=Input,
            outputs=prediction
        )

        full_model.compile(
            optimizer=tf.keras.optimizers.Adam(),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"]
        )
        
        full_model.summary()
        return full_model
    
    
    def update_base_model(self):
        self.full_model = self._prepare_full_model(
            model=self.model,
            classes=self.config.params_classes
        )

        self.save_model(path=self.config.updated_base_model_path, model=self.full_model)

    
        
    @staticmethod
    def save_model(path:Path, model: tf.keras.Model):
        model.save(path)