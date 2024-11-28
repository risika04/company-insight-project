from flask import Flask, request, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt
import io
import matplotlib.style as style

app = Flask(__name__)

# Read the CSV file
data = pd.read_csv("All_companies.csv", usecols=[2, 3, 4, 5, 6, 7, 8])

@app.route('/')
def Search():
    return render_template('index.html')

@app.route('/plot/')
def plot():
    return render_template('plot.html')

@app.route('/submit', methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        industry = str(request.form.get('industry')).strip()
        location = str(request.form.get('location')).strip()
        job_type = str(request.form.get('type')).strip()
        rating = float(request.form.get('rating'))
        
        filtered_data = data[
            (data['industry'] == industry) &
            (data['location'] == location) &
            (data['type'] == job_type) &
            (data['company_rating'] == rating)
        ]
        
        filtered_html = filtered_data.to_html()

        return render_template('results.html', tables=[filtered_html], titles=[''])

@app.route('/submit_plot', methods=["GET", "POST"])
def submit_plot():
    if request.method == "POST":
        graph_type = str(request.form.get('graphType')).strip()
        column1 = str(request.form.get('column1')).strip()
        column2 = str(request.form.get('column2')).strip()

        plt.close()
        

        if graph_type == "bar":
            style.use('ggplot')
            graph=data.groupby(column2)[column1].mean().sort_values(ascending=False)
            graph.head(10).plot(kind='bar',color='orange')
            plt.xlabel(column2)
            plt.ylabel(column1)
            plt.title(f'Top 10 {column1} by {column2}')
        elif graph_type == "Scatter":
            
            plt.figure(figsize=(15, 10),dpi=200,facecolor='pink')
            plt.scatter(data[column2], data[column1])
            plt.tick_params(rotation=90)
            plt.xlabel(column1)
            plt.ylabel(column2)
            plt.yticks(fontsize=6)  
            plt.title(f'{column1} vs {column2}')


        elif graph_type == "pie":
            ratings = data[column1].value_counts().sort_values(ascending=False).head(5)
            plt.figure(figsize=(10, 6))
            plt.pie(ratings, labels=ratings.index, autopct="%.1f%%", startangle=140, colors=plt.cm.Paired.colors)
            plt.title(f'{column1} Distribution')


        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        
        return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
