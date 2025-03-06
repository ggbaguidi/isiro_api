from typing import Callable, Awaitable
import asyncio
import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from flask import Flask, jsonify, request


def create_app(prediction_service):
    """Create Flask app with async support"""
    app = Flask(__name__)

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    @app.route('/predict', methods=['POST'])
    async def predict():
        """Async endpoint for manual prediction triggering"""
        try:
            probability = await prediction_service.predict_and_alert()
            return jsonify({
                'probability': probability,
                'alert_sent': probability >= prediction_service.alert_threshold
            }), 200
        except ValueError as e:
            logger.error(f"Invalid input data: {str(e)}")
            return jsonify({'error': f'Invalid input data: {str(e)}'}), 400
        except (ConnectionError, TimeoutError) as e:
            logger.error(f"Service unavailable: {str(e)}")
            return jsonify({'error': f'Service unavailable: {str(e)}'}), 503
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}", exc_info=True)
            return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

    @app.route('/arduino-data', methods=['POST'])
    def arduino_data():
        """Receive sensor data from Arduino"""
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No JSON data received'}), 400

            # Validate required fields
            required = [
                'temperature',
                'humidity',
                'soil_moisture',
                'water_level']
            if not all(key in data for key in required):
                return jsonify(
                    {'error': f'Missing fields. Required: {required}'}), 400

            # Add timestamp and save
            data['timestamp'] = datetime.now().isoformat()
            prediction_service._save_arduino_data(data)

            return jsonify({'message': 'Data received', 'data': data}), 200

        except Exception as e:
            logger.error(f"Arduino data error: {str(e)}")
            return jsonify({'error': str(e)}), 500

        except Exception as e:
            logger.error(f"Arduino data error: {str(e)}")
            return jsonify({'error': str(e)}), 500

    def run_async_job(job: Callable[[], Awaitable[None]]):
        """Helper function to run async jobs in the scheduler"""
        try:
            asyncio.run(job())
        except Exception as e:
            logger.error(f"Scheduled job failed: {str(e)}", exc_info=True)

    # Schedule predictions every 15 minutes
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=run_async_job,
        args=[prediction_service.predict_and_alert],
        # Change to minutes=15 for production
        trigger=IntervalTrigger(seconds=900),
        id='flood_prediction_job',
        replace_existing=True
    )
    scheduler.start()

    # Ensure scheduler shuts down gracefully
    @app.teardown_appcontext
    def shutdown_scheduler(exception=None):
        if scheduler.running:
            scheduler.shutdown()

    return app
