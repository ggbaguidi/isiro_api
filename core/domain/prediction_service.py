from typing import Dict, Any
import pandas as pd
from datetime import datetime
from core.ports.model_port import ModelPort
from core.ports.notification_port import NotificationPort
from infrastructure.config import Config

class PredictionService:
    """Prediction service class with random sampling and async support"""
    def __init__(self, model: ModelPort, notifier: NotificationPort):
        self.model = model
        self.notifier = notifier
        self.alert_threshold = float(Config.ALERT_THRESHOLD)
        self._dataset = self._load_dataset()  # Load dataset once during initialization
        self.arduino_data = None  # Store latest Arduino data

    def _load_dataset(self) -> pd.DataFrame:
        """Load and cache the dataset"""
        dataset_path = Config.FLOOD_DATASET_PATH

        if not dataset_path:
            raise ValueError("Environment variable FLOOD_DATASET_PATH not set")

        try:
            df = pd.read_csv(dataset_path)
            print(f"Loaded dataset with {len(df)} entries")
            return df
        except Exception as e:
            raise ValueError(f"Error loading flood dataset: {str(e)}") from e

    async def predict_and_alert(self) -> float:
        """Predict and alert with combined data (async)"""
        try:
            input_data = self._get_combined_data()
            print(f"Using combined data:\n{input_data}")

            probability = await self.model.predict(input_data)
            print(f"Predicted probability: {probability:.2f}")

            if probability >= self.alert_threshold:
                message = self._format_alert_message(probability)
                await self.notifier.send_alert(message)
                print("Alert sent successfully")

            return probability

        except Exception as e:
            raise PredictionError(f"Prediction and alert failed: {str(e)}") from e

    def _get_combined_data(self) -> Dict[str, Any]:
        """Combine Arduino data with random sample from dataset"""
        if self._dataset.empty:
            raise ValueError("Dataset is empty")

        # Get random sample from dataset
        sample = self._dataset.sample(n=1).iloc[0].to_dict()
        sample.pop('FloodProbability', None)  # Remove target variable

        # Merge with latest Arduino data
        if self.arduino_data:
            sample.update(self.arduino_data)

        return sample

    def _save_arduino_data(self, data: dict):
        """Save Arduino data and update latest values"""
        file_path = Config.ARDUINO_DATA_PATH
        df = pd.DataFrame([data])
        
        # Write header if file doesn't exist
        header = not pd.io.common.file_exists(file_path)
        df.to_csv(file_path, mode='a', header=header, index=False)

        # Update latest Arduino data
        self.arduino_data = data

    def _format_alert_message(self, probability: float) -> str:
        """Format short flood alert SMS in French"""
        return (
            f"\nALERTE INONDATION\n"
            f"Niveau critique: [{probability*100:.0f}%].\n"
            "Veuillez prendre des mesures préventives.\n"
            "Infos: services d'urgence"
        )


class PredictionError(Exception):
    """Prediction error class"""