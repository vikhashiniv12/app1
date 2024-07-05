from flask import Flask
import firebase_admin
from firebase_admin import credentials, db
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Your service account key JSON as a Python dictionary
service_account_key = {
    "type": "service_account",
    "project_id": "user-65c40",
    "private_key_id": "cb3722552a39d941d6de5150758542c08c5348cb",
    "private_key": b"-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCgwYruMQy04EAt\nHIwYpdBR+8vQ94R4siDxNQMS8rK77fO3DBOalkzNIgp42ksmBvkQeaIg/CyYG+CZ\noDoVt5+hSjo7DYnYjeJjPFZSMRAmXQAfxlTC41opwo0Sh1LhpOjyTUjIgyYNjgPG\nYZN3PxRlSY5yH/3Vj/YOHmUtBwp9S68w7qxxr2nQc7SlXeuaVpYAmqlBcNp7lOwc\nomdF0xUakoDk4qxrbUDrLZrGvvdC1372x5SuwNYBqfNwcOmGs4PIO2FL40bWlAYk\nGncOOCwRQChSEZC2P3RjesOukSSkc4G7ISyWLEzE4kYXZ5jwODIq6uGrZf2yzMPd\nNx8fZ+W1AgMBAAECggEAFMY2M0Zk7zn8qSfDhgrlkzawNerKtINGhQ1V/pydEvKy\n+GCH5wYN2kOQKWKCbCFiDeo+FLep9qVBnvDJGNXgO+p5AHklK3ZYf30EZb4/6UlC\n8xhBC2dwly10aCTTReQ3E1r/8SObpwxHehtRgItHEjjRfveZ6L+gK15rskgy55KM\nHED2cGiUZblNEdiZVB+CZoOHr3JWQH30mpnAuo5cduCPuRoQLFuB/QBzPoedGXjB\nQl7oZeEzGNRBHR0pPyyjZmQ8mvJ0F7MC+TVaz8HSzxTckXtrMGyjgAuY5gNHsWGQ\nN2Lz+uv+rs6ciUNckhSk7PE4wV+GbFNa0v/2mi5YwQKBgQDLyZTW8CAgbpV8xLTz\nyGOdgfB15UFmcecrgyOgAIQMEe9j9LB4pTxClmVZgYDf+ZqSCmo+R8EN7PV6x7au\nt+GKqGYmQWUlIKGWxFckZvlss7q+vxqyBkls9OejU04Y9+dv0BAcHj4kuYpoQnVx\nuv6Lw574kzK9OskNKCXSTh6V9QKBgQDJ8YgLlgm2PFPiEuRnduFLc7t6FZy5tWop\ncLNe+H/MYjTfRS+Ofs/6Hy0wyjFWvM7JU8QftJixbrPp8kD+UjKhGEmDlImhwVbl\nldBlO2Ivyjo17a0K9aO1RPbcsKXUKjFqkWaUnfyhyh6dII3lLcSK+jm7BpWhuosU\nrgvVXRZ4wQKBgF1hptmDOUWDRu7geIbJSZRwaY6smfZmtWaD9jwoYFnjkg38nyz5\nko50ukZ0iGiZyRGowhx95uIJtkcn4vdW/Xv7RKu9Basos8MRf1kH8r2z8hvcGFCB\nfv31j3uQ/dWFK8FZ1zf7R8CuYNT7tzOBW4kR//OqB/McT+q+fe5Lq8pNAoGAX4W4\nbIKUJXdz1kRJdgdtmlssGxuN/uopRWDh99Jj4TGzAMmhLS4fApksrx91Jyo4RlMx\nOi4a",
    "client_email": "firebase-adminsdk-rgi4e@user-65c40.iam.gserviceaccount.com",
    "client_id": "101021074565361512418",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-rgi4e%40user-65c40.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com",
    "databaseURL": "https://user-65c40-default-rtdb.firebaseio.com"
}

# Initialize Firebase with your credentials
cred = credentials.Certificate(service_account_key)
firebase_admin.initialize_app(cred, {
    'databaseURL': service_account_key['databaseURL']
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
