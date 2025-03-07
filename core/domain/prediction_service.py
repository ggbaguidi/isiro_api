import os
from typing import Dict, Any
import pandas as pd
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
        self.arduino_data = self._load_arduino_data()  # Store latest Arduino data

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

    def _load_arduino_data(self) -> Dict[str, Any]:
        """Load the latest Arduino data from the CSV file"""
        file_path = Config.ARDUINO_DATA_PATH

        if not os.path.exists(file_path):
            print("No Arduino data file found. Starting with empty data.")
            return None

        try:
            # Read the CSV file
            df = pd.read_csv(file_path)

            # Get the last row (most recent data)
            if not df.empty:
                latest_data = df.iloc[-1].to_dict()
                print(f"Loaded latest Arduino data: {latest_data}")
                return latest_data
            else:
                print("Arduino data file is empty.")
                return None

        except Exception as e:
            print(f"Error loading Arduino data: {str(e)}")
            return None

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
        """Combine Arduino data with the last row of the dataset"""
        if self._dataset.empty:
            raise ValueError("Dataset is empty")

        # Get random sample from dataset
        last_row = self._dataset.sample(n=1).iloc[0].to_dict()
        last_row.pop('FloodProbability', None)  # Remove target variable

        # Merge with latest Arduino data (if available)
        if self.arduino_data:
            # Add Arduino data as new features
            last_row.update({
                'temperature': self.arduino_data.get('temperature', 0),
                'humidity': self.arduino_data.get('humidity', 0),
                'soil_moisture': self.arduino_data.get('soil_moisture', 0),
                'water_level': self.arduino_data.get('water_level', 0)
            })

        return last_row

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