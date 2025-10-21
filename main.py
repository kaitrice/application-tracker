from db import init_db, load_data, seed_db
from visualization.chart_bar import bar_chart_by_status


print("*"*21)
print(" APPLICATION TRACKER ")
print("*"*21)

init_db()
seed_db()

bar_chart_by_status()