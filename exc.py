import pandas as pd
from datetime import datetime

# Sample data (replace this with your data)
data = {
    'GRUPO B - COMPACTO COM AR': '87,25',
    'GRUPO C - ECONÔMICO COM AR': '93,50',
    'GRUPO CE - ECONÔMICO ESPECIAL C/AR': '101,54',
    'GRUPO CS - ECONÔMICO SEDAN C/AR': '108,68',
    'GRUPO F - INTERMEDIÁRIO': '122,97',
    'GRUPO FS - INTERMEDIÁRIO SEDAN': '137,25',
    'GRUPO FX - INTERMEDIÁRIO AUTOMÁTICO': '162,97',
    'GRUPO GC - SUV COMPACTO AUTOMÁTICO': '153,86',
    'GRUPO GX - SUV AUTOMÁTICO': '196,72',
    'GRUPO L - EXECUTIVO': '348,50'
}

# Get the current date in the format "dd/mm/yyyy"
current_date = datetime.now().strftime('%d/%m/%Y')

# Create or read the Excel file
try:
    df = pd.read_excel('car_prices.xlsx', index_col=0)
except FileNotFoundError:
    df = pd.DataFrame()

# Add the new data to the DataFrame
data[current_date] = df.index.map(lambda x: data.get(x, None))
df = pd.DataFrame(data).transpose()

# Save the updated DataFrame to the Excel file
df.to_excel('car_prices.xlsx')
