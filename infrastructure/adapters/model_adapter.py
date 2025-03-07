import pickle

import pandas as pd

from core.ports.model_port import ModelPort
from infrastructure.config import Config


class FloodModelAdapter(ModelPort):
    def __init__(self):
        self.model = self._load_model()

    def _load_model(self):
        model_path = Config.MODEL_PATH
        with open(model_path, 'rb') as f:
            return pickle.load(f)

    async def predict(self, input_data: dict) -> float:
        # Convert input data to model's expected format

        features = [
            input_data['MonsoonIntensity'],
            input_data['TopographyDrainage'],
            input_data['RiverManagement'],
            input_data['Deforestation'],
            input_data['Urbanization'],
            input_data['ClimateChange'],
            input_data['DamsQuality'],
            input_data['Siltation'],
            input_data['AgriculturalPractices'],
            input_data['Encroachments'],
            input_data['IneffectiveDisasterPreparedness'],
            input_data['DrainageSystems'],
            input_data['CoastalVulnerability'],
            input_data['Landslides'],
            input_data['Watersheds'],
            input_data['DeterioratingInfrastructure'],
            input_data['PopulationScore'],
            input_data['WetlandLoss'],
            input_data['InadequatePlanning'],
            input_data['PoliticalFactors'],
            input_data['temperature'],  # From Arduino
            input_data['humidity'],     # From Arduino
            input_data['soil_moisture'], # From Arduino
            input_data['water_level']    # From Arduino
        ]

        features = pd.DataFrame(
            [features],
            columns=[
                'MonsoonIntensity',
                'TopographyDrainage',
                'RiverManagement',
                'Deforestation',
                'Urbanization',
                'ClimateChange',
                'DamsQuality',
                'Siltation',
                'AgriculturalPractices',
                'Encroachments',
                'IneffectiveDisasterPreparedness',
                'DrainageSystems',
                'CoastalVulnerability',
                'Landslides',
                'Watersheds',
                'DeterioratingInfrastructure',
                'PopulationScore',
                'WetlandLoss',
                'InadequatePlanning',
                'PoliticalFactors',
                'temperature',
                'humidity',
                'soil_moisture',
                'water_level'
            ])

        return float(self.model.predict(features)[0])
