from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import requests


class GPSCapture:
    def __init__(self):
        """Initialize the GPS capture with Chrome options."""
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless=new")  
        self.options.add_argument("--disable-gpu")               
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])        
        self.driver = webdriver.Chrome(options=self.options)
        
    def setup_html_page(self):
        """Create and load a temporary HTML page to capture GPS coordinates."""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>GPS Capture</title>
        </head>
        <body>
            <div id="location"></div>
            
            <script>
                navigator.geolocation.getCurrentPosition(
                    position => {
                        document.getElementById('location').innerHTML = 
                            `${position.coords.latitude},${position.coords.longitude},${position.coords.accuracy}`;
                    },
                    err => console.error(err),
                    {
                        enableHighAccuracy: true,
                        timeout: 10000,
                        maximumAge: 0
                    }
                );
            </script>
        </body>
        </html>
        """
        
        with open("temp.html", "w") as f:
            f.write(html)
        self.driver.get("file://" + os.path.abspath("temp.html"))
        
    def capture_location(self):
        """Capture and display the current GPS location."""
        try:
            time.sleep(2)  # Wait for location to be captured
            location = self.driver.find_element(By.ID, "location").text
            
            if not location:
                print("No location data received.")
                return
                
            lat, lon, accuracy = location.split(',')
            details = self.reverse_geocode(lat, lon)
            
            print("\nGPS Location Details:")
            print(f"Latitude: {lat}")
            print(f"Longitude: {lon}")
            print(f"Accuracy: {accuracy} meters")
            print(f"Address: {details}")
                
        except Exception as e:
            print(f"Error capturing location: {str(e)}")
            
    def reverse_geocode(self, lat, lon):
        """Convert coordinates to human-readable address using Nominatim API.
        
        Args:
            lat (str): Latitude coordinate
            lon (str): Longitude coordinate
            
        Returns:
            str: Formatted address string
        """
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        headers = {'User-Agent': 'MyReverseGeocoder/1.0'}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if 'address' in data:
                address = data['address']
                return self._format_address(address)
            return "Location not found"
            
        except requests.RequestException as e:
            return f"Geocoding error: {str(e)}"
            
    def _format_address(self, address_data):
        """Format address components into a readable string.
        
        Args:
            address_data (dict): Address components from API
            
        Returns:
            str: Formatted address string
        """
        components = [
            address_data.get('village', ''),
            address_data.get('city', ''),
            address_data.get('state', ''),
            address_data.get('country', ''),
            address_data.get('postcode', '')
        ]
        return ", ".join(filter(None, components))
            
    def cleanup(self):
        """Clean up resources and remove temporary files."""
        self.driver.quit()
        if os.path.exists("temp.html"):
            os.remove("temp.html")


def main():
    """Main execution function."""
    print("Starting GPS capture...")
    capture = GPSCapture()
    
    try:
        capture.setup_html_page()
        capture.capture_location()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        capture.cleanup()


if __name__ == "__main__":
    main()