import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt

def extract_pdf_data(pdf_path):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                data.extend(table)
    print(data)
    return pd.DataFrame(data)

def clean_data(df):
    # Assume first row as header
    df.columns = df.iloc[0]
    df = df[1:]
    df = df.dropna(how="all")  # Drop empty rows
    df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')
    df['Deductions'] = pd.to_numeric(df['Deductions'], errors='coerce')
    return df.dropna()

def transform_and_export(df, output_path):
    df['Net Salary'] = df['Salary'] - df['Deductions']
    df.to_csv(output_path, index=False)
    print(f"Data exported to {output_path}")

def visualize_data(df):
    df.groupby('Department')['Net Salary'].sum().plot(kind='bar')
    plt.title("Net Salary by Department")
    plt.ylabel("Total Salary")
    plt.show()


pdf_path = "sample_payslips.pdf"
output_path = "cleaned_data.csv"
raw_data = extract_pdf_data(pdf_path)
cleaned_data = clean_data(raw_data)
transform_and_export(cleaned_data, output_path)
visualize_data(cleaned_data)
