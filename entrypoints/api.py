import warnings
from gevent.pywsgi import WSGIServer

from infrastructure.adapters.flask_adapter import create_app
from infrastructure.adapters.model_adapter import FloodModelAdapter
from infrastructure.adapters.twilio_sms_adapter import TwilioSmsAdapter
from core.domain.prediction_service import PredictionService

warnings.filterwarnings("ignore")

# Initialize adapters
model_adapter = FloodModelAdapter()
sms_adapter = TwilioSmsAdapter()

# Create service
prediction_service = PredictionService(model_adapter, sms_adapter)

# Create Flask app
app = create_app(prediction_service)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)

    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
