# core/ports/model_port.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class ModelPort(ABC):
    @abstractmethod
    async def predict(self, input_data: Dict[str, Any]) -> float:
        """Async method to make predictions"""
        raise NotImplementedError
