import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
from datetime import datetime

# Load your dataset
crime_data = pd.read_excel(r"D:\Data Science\Projects\My Projects\Project 11\Sample Crime Dataset.xlsx")

# Convert 'Date' to datetime
crime_data['Date'] = pd.to_datetime(crime_data['Date'])

# Extract temporal features
crime_data['Month'] = crime_data['Date'].dt.month
crime_data['DayOfWeek'] = crime_data['Date'].dt.dayofweek
crime_data['Hour'] = crime_data['Date'].dt.hour

# Create a PDF report
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Detailed Crime Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_image(self, image_path, x, y, w, h):
        self.image(image_path, x, y, w, h)

# Initialize PDF
pdf = PDF()
pdf.add_page()

# Report Introduction
pdf.chapter_title('Introduction')
pdf.chapter_body('This report provides a detailed analysis of crime trends, hotspots, and other critical insights based on historical crime data.')

# Trend Analysis: Crimes Over Time
pdf.chapter_title('Crime Trends Over Time')
crime_counts_by_year = crime_data['Date'].dt.year.value_counts().sort_index()
plt.figure(figsize=(10, 6))
crime_counts_by_year.plot(kind='bar')
plt.title('Number of Crimes by Year')
plt.xlabel('Year')
plt.ylabel('Number of Crimes')
plt.tight_layout()
plt.savefig('crimes_by_year.png')
pdf.add_image('crimes_by_year.png', 10, pdf.get_y(), 190, 100)

# Hotspot Analysis: Crime Locations
pdf.add_page()
pdf.chapter_title('Crime Hotspots')
plt.figure(figsize=(10, 6))
sns.kdeplot(x=crime_data['Longitude'], y=crime_data['Latitude'], cmap='Reds', fill=True, thresh=0.05)
plt.title('Crime Hotspots')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.savefig('crime_hotspots.png')
pdf.add_image('crime_hotspots.png', 10, pdf.get_y(), 190, 100)

# Crime by Type
pdf.add_page()
pdf.chapter_title('Crime by Type')
crime_type_counts = crime_data['Primary Type'].value_counts()
plt.figure(figsize=(10, 6))
crime_type_counts.plot(kind='bar')
plt.title('Number of Crimes by Type')
plt.xlabel('Crime Type')
plt.ylabel('Number of Crimes')
plt.tight_layout()
plt.savefig('crime_by_type.png')
pdf.add_image('crime_by_type.png', 10, pdf.get_y(), 190, 100)

# Temporal Analysis: Crimes by Hour
pdf.add_page()
pdf.chapter_title('Crime by Hour of the Day')
crime_counts_by_hour = crime_data['Hour'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
crime_counts_by_hour.plot(kind='bar', color='skyblue')
plt.title('Number of Crimes by Hour')
plt.xlabel('Hour')
plt.ylabel('Number of Crimes')
plt.tight_layout()
plt.savefig('crime_by_hour.png')
pdf.add_image('crime_by_hour.png', 10, pdf.get_y(), 190, 100)

# Save PDF
pdf.output('Detailed_Crime_Report.pdf')

print('Report generated successfully.')
