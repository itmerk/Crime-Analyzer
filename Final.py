import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from io import BytesIO
import time
import streamlit.components.v1 as components

st.set_page_config(layout='wide')

with st.sidebar:
    select = option_menu('Menu',['Home','Temporal Analysis','Geospatial Analysis','Crime Type Analysis','Arrest and Domestic Incident Analysis',
                                      'Location-Specific Analysis','Seasonal and Weather Impact','Repeat Offenders and Recidivism',
                                      'Predictive Modeling and Risk Assessment'])

if select == 'Home':
    st.title('Chicago Crime Analyzer')

    st.write('''Your primary objective in this role is to leverage historical and recent crime data to identify patterns, trends, and hotspots within Chicago.
    By conducting a thorough analysis of this data, you will support strategic decision-making, improve resource allocation, and contribute to reducing crime 
    rates and enhancing public safety.Your task is to provide actionable insights that can shape our crime prevention strategies, ensuring a safer and more
    secure community.This project will be instrumental in aiding law enforcement operations and enhancing the overall effectiveness of our efforts in combating 
    crime in Chicago.''')

if select == 'Temporal Analysis':
    st.header('Temporal Analysis') 
    # Read the file
    crime_data = pd.read_excel(r"D:\Data Science\Projects\My Projects\Project 11\Clean Crime Dataset.xlsx")
    tab1,tab2 = st.tabs(['Crime Trends Over Time','Peak Crime Hours'])

    with tab1:
        # Add 'All' option to filters
        year_options = ['All'] + list(crime_data['Year'].unique())
        month_options = ['All'] + list(crime_data['Month'].unique())
        day_options = ['All'] + list(crime_data['Day'].unique())

        # Sidebar filters
        coll1,coll2,coll3 = st.columns(3)
        with coll1:
            year = st.multiselect('Select Year', year_options,default=['All'])
        with coll2:    
            month = st.multiselect('Select Month', month_options,default=['All'])
        with coll3:
            day = st.multiselect('Select Day', day_options,['All'])

        # Filter data based on user input
        filtered_data = crime_data.copy()

        if 'All' not in year:
            filtered_data = filtered_data[filtered_data['Year'].isin(year)]

        if 'All' not in month:
            filtered_data = filtered_data[filtered_data['Month'].isin(month)]

        if 'All' not in day:
            filtered_data = filtered_data[filtered_data['Day'].isin(day)]

        # Display filtered data
        st.subheader(f'Displaying {len(filtered_data)} records')
        st.dataframe(filtered_data)

        # Function to convert dataframe to Excel file
        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            return output.getvalue()

        # Convert filtered data to Excel
        excel_data = to_excel(filtered_data)

        # Provide download link for the Excel file
        st.download_button(
            label="Download data as Excel",
            data=excel_data,
            file_name='filtered_data.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        if not filtered_data.empty:
            coll1,coll2,coll3 = st.columns(3)
            with coll1:    
                # Plot crime count by year
                st.subheader('Crime Count as Year')
                yearly_crime_count = filtered_data['Year'].value_counts().sort_index()
                fig, ax = plt.subplots(figsize=(4, 8))
                yearly_crime_count.plot(kind='barh', ax=ax)
                ax.set_xlabel('Number of Crimes')
                ax.set_ylabel('Year')
                st.pyplot(fig)

            with coll2:
                # Plot crime count by month
                st.subheader('Crime Count by Month')
                monthly_crime_count = filtered_data['Month'].value_counts().sort_index()
                fig, ax = plt.subplots(figsize=(4, 8))
                monthly_crime_count.plot(kind='barh', ax=ax)
                ax.set_xlabel('Number of Crimes')
                ax.set_ylabel('Month')
                st.pyplot(fig)

            with coll3:
                # Plot crime count by day
                st.subheader('Crime Count by Day')
                daily_crime_count = filtered_data['Day'].value_counts().sort_index()
                fig, ax = plt.subplots(figsize=(4, 8))
                daily_crime_count.plot(kind='barh', ax=ax)
                ax.set_xlabel('Number of Crimes')
                ax.set_ylabel('Day')
                st.pyplot(fig)
        else:
            st.subheader('No data available for the selected filters')

    with tab2:
        # Add 'All' option to filters
        day_options = ['All'] + list(crime_data['Day'].unique())

        # Sidebar filters
        coll1,coll2,coll3 = st.columns(3)
        with coll1:
            day = st.multiselect('Select Day for crime per hour', day_options,default=['All'])

        # Filter data based on user input
        filtered_data = crime_data.copy()

        # Filter data based on user input
        if 'All' not in day:
            filtered_data = filtered_data[filtered_data['Day'].isin(day)]

        # Display filtered data
        st.subheader(f'Displaying {len(filtered_data)} records')
        st.dataframe(filtered_data)

        # Function to convert dataframe to Excel file
        st.subheader('Peak Crime Hours')

        if not filtered_data.empty:
            crime_per_hour = filtered_data['Hour'].value_counts().sort_index()
            # Plotting the trend
            fig, ax = plt.subplots(figsize=(15, 4))
            crime_per_hour.plot(kind='bar', ax=ax)
            ax.set_xlabel('Time')
            ax.set_ylabel('Number of Crimes')
            st.pyplot(fig)
        else:
            st.subheader('No data available for the selected filters')


if select == 'Geospatial Analysis':
    st.header('Geospatial Analysis')    
    crime_data = pd.read_excel(r"D:\Data Science\Projects\My Projects\Project 11\Clean Crime Dataset.xlsx")
    tab1,tab2 = st.tabs(['Crime Hotspots','District/Ward Analysis']) 

    with tab1:
        st.subheader('Crime Locations based on Heatmap')
        map_center = [crime_data['Latitude'].mean(), crime_data['Longitude'].mean()]
                
        # Create a Folium map centered around the mean latitude and longitude
        crime_map = folium.Map(location=map_center, zoom_start=12)

        # Prepare heat data
        heat_data = [[row['Latitude'], row['Longitude']] for index, row in crime_data.iterrows()]

        # Add HeatMap to the Folium map
        HeatMap(heat_data).add_to(crime_map)

        # Display the map in the Streamlit app
        folium_static(crime_map, width=1300, height=600)

    with tab2:
        st.subheader('Crime Rate across different District and Ward')
        tab1,tab2 = st.tabs(['District Analysis','Ward Analysis']) 

        with tab1:
            # Add 'All' option to filters
            primary_type_options = ['All'] + list(crime_data['Primary Type'].unique())
            district_options = ['All'] + list(crime_data['District'].unique())

            # Sidebar filters
            coll1,coll2 = st.columns(2)
            with coll1:
                primary_type = st.multiselect('Select Crime type', primary_type_options,default='All')
            with coll2:
                district = st.multiselect('Select district', district_options,default='All')

            # Filter data based on user input
            filtered_data = crime_data.copy()

            # Filter data based on user input
            if 'All' not in primary_type:
                filtered_data = filtered_data[filtered_data['Primary Type'].isin(primary_type)]     

            if 'All' not in district:
                filtered_data = filtered_data[filtered_data['District'].isin(district)]         

            # Display filtered data
            st.subheader(f'Displaying {len(filtered_data)} records')
            st.dataframe(filtered_data)

            # Function to convert dataframe to Excel file
            def to_excel(df):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Sheet1')
                return output.getvalue()

            # Convert filtered data to Excel
            excel_data = to_excel(filtered_data)

            # Provide download link for the Excel file
            st.download_button(
                label="Download data as Excel",
                data=excel_data,
                file_name='filtered_data.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

            st.header('No of Crime across District')
            if not filtered_data.empty:
                crime_per_district = filtered_data['District'].value_counts().sort_index()
                # Plotting the trend
                fig, ax = plt.subplots(figsize=(15, 6))
                crime_per_district.plot(kind='bar', ax=ax)
                ax.set_xlabel('District')
                ax.set_ylabel('Number of Crimes')
                st.pyplot(fig)
            else:
                st.subheader('No data available for the selected filters')

        with tab2:
            # Add 'All' option to filters
            primary_type_options = ['All'] + list(crime_data['Primary Type'].unique())
            ward_options = ['All'] + list(crime_data['Ward'].unique())

            # Sidebar filters
            coll1,coll2 = st.columns(2)
            with coll1:
                primary_type = st.multiselect('Select Crime Type', primary_type_options,default='All')
            with coll2:
                ward = st.multiselect('Select Ward', ward_options,default='All')

            # Filter data based on user input
            filtered_data = crime_data.copy()

            # Filter data based on user input
            if 'All' not in primary_type:
                filtered_data = filtered_data[filtered_data['Primary Type'].isin(primary_type)]     

            if 'All' not in ward:
                filtered_data = filtered_data[filtered_data['Ward'].isin(ward)] 

            # Display filtered data
            st.subheader(f'Displaying {len(filtered_data)} records')
            st.dataframe(filtered_data)

            # Function to convert dataframe to Excel file
            def to_excel(df):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Sheet1')
                return output.getvalue()

            # Convert filtered data to Excel
            excel_data = to_excel(filtered_data)

            # Provide download link for the Excel file
            st.download_button(
                label="Download data as Excel",
                data=excel_data,
                file_name='filtered_data as ward.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

            st.header('No of Crime across Ward')
            if not filtered_data.empty:
                crime_per_ward = filtered_data['Ward'].value_counts().sort_index()
                # Plotting the trend
                fig, ax = plt.subplots(figsize=(15, 10))
                crime_per_ward.plot(kind='barh', ax=ax,color='skyblue')
                ax.set_xlabel('Number of Crimes')
                ax.set_ylabel('Ward')
                st.pyplot(fig)
            else:
                st.subheader('No data available for the selected filters')

if select == "Crime Type Analysis":
    st.header('Crime Type Analysis')    
    crime_data = pd.read_excel(r"D:\Data Science\Projects\My Projects\Project 11\Clean Crime Dataset.xlsx")
    tab1,tab2 = st.tabs(['Distribution of Crime Types','Severity Analysis']) 

    with tab1:
        primary_type_options = ['All'] + list(crime_data['Primary Type'].unique())

        # Sidebar filters
        coll1,coll2,coll3 = st.columns(3)
        with coll1:
            primary_type = st.multiselect('Select Primary Type', primary_type_options,default='All')

        # Filter data based on user input
        filtered_data = crime_data.copy()

        # Filter data based on user input
        if 'All' not in primary_type:
            filtered_data = filtered_data[filtered_data['Primary Type'].isin(primary_type)] 

        # Display filtered data
        st.subheader(f'Displaying {len(filtered_data)} records')
        st.dataframe(filtered_data)

        # Function to convert dataframe to Excel file
        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            return output.getvalue()

        # Convert filtered data to Excel
        excel_data = to_excel(filtered_data)

        # Provide download link for the Excel file
        st.download_button(
            label="Download data as Excel",
            data=excel_data,
            file_name='filtered_data.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        st.header('No of Crime across Description')
        if not filtered_data.empty:
            crime_per_ward = filtered_data['Description'].value_counts().sort_index()
            # Plotting the trend
            fig, ax = plt.subplots(figsize=(15, 25))
            crime_per_ward.plot(kind='barh', ax=ax,color='skyblue')
            ax.set_xlabel('Number of Crimes')
            ax.set_ylabel('Description')
            st.pyplot(fig)

        else:
            st.subheader('No data available for the selected filters')

    with tab2:
        st.header('Severity Analysis')

        severe_crimes = ['HOMICIDE','CRIMINAL SEXUAL ASSAULT','BATTERY','KIDNAPPING','ROBBERY','SEX OFFENSE','ARSON','NARCOTICS','WEAPONS VIOLATION']
        less_severe_crimes = ['BURGLARY','THEFT','MOTOR VEHICLE THEFT','ASSAULT','STALKING','CRIMINAL DAMAGE','CRIMINAL TRESPASS','PROSTITUTION','OFFENSE INVOLVING CHILDREN'
                        ,'DECEPTIVE PRACTICE','OTHER OFFENSE','CONCEALED CARRY LICENSE VIOLATION','INTERFERENCE WITH PUBLIC OFFICER','PUBLIC PEACE VIOLATION']
            
        # Categorize crimes
        crime_data['Severity'] = crime_data['Primary Type'].apply(
            lambda x: 'Severe' if x in severe_crimes else 'Less Severe'
        )

        # Streamlit multiselect
        primary_type_options = ['All'] + list(crime_data['Primary Type'].unique())
        coll1,coll2,coll3 = st.columns(3)
        with coll1:
            selected_crime_types = st.multiselect('Select Crime Types', primary_type_options, default='All')

        # Function to filter data based on selection
        def filter_crime_data(selected_types):
            if 'All' in selected_types:
                return crime_data
            return crime_data[crime_data['Primary Type'].isin(selected_types)]

        # Filtered data
        filtered_data = filter_crime_data(selected_crime_types)

        # Display the filtered data
        st.subheader(f'Displaying {len(filtered_data)} records')
        st.dataframe(filtered_data)

        # Function to convert dataframe to Excel file
        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            return output.getvalue()

        # Convert filtered data to Excel
        excel_data = to_excel(filtered_data)

        # Provide download link for the Excel file
        st.download_button(
            label="Download data as Excel",
            data=excel_data,
            file_name='filtered_data_crime_type.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
        if not filtered_data.empty:
            # Calculate distribution of severe vs. less severe crimes
            severity_distribution = filtered_data.groupby('Severity')['Arrest'].sum().reset_index()

            # Detailed distribution of each crime type
            plt.figure(figsize=(14, 8))
            crime_distribution = filtered_data.groupby(['Severity', 'Primary Type'])['Arrest'].sum().unstack()
            crime_distribution.T.plot(kind='barh', stacked=True)
            plt.xlabel('Crime Type')
            plt.ylabel('Arrest')
            plt.title('Detailed Distribution of Crime Types by Severity')
            plt.legend(title='Severity')
            st.pyplot(plt)
        else:
            st.subheader('No data available for the selected filters')

if select == "Arrest and Domestic Incident Analysis":
    st.header('Arrest and Domestic Incident Analysis')    
    crime_data = pd.read_excel(r"D:\Data Science\Projects\My Projects\Project 11\Clean Crime Dataset.xlsx")
    tab1,tab2 = st.tabs(['Arrest Rates','Domestic vs. Non-Domestic Crimes']) 

    with tab1:
        primary_type_options = ['All'] + list(crime_data['Primary Type'].unique())

        # Sidebar filters
        coll1,coll2,coll3 = st.columns(3)
        with coll1:
            primary_type = st.multiselect('Select Crime Type for Arrest', primary_type_options,default=['All'])

        # Filter data based on user input
        filtered_data = crime_data.copy()

        # Filter data based on user input
        if 'All' not in primary_type:
            filtered_data = filtered_data[filtered_data['Primary Type'].isin(primary_type)] 

        # Display filtered data
        st.subheader(f'Displaying {len(filtered_data)} records')
        st.dataframe(filtered_data)

        # Function to convert dataframe to Excel file
        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            return output.getvalue()

        # Convert filtered data to Excel
        excel_data = to_excel(filtered_data)

        # Provide download link for the Excel file
        st.download_button(
            label="Download data as Excel",
            data=excel_data,
            file_name='filtered_data_by_arrest.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        if not filtered_data.empty:
            coll1,coll2,coll3,coll4 = st.columns(4)
            with coll1:
                # Plot arrest rate by crime type
                arrest_rate_by_crime_type = filtered_data.groupby('Primary Type')['Arrest'].mean() * 100
                plt.figure(figsize=(7,14))
                arrest_rate_by_crime_type.sort_values(ascending=False).plot(kind='bar')
                plt.title('Arrest Rate by Crime Type')
                plt.xlabel('Primary Type')
                plt.ylabel('Arrest Rate (%)')
                st.pyplot(plt)

            with coll2:
                arrest_rate_by_district = filtered_data.groupby('District')['Arrest'].mean() * 100
                plt.figure(figsize=(7,14))
                arrest_rate_by_district.sort_values(ascending=False).plot(kind='bar')
                plt.title('Arrest Rate by District')
                plt.xlabel('District')
                plt.ylabel('Arrest Rate (%)')
                st.pyplot(plt)

            with coll3:
                arrest_rate_by_ward = filtered_data.groupby('Ward')['Arrest'].mean() * 100
                plt.figure(figsize=(7,14))
                arrest_rate_by_ward.sort_values(ascending=False).plot(kind='bar')
                plt.title('Arrest Rate by Ward')
                plt.xlabel('Ward')
                plt.ylabel('Arrest Rate (%)')
                st.pyplot(plt)

            with coll4:
                arrest_rate_by_year = filtered_data.groupby('Year')['Arrest'].mean()*100
                plt.figure(figsize=(7,14))
                arrest_rate_by_year.sort_values(ascending=False).plot(kind='bar')
                plt.title('Arrest Rate by Year')
                plt.xlabel('Year')
                plt.ylabel('Arrest Rate (%)')
                st.pyplot(plt)

        else:
            st.subheader('No data available for the selected filters')

    with tab2:
        primary_type_options = ['All'] + list(crime_data['Primary Type'].unique())

        # Sidebar filters
        coll1,coll2,coll3 = st.columns(3)
        with coll1:
            primary_type = st.multiselect('Select Crime Type', primary_type_options,default=['All'])

        # Filter data based on user input
        filtered_data = crime_data.copy()

        # Filter data based on user input
        if 'All' not in primary_type:
            filtered_data = filtered_data[filtered_data['Primary Type'].isin(primary_type)] 

        # Display filtered data
        st.subheader(f'Displaying {len(filtered_data)} records')
        st.dataframe(filtered_data)

        # Function to convert dataframe to Excel file
        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            return output.getvalue()

        # Convert filtered data to Excel
        excel_data = to_excel(filtered_data)

        # Provide download link for the Excel file
        st.download_button(
            label="Download data as Excel",
            data=excel_data,
            file_name='filtered_data_by_domestic_crime.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        # Calculate the number of domestic and non-domestic incidents
        domestic_crimes = filtered_data[filtered_data['Domestic'] == True]
        non_domestic_crimes = filtered_data[filtered_data['Domestic'] == False]

        # Calculate the number of domestic and non-domestic incidents by primary type
        domestic_crimes_by_type = domestic_crimes['Primary Type'].value_counts()
        non_domestic_crimes_by_type = non_domestic_crimes['Primary Type'].value_counts()

        combined_df = pd.DataFrame({
            'Domestic': domestic_crimes_by_type,
            'Non-Domestic': non_domestic_crimes_by_type
        })

        if not filtered_data.empty:
        # Plot the grouped bar chart
            plt.figure(figsize=(14, 7))
            combined_df.plot(kind='barh', color=['orange', 'blue'], alpha=0.6)
            plt.title('Domestic vs. Non-Domestic Incidents by Crime Type')
            plt.xlabel('Number of Incidents')
            plt.ylabel('Primary Type')
            plt.legend(title='Crime Type')
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
            st.pyplot(plt)  # Adjust layout to prevent clipping of labels
        else:
            st.subheader('No data available for the selected filters')

        # Calculate the arrest rates for domestic and non-domestic incidents
        domestic_arrest_rate = domestic_crimes['Arrest'].mean() * 100
        non_domestic_arrest_rate = non_domestic_crimes['Arrest'].mean() * 100

        st.write(f'Domestic Arrest Rate: {domestic_arrest_rate:.2f}%')
        st.write(f'Non-Domestic Arrest Rate: {non_domestic_arrest_rate:.2f}%')

if select == "Location-Specific Analysis":
    st.header('Location-Specific Analysis')    
    crime_data = pd.read_excel(r"D:\Data Science\Projects\My Projects\Project 11\Clean Crime Dataset.xlsx")
    tab1,tab2 = st.tabs(['Location Description Analysis','Comparison by Beat and Community Area']) 

    with tab1:
        st.header('Location Description Analysis')

        Location_Description_options = ['All'] + list(crime_data['Location Description'].unique())

        # Sidebar filters
        coll1,coll2 = st.columns(2)
        with coll1:
            Location_Description_type = st.multiselect('Select Location Description', Location_Description_options,default=['All'])

        # Filter data based on user input
        filtered_data = crime_data.copy()

        # Filter data based on user input
        if 'All' not in Location_Description_type:
            filtered_data = filtered_data[filtered_data['Location Description'].isin(Location_Description_type)] 

        # Display filtered data
        st.subheader(f'Displaying {len(filtered_data)} records')
        st.dataframe(filtered_data)

        # Function to convert dataframe to Excel file
        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            return output.getvalue()

        # Convert filtered data to Excel
        excel_data = to_excel(filtered_data)

        # Provide download link for the Excel file
        st.download_button(
            label="Download data as Excel",
            data=excel_data,
            file_name='filtered_data_by_location_description.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
        if not filtered_data.empty:
            # Analyze the most common locations for crimes
            location_counts = filtered_data['Description'].value_counts().sort_index(ascending=True)

            # Plot the most common locations for crimes
            plt.figure(figsize=(14, 15))
            location_counts.plot(kind='barh')
            plt.title('Most Common Locations for Crimes')
            plt.xlabel('Frequency')
            plt.ylabel('Location Description')
            st.pyplot(plt)
        else:
            st.subheader('No data available for the selected filters')

    with tab2:
        st.subheader('Comparison by Beat and Community Area')
        # Analyze crime data by beat
        Beat_options = ['All'] + list(crime_data['Beat'].unique())

        # Sidebar filters
        coll1,coll2 = st.columns(2)
        with coll1:
            Beat_type = st.multiselect('Select Beat', Beat_options,default=['All'])

        # Filter data based on user input
        filtered_data = crime_data.copy()

        # Filter data based on user input
        if 'All' not in Beat_type:
            filtered_data = filtered_data[filtered_data['Beat'].isin(Beat_type)] 

        # Display filtered data
        st.subheader(f'Displaying {len(filtered_data)} records')
        st.dataframe(filtered_data)

        # Function to convert dataframe to Excel file
        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            return output.getvalue()

        # Convert filtered data to Excel
        excel_data = to_excel(filtered_data)

        # Provide download link for the Excel file
        st.download_button(
            label="Download data as Excel",
            data=excel_data,
            file_name='filtered_data.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        if not filtered_data.empty:
            coll1,coll2 = st.columns(2)
            with coll1:
                crimes_by_beat = filtered_data['Beat'].value_counts().sort_values(ascending=False).head(50)
                # Plot crimes by beat
                plt.figure(figsize=(7, 25))
                crimes_by_beat.plot(kind='barh')
                plt.title('Crimes by Beat')
                plt.xlabel('Number of Crimes')
                plt.ylabel('Beat')
                st.pyplot(plt)

            with coll2:
                # Analyze crime data by community area
                crimes_by_community_area = filtered_data['Community Area'].value_counts().sort_values(ascending=False).head(50)
                # Plot crimes by community area
                plt.figure(figsize=(7,25))
                crimes_by_community_area.plot(kind='barh')
                plt.title('Crimes by Community Area')
                plt.xlabel('Number of Crimes')
                plt.ylabel('Community Area')
                st.pyplot(plt)
        else:
            st.subheader('No data available for the selected filters')

if select == "Seasonal and Weather Impact":
    st.header('Seasonal and Weather Impact')
    st.subheader('Seasonal Trends')    
    crime_data = pd.read_excel(r"D:\Data Science\Projects\My Projects\Project 11\Clean Crime Dataset.xlsx")

    Season_options = ['All'] + list(crime_data['Season'].unique())

    # Sidebar filters
    coll1,coll2 = st.columns(2)
    with coll1:
        Season_type = st.multiselect('Select Season', Season_options,default=['All'])
    
    # Filter data based on user input
    filtered_data = crime_data.copy()

    # Filter data based on user input
    if 'All' not in Season_type:
        filtered_data = filtered_data[filtered_data['Season'].isin(Season_type)] 

    # Display filtered data
    st.subheader(f'Displaying {len(filtered_data)} records')
    st.dataframe(filtered_data)

    # Function to convert dataframe to Excel file
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        return output.getvalue()

    # Convert filtered data to Excel
    excel_data = to_excel(filtered_data)

    # Provide download link for the Excel file
    st.download_button(
        label="Download data as Excel",
        data=excel_data,
        file_name='filtered_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    if not filtered_data.empty:
        coll1,coll2 = st.columns(2)
        with coll1:
            # Analyze the number of crimes by season
            crimes_by_season = filtered_data['Season'].value_counts()
            # Plot the number of crimes by season
            plt.figure(figsize=(14, 10))
            crimes_by_season.plot(kind='bar', color=['blue', 'green', 'red', 'orange'])
            plt.title('Number of Crimes by Season')
            plt.xlabel('Season')
            plt.ylabel('Number of Crimes')
            st.pyplot(plt)

        with coll2:
            # Analyze the number of crimes by primary type and season
            crimes_by_type_and_season = filtered_data.groupby(['Season', 'Primary Type']).size().unstack().fillna(0)

            # Plot a heatmap of crimes by primary type and season
            plt.figure(figsize=(14, 10))
            sns.heatmap(crimes_by_type_and_season, cmap='YlGnBu', annot=True, fmt='.0f')
            plt.title('Crimes by Primary Type and Season')
            plt.xlabel('Primary Type')
            plt.ylabel('Season')
            st.pyplot(plt)
    else:
        st.subheader('No data available for the selected filters')

if select == "Repeat Offenders and Recidivism":
    st.header('Repeat Offenders and Recidivism')    
    crime_data = pd.read_excel(r"D:\Data Science\Projects\My Projects\Project 11\Clean Crime Dataset.xlsx")
    tab1,tab2 = st.tabs(['Repeat Crime Locations','Recidivism Rates']) 

    with tab1:
        st.write('Identify locations that are repeatedly associated with criminal activity.')

        Location_Description_options = ['All'] + list(crime_data['Location Description'].unique())

        # Sidebar filters
        coll1,coll2 = st.columns(2)
        with coll1:
            Location_Description_type = st.multiselect('Select Location_Description_', Location_Description_options,default=['All'])

        # Filter data based on user input
        filtered_data = crime_data.copy()

        # Filter data based on user input
        if 'All' not in Location_Description_type:
            filtered_data = filtered_data[filtered_data['Location Description'].isin(Location_Description_type)] 

        # Display filtered data
        st.subheader(f'Displaying {len(filtered_data)} records')
        st.dataframe(filtered_data)

        # Function to convert dataframe to Excel file
        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            return output.getvalue()

        # Convert filtered data to Excel
        excel_data = to_excel(filtered_data)

        # Provide download link for the Excel file
        st.download_button(
            label="Download data as Excel",
            data=excel_data,
            file_name='filtered_data.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        if not filtered_data.empty:
            # Plot crime count by year
            st.subheader('Repeat No of Crime')
            repeat_crime_count = filtered_data['Primary Type'].value_counts().sort_index()
            fig, ax = plt.subplots(figsize=(15, 6))
            repeat_crime_count.plot(kind='barh', ax=ax)
            ax.set_xlabel('Number of Crimes')
            ax.set_ylabel('Primary Type')
            st.pyplot(fig)
        else:
            st.subheader('No data available for the selected filters')

    with tab2:
        if st.button('Calculate Recidivism Rates'):
            with st.spinner('Calculating...'):
                time.sleep(1.5)
                # Count total arrests
                total_arrests = crime_data[crime_data['Arrest'] == True].shape[0]

                # Filter for incidents where there was a subsequent arrest within 1 year
                recidivism_criteria = crime_data[(crime_data['Arrest'] == True) & (crime_data['Year'] == crime_data['Year'] + 1)]

                # Count incidents meeting recidivism criteria
                recidivism_count = recidivism_criteria.shape[0]

                # Calculate recidivism rate
                recidivism_rate = (recidivism_count / total_arrests) * 100

                st.write(f"Recidivism Rate: {recidivism_rate:.2f}%")

if select == "Predictive Modeling and Risk Assessment":
    st.header('Predictive Modeling and Risk Assessment')    
    crime_data = pd.read_excel(r"D:\Data Science\Projects\My Projects\Project 11\Clean Crime Dataset.xlsx")
    tab1,tab2 = st.tabs(['Predictive Analysis','Risk Assessment']) 

    with tab1:
        st.write("Develop models to predict future crime incidents based on historical data, time, location, and other relevant factors")
        HtmlFile = open(r"D:\Data Science\Projects\My Projects\Project 11\high_risk_areas_map.html")
        source_code = HtmlFile.read() 
        components.html(source_code,height = 500)
    
    with tab2:
        st.write("Assess the risk of different areas and times for specific types of crimes to help in resource allocation for law enforcement.")
        HtmlFile = open(r"D:\Data Science\Projects\My Projects\Project 11\predicted_high_risk_areas_map.html")
        source_code = HtmlFile.read() 
        components.html(source_code,height = 500)