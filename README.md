# Raspberry Pi 5 Exporter

Raspberry Pi Prometheus exporter. Works in Docker, or as a standalone script. Written in Python (since more people know this language, including myself) so it can be easily extended. It uses python's internal webserver.

Supports Raspberry Pi 5 and Raspbian-based images. Currently shows:

* CPU/GPU temperature
* fan speed of the official [active cooler](https://www.raspberrypi.com/products/active-cooler/)

## Requirements

* Python 3.x
* (optional) Docker

## Usage

### Docker

```
docker run -d -p 8878:8878 --device /dev/vcio --name rpi5_exporter berkas1/rpi5_exporter:v0.1
```

### Standalone

* clone this repository or download the script to your Raspberry Pi 5
* run the exporter `python3 raspberry_pi_5_exporter.py --webserver --port 8878`


## Integration with Prometheus:

To integrate with Prometheus, add the following job to your Prometheus configuration file (prometheus.yml):


```yaml
scrape_configs:
  - job_name: 'raspberry_pi_5'
    static_configs:
      - targets: ['<Raspberry_Pi_IP>:8878']
```

## License

This script is provided under the MIT License. See the LICENSE file for more details.