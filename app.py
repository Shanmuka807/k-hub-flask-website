from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Store user data in a list (for demonstration purposes; not suitable for production)
data = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        sport = request.form['sport']
        email = request.form['email']
        phone = request.form['phone']

        data.append({'name': name, 'sport': sport, 'email': email, 'phone': phone})
        return render_template('display.html', data=data)
    
    return render_template('input.html')

@app.route('/visualize')
def visualize():
    df = pd.DataFrame(data)
    sport_counts = df['sport'].value_counts()

    # Create a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(sport_counts, labels=sport_counts.index, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Favorite Sport - Pie Chart')
    plt.tight_layout()

    # Convert the pie chart to a base64-encoded image
    pie_img = BytesIO()
    plt.savefig(pie_img, format='png')
    pie_img.seek(0)
    pie_plot_url = base64.b64encode(pie_img.getvalue()).decode()

    # Create a bar graph
    sport_counts.sort_index(inplace=True)
    plt.figure(figsize=(8, 6))
    plt.bar(sport_counts.index, sport_counts.values)
    plt.xlabel('sport')
    plt.ylabel('Count')
    plt.title('Favorite sport - Bar Graph')
    plt.tight_layout()

    # Convert the bar graph to a base64-encoded image
    bar_img = BytesIO()
    plt.savefig(bar_img, format='png')
    bar_img.seek(0)
    bar_plot_url = base64.b64encode(bar_img.getvalue()).decode()

    return render_template('visualize.html', pie_plot_url=pie_plot_url, bar_plot_url=bar_plot_url)

if __name__== '__main__':
    app.run(debug=True)