from flask import Flask, jsonify, render_template_string
from threading import Thread
import time
import random
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# HTML Template for the web page
HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Mercedes-Benz Predictive Maintenance and Driver Behavior Dashboard</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
      body { font-family: Arial, sans-serif; background-color: #f8f9fa; }
      .container { max-width: 800px; margin: auto; padding: 20px; background-color: #fff; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
      .status { margin: 10px 0; font-size: 1.2rem; }
      .table-container { margin-top: 20px; }
      .btn { margin-top: 10px; }
      .card { margin-top: 20px; }
      .card-header { font-weight: bold; }
      .spinner-border { display: none; margin-left: 10px; }
    </style>
  </head>
  <body>
    <div class="container">
      <h1 class="mt-5 text-center">Predictive Maintenance and Driver Behavior Dashboard</h1>
      <div id="dashboard">
        <div class="status alert alert-info">
          <strong>Maintenance Alert:</strong> <span id="maintenance_alert">Loading...</span>
        </div>
        <div class="status alert alert-info">
          <strong>Driver Behavior:</strong> <span id="driver_behavior">Loading...</span>
        </div>
        <div class="table-container">
          <table class="table table-bordered">
            <thead class="thead-dark">
              <tr>
                <th scope="col">Metric</th>
                <th scope="col">Value</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Mileage</td>
                <td id="mileage">Loading...</td>
              </tr>
              <tr>
                <td>Engine Hours</td>
                <td id="engine_hours">Loading...</td>
              </tr>
              <tr>
                <td>Part Wear</td>
                <td id="part_wear">Loading...</td>
              </tr>
              <tr>
                <td>Speed</td>
                <td id="speed">Loading...</td>
              </tr>
              <tr>
                <td>Acceleration</td>
                <td id="acceleration">Loading...</td>
              </tr>
              <tr>
                <td>Braking</td>
                <td id="braking">Loading...</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="text-center">
          <button class="btn btn-primary" onclick="triggerAlert()">Trigger Maintenance Alert <div class="spinner-border text-light" role="status"></div></button>
        </div>
        <div id="alert-placeholder" class="mt-3"></div>
      </div>
    </div>
    <script>
      function updateDashboard(data) {
        document.getElementById('maintenance_alert').textContent = data.maintenance_alert;
        document.getElementById('driver_behavior').textContent = data.driver_behavior;
        document.getElementById('mileage').textContent = data.vehicle_data.mileage.toFixed(2);
        document.getElementById('engine_hours').textContent = data.vehicle_data.engine_hours.toFixed(2);
        document.getElementById('part_wear').textContent = data.vehicle_data.part_wear.toFixed(2);
        document.getElementById('speed').textContent = data.driver_data.speed.toFixed(2);
        document.getElementById('acceleration').textContent = data.driver_data.acceleration.toFixed(2);
        document.getElementById('braking').textContent = data.driver_data.braking.toFixed(2);
      }

      function fetchData() {
        fetch('/status')
          .then(response => response.json())
          .then(data => updateDashboard(data));
      }

      setInterval(fetchData, 1000);
      fetchData();

      function triggerAlert() {
        const button = document.querySelector('.btn-primary');
        const spinner = button.querySelector('.spinner-border');
        spinner.style.display = 'inline-block';
        
        fetch('/trigger_alert')
          .then(response => response.json())
          .then(data => {
            spinner.style.display = 'none';
            showAlert(data.message, 'success');
          });
      }

      function showAlert(message, type) {
        const alertPlaceholder = document.getElementById('alert-placeholder');
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.role = 'alert';
        alert.innerHTML = `
          ${message}
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        `;
        alertPlaceholder.appendChild(alert);
        setTimeout(() => {
          $(alert).alert('close');
        }, 5000);
      }
    </script>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
  </body>
</html>
'''

# Simulated vehicle and driver data
vehicle_data = {
    'mileage': 0,
    'engine_hours': 0,
    'part_wear': 0
}

driver_data = {
    'speed': 0,
    'acceleration': 0,
    'braking': 0
}

# Simulate machine learning model for predictive maintenance
def predictive_maintenance_model():
    model = LinearRegression()
    X = np.array([[0, 0, 0], [10, 100, 1], [20, 200, 2], [30, 300, 3]])  # Simulated data
    y = np.array([0, 1, 1, 2])  # Simulated maintenance alerts
    model.fit(X, y)
    return model

# Simulate machine learning model for driver behavior analysis
def driver_behavior_model():
    model = LinearRegression()
    X = np.array([[0, 0, 0], [50, 2, 1], [60, 3, 2], [70, 4, 3]])  # Simulated data
    y = np.array(['Good', 'Average', 'Poor', 'Very Poor'])  # Simulated behavior labels
    
    # Convert string labels to numerical values
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    model.fit(X, y_encoded)
    return model, label_encoder

maintenance_model = predictive_maintenance_model()
behavior_model, label_encoder = driver_behavior_model()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/status')
def get_status():
    maintenance_alert = maintenance_model.predict([[vehicle_data['mileage'], vehicle_data['engine_hours'], vehicle_data['part_wear']]])[0]
    driver_behavior_encoded = behavior_model.predict([[driver_data['speed'], driver_data['acceleration'], driver_data['braking']]])[0]
    
    maintenance_alert_text = "No issues" if maintenance_alert < 1 else "Maintenance required soon"
    driver_behavior_text = label_encoder.inverse_transform([int(driver_behavior_encoded)])[0]
    
    return jsonify({
        'maintenance_alert': maintenance_alert_text,
        'driver_behavior': driver_behavior_text,
        'vehicle_data': vehicle_data,
        'driver_data': driver_data
    })

@app.route('/trigger_alert')
def trigger_alert():
    # Simulate triggering an alert
    return jsonify({'message': 'Maintenance alert triggered!'})

def update_data():
    while True:
        time.sleep(1)
        vehicle_data['mileage'] += random.uniform(0, 1)
        vehicle_data['engine_hours'] += random.uniform(0, 0.1)
        vehicle_data['part_wear'] += random.uniform(0, 0.05)
        driver_data['speed'] = random.uniform(0, 100)
        driver_data['acceleration'] = random.uniform(0, 5)
        driver_data['braking'] = random.uniform(0, 5)

if __name__ == '__main__':
    Thread(target=update_data).start()
    app.run(debug=True)
