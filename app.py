from flask import Flask
import firebase_admin
from firebase_admin import credentials, db
import matplotlib.pyplot as plt
import io
import base64
import requests


app = Flask(__name__)

# Replace with the actual path to your service account key JSON file
rl = 'https://github.com/vikhashiniv12/app1/blob/main/serviceAccountKey.json'
response = requests.get(url)

print(response.text)  # Print the content to inspect it

try:
    service_account_key = response.json()  # Try to decode JSON
    # Use service_account_key in your application
except ValueError as e:
    print(f"Error decoding JSON: {e}")

# Initialize Firebase with your credentials
cred = credentials.Certificate(service_account_key)
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
