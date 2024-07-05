import os
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask
import matplotlib.pyplot as plt
import io
import base64
import json

app = Flask(__name__)

# Read the service account key from environment variable
encoded_service_account_key = os.getenv('ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAidXNlci02NWM0MCIsCiAgInByaXZhdGVfa2V5X2lkIjogImNiMzcyMjU1MmEzOWQ5NDFkNmRlNTE1MDc1ODU0MmMwOGM1MzQ4Y2IiLAogICJwcml2YXRlX2tleSI6ICItLS0tLUJFR0lOIFBSSVZBVEUgS0VZLS0tLS0KTVlJRXdJQkFEQU5CZ2txYkhqa2tqaUdvejd3MEJBSAogIEFvSUJBRGFOQmdrcWlydU1ReTA0RUNUSGkKICBZcGRCUituOVJ4bEFydXhjT1B0SmtlVjRkaWdBZmhsb0RvVnQ1K2hTanowN0RZbllqZUpteEZ2a1FlYUlnL0N5WUcrQlpaTytDWm9Eb1Z0NStoU2pvN0RZbllqZ1BHWTNQeFJsU1k1eUgvM1ZqL1lPSG1VdEJ3cDlTNjhzdzdxOHhyMm5RYzdTbFdldWFWcFlBbXFsQmNOcDdsT3djb21kRjB4VWFrb0RrNHJMQnpyR3Z2ZEMxMzcyeDVTdXdOWUJxZk53Y09tZEE2U2xYZXVhVnBZQW1xbEIzYW5jT3hGTHVwT2p5VFVqSWd5Wk5qZ1BHR1lOT3B4UjFMU1k0NWUzRTEycm84U09icHdYZTZrczJ5ek1QZE54OHxHQU1CQUFCCUFBQ2d3WW5NM<|endoffile|>
')

if not encoded_service_account_key:
    raise ValueError("The environment variable 'GOOGLE_APPLICATION_CREDENTIALS' is not set.")

# Decode the Base64 string
service_account_key = base64.b64decode(encoded_service_account_key).decode('utf-8')
service_account_info = json.loads(service_account_key)

# Initialize Firebase with your credentials
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://user-65c40-default-rtdb.firebaseio.com'
})

@app.route('/plot', methods=['GET'])
def plot_users():
    # Reference to your database
    ref = db.reference('/user')

    # Fetch data from Firebase
    snapshot = ref.get()

    # Initialize dictionary to store city-wise user counts
    city_data = {}

    # Process data to get city-wise user counts
    if snapshot:
        for username, user_info in snapshot.items():
            if 'city' in user_info:
                city = user_info['city']
                if city:
                    if city in city_data:
                        city_data[city] += 1
                    else:
                        city_data[city] = 1

    # Prepare data for plotting
    cities = list(city_data.keys())
    user_counts = list(city_data.values())

    # Plotting only if there is data to plot
    if cities and user_counts:
        plt.figure(figsize=(10, 6))
        bars = plt.bar(cities, user_counts, color='skyblue')
        plt.xlabel('City')
        plt.ylabel('Number of Users')
        plt.title('Number of Users in Each City')
        plt.xticks(rotation=45)
        plt.yticks(range(max(user_counts) + 1))  # Set y-axis ticks as integers

        # Add annotations to each bar
        for bar, count in zip(bars, user_counts):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 0.1, str(count), ha='center', va='bottom', fontsize=9)

        plt.tight_layout()

        # Convert plot to base64 for embedding in HTML
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

        return f'<img src="data:image/png;base64,{plot_url}">'

    else:
        return "No data available to plot."

if __name__ == '__main__':
    app.run(debug=True)

