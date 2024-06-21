import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
crime_data = pd.read_excel(r"D:\Data Science\Projects\My Projects\Project 11\Sample Crime Dataset.xlsx")

# Convert 'Date' to datetime
crime_data['Date'] = pd.to_datetime(crime_data['Date'])

# Extract temporal features
crime_data['Month'] = crime_data['Date'].dt.month
crime_data['DayOfWeek'] = crime_data['Date'].dt.dayofweek
crime_data['Hour'] = crime_data['Date'].dt.hour

# Streamlit app
st.title('Crime Data Dashboard')
st.sidebar.header('Filter Options')

# Sidebar filters
crime_type = st.sidebar.selectbox('Select Crime Type', crime_data['Primary Type'].unique())
month = st.sidebar.slider('Select Month', 1, 12, (1, 12))
hour = st.sidebar.slider('Select Hour', 0, 23, (0, 23))

# Filter data based on user input
filtered_data = crime_data[
    (crime_data['Primary Type'] == crime_type) &
    (crime_data['Month'].between(month[0], month[1])) &
    (crime_data['Hour'].between(hour[0], hour[1]))
]

# Display filtered data
st.subheader(f'Displaying {len(filtered_data)} records')
st.dataframe(filtered_data)

# Plot crime locations
st.subheader('Crime Locations')
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='Longitude', y='Latitude', data=filtered_data, hue='Primary Type', alpha=0.5, ax=ax)
st.pyplot(fig)

# Plot crime count by hour
st.subheader('Crime Count by Hour')
hourly_crime_count = filtered_data['Hour'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(10, 6))
hourly_crime_count.plot(kind='bar', ax=ax)
ax.set_xlabel('Hour')
ax.set_ylabel('Number of Crimes')
st.pyplot(fig)
