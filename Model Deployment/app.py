import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load model and feature names
with open('model_XGB_GridSearchCV.pkl', 'rb') as file_1:
    grid_search_XGB= joblib.load( file_1)

with open('Selected_features.txt', 'rb') as file_2:
    Selected = joblib.load(file_2)

# Set up app title and header image
st.set_page_config(page_title='Profit Prediction', page_icon=':money_with_wings:')
st.title('Profit Prediction')
st.image('https://i.imgur.com/pi5ccYK.png', use_column_width=True)


# Load dataset
df = pd.read_csv("data_sales.csv")

# FOR DATAFRAME
# Create Streamlit app
st.title('DATA FRAME STORE')

# Display raw data if checkbox is selected
if st.checkbox('Show raw data'):
    st.write(df)

# Filter data and display inference
st.header('Filter Data & Inference')
Market = st.selectbox('Market', df['Market'].unique())
Product_type = st.selectbox('Product Type', df['Product Type'].unique())

# Filter data based on selected options
filtered_data = df[(df['Product Type'] == Product_type) & (df['Market'] == Market)]

# Display filtered data
st.write(f'Number of entries: {len(filtered_data)}')
st.write(filtered_data)

# Create line plot
sns.set_style('darkgrid')

# Convert 'Date' column to datetime objects
df['Date'] = pd.to_datetime(df['Date'])

# FOR INTERACTIVE LINE PLOT
# Convert 'Date' column to datetime objects
st.header('Interactiv Line Plot')
df['Date'] = pd.to_datetime(df['Date'])

# Add date range slider to select data range
min_date = df['Date'].min()
max_date = df['Date'].max()
start_date = st.date_input('Start date', min_date)
end_date = st.date_input('End date', max_date)

if start_date <= end_date:
    st.success('Start date: `{}`\n\nEnd date:`{}`'.format(start_date, end_date))
else:
    st.error('Error: End date must fall after start date.')

# Convert start_date and end_date to datetime objects
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data based on selected date range
filtered_data = df[(df['Product Type'] == Product_type) & (df['Market'] == Market) & (df['Date'] >= start_date) & (df['Date'] <= end_date)]

# Create line plot based on filtered data
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='Date', y='Profit', data=filtered_data, ax=ax, color='red', linewidth=2, label='Profit')
sns.lineplot(x='Date', y='Sales', data=filtered_data, ax=ax, color='blue', linewidth=2, label='Sales')
ax.set_xlabel('Date')
ax.set_ylabel('Total')
ax.set_title('Total Sales and Profit by Date')
ax.tick_params(axis='both', which='major', labelsize=12)
ax.legend()

# Display plot in Streamlit
st.pyplot(fig)

# FOR COMPARE LINE PLOT
st.header('Comparison Line Plot')
sns.set_style('darkgrid')

fig, axes = plt.subplots(ncols=2, figsize=(18, 6))

for i, col in enumerate(['Profit', 'Sales']):
    df.groupby('Date')[col].sum().plot(kind='line', ax=axes[i], color='red', linewidth=2)
    axes[i].set_xlabel('Date')
    axes[i].set_ylabel(f'Total {col}')
    axes[i].set_title(f'Total {col} by Date')
    axes[i].tick_params(axis='both', which='major', labelsize=12)

    max_date = df.groupby('Date')[col].sum().idxmax()
    min_date = df.groupby('Date')[col].sum().idxmin()
    max_val = df.groupby('Date')[col].sum().max()
    min_val = df.groupby('Date')[col].sum().min()

    axes[i].annotate('Highest', xy=(max_date, max_val), xytext=(max_date, max_val+500),
                arrowprops=dict(facecolor='black', arrowstyle='->'), fontsize=12)
    axes[i].annotate('Lowest', xy=(min_date, min_val), xytext=(min_date, min_val-500),
                arrowprops=dict(facecolor='black', arrowstyle='->'), fontsize=12)

st.pyplot(fig)








### For Predict ###

# Collect user input using sliders
st.title('Lets Predict Our Profit')
st.subheader('Enter Your Store Data:')
Area_Code = st.selectbox('Area Code', tuple([203,206,209,210,212,213,214,216,217,224,225,234,239,253,254,262,281,303,305,309,310,312,314,315,318,
                                           319,321,323,325,330,337,339,347,351,352,360,361,386,405,407,408,409,413,414,415,417,419,425,430,432,
                                           435,440,469,475,503,504,505,508,509,510,512,513,515,516,518,530,541,559,561,562,563,567,573,580,585,
                                           603,607,608,614,617,618,619,626,630,631,636,641,646,650,660,661,682,702,707,708,712,713,714,715,716,
                                           718,719,720,727,740,754,760,772,773,774,775,781,786,801,805,806,813,815,816,817,818,830,831,832,845,
                                           847,850,857,858,860,863,903,904,909,914,915,916,917,918,920,925,936,937,940,941,949,951,954,956,959,970,
                                           971,972,978,979,985]))
State = st.selectbox('State', tuple(['Connecticut', 'Washington', 'California', 'Texas', 'New York', 'Ohio', 
                                     'Illinois', 'Louisiana', 'Florida', 'Wisconsin', 'Colorado', 'Missouri', 'Iowa', 
                                     'Massachusetts', 'Oklahoma', 'Utah', 'Oregon', 'New Mexico', 'New Hampshire', 'Nevada']))

Market_Size = st.selectbox('Market Size', tuple(('Small Market', 'Major Market')))

Product = st.selectbox('Product', tuple(('Columbian','Green Tea','Caffe Mocha','Decaf Espresso','Lemon','Mint','Darjeeling',
                                         'Decaf Irish Cream','Chamomile','Earl Grey','Caffe Latte','Amaretto','Regular Espresso')))

Total_Expenses = st.slider('Total Expenses $', 0,1000)
Inventory = st.slider ('Inventory $', 0,10000)
Sales = st.slider ('Sales $', 0, 1000)


# Generate new DataFrame based on user input
new_data = pd.DataFrame({
    'Area Code': [Area_Code],
    'State': [State],
    'Market Size': [Market_Size],
    'Product': [Product],
    'Total Expenses': [Total_Expenses],
    'Inventory': [Inventory],
    'Sales': [Sales]
})



if st.button('Predict'):
  profit_pred = grid_search_XGB.predict(new_data)
  st.subheader('Profit Store: ${:.2f}'.format(profit_pred[0]))
