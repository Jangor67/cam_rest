from flask import Flask, Response, request, jsonify
from picamera2 import Picamera2, Preview
import io, time

app = Flask(__name__)
picam = Picamera2()

still_config=picam.create_still_configuration()
preview_config=picam.create_preview_configuration()

is_started = False

@app.route('/preview')
def serve_preview():

    global is_started
    if is_started:
        time.sleep(1)
    if is_started:
        return jsonify({'error': 'processing still in progress'}), 400
    is_started = True

    picam.configure(preview_config)
    picam.start(show_preview=True)

    stream = io.BytesIO()
    picam.capture_file(stream, format='jpeg')
    picam.stop()
    is_started = False

    stream.seek(0)
    return Response(stream, mimetype='image/jpeg')

@app.route('/image')
def serve_image():
    exposureTime = request.args.get('exposureTime')
    analogueGain = request.args.get('analogueGain')
    lensPosition = request.args.get('lensPosition')

    controls = {}
    # Voeg alleen geldige waarden toe aan de controls
    if exposureTime is not None:
        try:
            exposureTime = int(exposureTime)
            # Optionele controles op bereik
            # Pas bereik aan naar wat geschikt is voor je camera
            if not (0 <= exposureTime <= 3000000):
                return jsonify({'error': 'exposureTime out of range'}), 400
            controls["ExposureTime"] = exposureTime
        except ValueError:
            return jsonify({'error': 'exposureTime must be an integer'}), 400

    if analogueGain is not None:
        try:
            analogueGain = float(analogueGain)
            # Voorbeeld bereik, afhankelijk van je camera
            if not (1.0 <= analogueGain <= 16.0):
                return jsonify({'error': 'analogueGain range is from 1.0 until 16.0 '}), 400
            controls["AnalogueGain"] = analogueGain
        except ValueError:
            return jsonify({'error': 'analogueGain must be a float'}), 400

    if lensPosition is not None:
        try:
            lensPosition = float(lensPosition)
            # Voorbeeld bereik, afhankelijk van je camera
            if not (0.0 <= lensPosition <= 1.0):
                return jsonify({'error': 'lensPosition must be between 0.0 (far away) and 1.0 (closeby)'}), 400
            controls["LensPosition"] = lensPosition
        except ValueError:
            return jsonify({'error': 'lensPosition must be a float'}), 400

    global is_started
    if is_started:
        time.sleep(1)
    if is_started:
        return jsonify({'error': 'processing still in progress'}), 400
    is_started = True

    picam.configure(still_config)
    if controls:
      try:
          picam.set_controls(controls)
      except Exception as e:
          return jsonify({'error': str(e)}), 500

    picam.start()

    stream = io.BytesIO()
    picam.capture_file(stream, format='jpeg')
    picam.stop()
    is_started = False

    stream.seek(0)
    return Response(stream, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

