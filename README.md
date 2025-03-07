# ISIRO API
## Flood Prediction API

ISIRO API is a real-time flood prediction system that combines environmental data with Arduino sensor readings to predict flood probabilities and send alerts when risk levels are critical.

### Features

- Real-time flood probability prediction
- Integration with Arduino sensors for environmental data
- Automatic SMS alerts via Twilio when flood risk is high
- Scheduled predictions every 15 minutes
- REST API endpoints for manual predictions and sensor data collection

### Installation

```bash
# Clone the repository
git clone https://github.com/ggbaguidi/isiro_api.git
cd isiro_api

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Copy a `.env.example` to `.env` file in the root directory with the following variables:

```
cp .env.example .env
```

### API Endpoints

#### POST /predict
Triggers a manual prediction and returns the flood probability.

**Response:**
```json
{
    "probability": 0.85,
    "alert_sent": true
}
```

#### POST /arduino-data
Endpoint for Arduino devices to submit sensor readings.

**Request Body:**
```json
{
    "temperature": 28.5,
    "humidity": 75.2,
    "soil_moisture": 390,
    "water_level": 120
}
```

### Running the API

```bash
# Run the Flask application
python -m entrypoints.api
```

### Architecture

The application follows a hexagonal architecture:

- **Core Domain** (`core/`): Contains the business logic and domain services
- **Ports** (`core/ports/`): Defines interfaces for external adapters
- **Adapters** (`infrastructure/adapters/`): Implements ports for external services
- **API** (`infrastructure/adapters/flask_adapter.py`): Flask web server exposing endpoints

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### License

This project is licensed under the MIT License - see the LICENSE file for details.
