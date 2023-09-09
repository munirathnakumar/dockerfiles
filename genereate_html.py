import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Template
import io
import base64

# Load your Excel file (replace 'data.xlsx' with your file path)
xls_file = pd.ExcelFile('data.xlsx')

# Read data from the sheets named "Threat," "Threat 2," and "Threat 3"
threat_sheet = xls_file.parse('Threat')
threat2_sheet = xls_file.parse('Threat 2')
threat3_sheet = xls_file.parse('Threat 3')

# Calculate counts for each sheet
threat_count = len(threat_sheet)
threat2_count = len(threat2_sheet)
threat3_count = len(threat3_sheet)

# Create pie charts for the "Risk" column in each sheet with legends
def create_pie_chart(data, labels, title):
    plt.figure(figsize=(6, 6))
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    
    # Add a legend
    plt.legend(labels, loc='upper right', bbox_to_anchor=(1.1, 1))

    plt.tight_layout()
    
    # Save the chart as binary data
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

threat_chart = create_pie_chart(threat_sheet['Risk'].value_counts(), threat_sheet['Risk'].unique(), 'Threat Sheet Risk Distribution')
threat2_chart = create_pie_chart(threat2_sheet['Risk'].value_counts(), threat2_sheet['Risk'].unique(), 'Threat 2 Sheet Risk Distribution')
threat3_chart = create_pie_chart(threat3_sheet['Risk'].value_counts(), threat3_sheet['Risk'].unique(), 'Threat 3 Sheet Risk Distribution')

# Convert chart images to base64
threat_chart_b64 = base64.b64encode(threat_chart).decode()
threat2_chart_b64 = base64.b64encode(threat2_chart).decode()
threat3_chart_b64 = base64.b64encode(threat3_chart).decode()

# Create Jinja2 template for the HTML page
template = Template("""
<!DOCTYPE html>
<html>
<head>
    <title>Excel Data Visualization</title>
    <style>
        /* CSS styles for the page (background, text, etc.) */
        body {
            background-color: black;
            color: white;
            font-family: Arial, sans-serif;
        }
        /* Define styles for tables, charts, and other elements as needed */
        .static-table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 10px;
        }
        .static-table th, .static-table td {
            border: 1px solid white;
            padding: 8px;
            text-align: center;
        }
        .static-table th {
            background-color: #333;  /* Change heading background color */
            color: white;  /* Change heading text color */
        }
        .chart-container {
            display: flex;
        }
        .chart {
            flex: 1;
            padding: 10px;
        }
        .chart img {
            max-width: 100%;
        }
        .dynamic-table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 10px;
        }
        .dynamic-table th, .dynamic-table td {
            border: 1px solid white;
            padding: 8px;
            text-align: center;
        }
        .high {
            background-color: red;
            color: white;
        }
        .medium {
            background-color: orange;
            color: white;
        }
        .low {
            background-color: green;
            color: white;
        }
    </style>
</head>
<body>
    <!-- Static table at the top -->
    <table class="static-table">
        <tr>
            <th>Threat Count</th>
            <th>Threat 2 Count</th>
            <th>Threat 3 Count</th>
        </tr>
        <tr>
            <td>{{ threat_count }}</td>
            <td>{{ threat2_count }}</td>
            <td>{{ threat3_count }}</td>
        </tr>
    </table>

    <!-- Pie charts -->
    <div class="chart-container">
        <div class="chart">
            <img src="data:image/png;base64,{{ threat_chart_b64 }}" alt="Threat Sheet Risk Distribution" />
        </div>
        <div class="chart">
            <img src="data:image/png;base64,{{ threat2_chart_b64 }}" alt="Threat 2 Sheet Risk Distribution" />
        </div>
        <div class="chart">
            <img src="data:image/png;base64,{{ threat3_chart_b64 }}" alt="Threat 3 Sheet Risk Distribution" />
        </div>
    </div>

    <!-- Dynamic tables for Excel data -->
    <h2>Threat Sheet</h2>
    <table class="dynamic-table">
        <tr>
            {% for column in threat_sheet.columns %}
            <th>{{ column }}</th>
            {% endfor %}
        </tr>
        {% for _, row in threat_sheet.iterrows() %}
        <tr>
            {% for column in threat_sheet.columns %}
            {% if column == 'Severity' %}
                <td class="{% if row[column] == 'High' %}high{% elif row[column] == 'Medium' %}medium{% else %}low{% endif %}">{{ row[column] }}</td>
            {% else %}
                <td>{{ row[column] }}</td>
            {% endif %}
            {% endfor %}
        </tr>
        {% endfor %}
    </table>

    <!-- Add tables for Threat 2 Sheet and Threat 3 Sheet similarly -->

</body>
</html>
""")

# Render the template with data and pie chart images
html_output = template.render(
    threat_count=threat_count,
    threat2_count=threat2_count,
    threat3_count=threat3_count,
    threat_chart_b64=threat_chart_b64,
    threat2_chart_b64=threat2_chart_b64,
    threat3_chart_b64=threat3_chart_b64,
)

# Save the HTML to a file or serve it in a web application
with open('output.html', 'w') as file:
    file.write(html_output)
