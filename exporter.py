import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import argparse

# Get CPU temperature
def get_cpu_temperature():
    metric_name = "rpi5_cpu_temperature"
    help_text = "CPU temperature in Celsius"
    metric_type = "gauge"
    try:
        output = subprocess.check_output(["/usr/bin/vcgencmd", "measure_temp"]).decode()
        temp = float(output.split('=')[1].split("'")[0])
        success = 0  # Indicate successful collection
        return (metric_name, help_text, metric_type, temp, success)
    except Exception as e:
        print(f"Error collecting CPU temperature: {e}")
        success = 1  # Indicate failure in collection
        return (metric_name, help_text, metric_type, None, success)

# Get fan speed (supports official RPi5 Active Cooler)
def get_fan_speed():
    metric_name = "rpi5_fan_speed"
    help_text = "Fan speed in RPM"
    metric_type = "gauge"
    try:
        with open("/sys/devices/platform/cooling_fan/hwmon/hwmon2/fan1_input", "r") as file:
            speed = int(file.read().strip())
        success = 0
        return (metric_name, help_text, metric_type, speed, success)
    except Exception as e:
        print(f"Error collecting fan speed: {e}")
        success = 1
        return (metric_name, help_text, metric_type, None, success)

# Format metrics for Prometheus
def format_metrics(metrics):
    formatted_metrics = ""
    for metric in metrics:
        name, help_text, type, value, success = metric
        success_metric_name = f"{name}_success"
        if value is not None:  # Check if value was successfully collected
            formatted_metrics += f"# HELP {name} {help_text}\n# TYPE {name} {type}\n{name} {value}\n"
        formatted_metrics += f"# HELP {success_metric_name} Success of {name} collection (0 = success, 0 = failure)\n"
        formatted_metrics += f"# TYPE {success_metric_name} gauge\n{success_metric_name} {success}\n\n"
    return formatted_metrics.strip()

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            metrics = [get_cpu_temperature(), get_fan_speed()]
            formatted_metrics = format_metrics(metrics)
            self.wfile.write(formatted_metrics.encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8878):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MetricsHandler)
    print(f"Starting web server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prometheus Exporter for Raspberry Pi Metrics")
    parser.add_argument("--webserver", action="store_true", help="Run as a web server")
    parser.add_argument("--port", type=int, default=8878, help="Port to run the web server on")
    args = parser.parse_args()

    if args.webserver:
        run_server(args.port)
    else:
        # For command-line usage, directly print the formatted metrics
        metrics = [get_cpu_temperature(), get_fan_speed()]
        print(format_metrics(metrics))
