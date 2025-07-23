# GPS Location Capture with Selenium

A Python script that captures simulated GPS coordinates using Chrome's geolocation API and reverse geocodes them to get address information. This approach provides more precise location data than IP-based Geolocation method.

## Features
- Simulates GPS location capture in Chrome
- Reverse geocoding using OpenStreetMap Nominatim API
- Clean console output with suppressed browser logs
- Automatic cleanup of temporary files

## Requirements
- Python
- Chrome browser
- ChromeDriver

## Basic Usage
```bash
python gps_capture.py
```
## Example Output
```bash
Starting GPS capture...
DevTools listening on ws://127.0.0.1:56941/devtools/browser/dd242e29-664b-4d10-8b74-52a064fbc74c

GPS Location Details:
Latitude: -7.2781707
Longitude: 112.7978779
Accuracy: 20.18 meters
Address: Surabaya, Jawa Timur, Indonesia, 60111

