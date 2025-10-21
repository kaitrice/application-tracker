from db import load_data
import plotly.express as px

def bar_chart_by_status():
    data = load_data()
    if data.empty:
        print("No data available to plot.")
        return
    status_counts = data['status'].value_counts().reset_index()
    fig = px.bar(
        status_counts,
        x='status',
        y='count',
        color='status',
        title='Number of Applications per Status'
    )
    fig.show()
