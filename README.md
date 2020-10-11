# prometheus_telldus_exporter
Prometheus Exporter for Telldus Live

Project extended from the work by https://gitlab.com/rlnrln/telldus-exporter/

# Instructions
Add your Telldus Live API key and token to apikeys.json before launching the script or building the Dockerfile.

```shell
docker build --tag telldus-exporter .
```

## Docker image
Start your docker container with:

```shell
docker run -d -p 9191:9191 --restart="always" -v /path/to/apikeys:/etc/telldus-exporter \
telldus-exporter:latest
```

Point your web browser to http://YOUR_IP:9191/metrics to verify you're getting data from the Telldus API.

# Sample

These sample metrics you can get from your sensors

```
# HELP telldus_sensor_power_amp Sensor data
# TYPE telldus_sensor_power_amp gauge
telldus_sensor_power_amp{id="1535337344",location="Home",name="Outlet1"} 0.182
# HELP telldus_sensor_power_volt Sensor data
# TYPE telldus_sensor_power_volt gauge
telldus_sensor_power_volt{id="1535337344",location="Home",name="Outlet1"} 224.69
# HELP telldus_sensor_temperature Sensor data
# TYPE telldus_sensor_temperature gauge
telldus_sensor_temperature{id="1535329719",location="Home",name="Greenhouse - Inside"} 2.8
telldus_sensor_temperature{id="1535329749",location="Home",name="Greenhouse - Outside"} 2.2
# HELP telldus_sensor_humidity Sensor data
# TYPE telldus_sensor_humidity gauge
telldus_sensor_humidity{id="1535329719",location="Home",name="Greenhouse - Inside"} 90.0
# HELP telldus_sensor_power_kwh_total Sensor data
# TYPE telldus_sensor_power_kwh_total counter
telldus_sensor_power_kwh_total{id="1535337344",location="Home",name="Outlet1"} 469134.8899999885
telldus_sensor_power_kwh_total{id="1535413544",location="Home",name="Outlet2"} 11115.649999999763
# HELP telldus_sensor_power_kwh_created Sensor data
# TYPE telldus_sensor_power_kwh_created gauge
telldus_sensor_power_kwh_created{id="1535337344",location="Home",name="Outlet1"} 1.602533162288238e+09
telldus_sensor_power_kwh_created{id="1535413544",location="Home",name="Outlet2"} 1.602533162012138e+09
# HELP telldus_sensor_power_watt Sensor data
# TYPE telldus_sensor_power_watt gauge
telldus_sensor_power_watt{id="1535337344",location="Home",name="Outlet1"} 15.978
telldus_sensor_power_watt{id="1535413544",location="Home",name="Outlet2"} 0.0
```