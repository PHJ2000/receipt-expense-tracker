import sqlite3
from flask import Flask, request, jsonify
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import logging

app = Flask(__name__)

# 환경 변수 로드
load_dotenv()
endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

# Form Recognizer 클라이언트 설정
form_recognizer_client = FormRecognizerClient(endpoint, AzureKeyCredential(key))

# 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY, 
                    merchant TEXT, 
                    date TEXT, 
                    total REAL,
                    items TEXT)''')
    conn.commit()
    conn.close()

# 앱 시작 시 데이터베이스 초기화
init_db()

def analyze_receipt(file_path):
    with open(file_path, "rb") as receipt:
        poller = form_recognizer_client.begin_recognize_receipts(receipt)
        result = poller.result()

    receipt_info = {}
    for receipt in result:
        receipt_info["Merchant Name"] = receipt.fields.get("MerchantName").value if receipt.fields.get("MerchantName") else None
        receipt_info["Transaction Date"] = receipt.fields.get("TransactionDate").value if receipt.fields.get("TransactionDate") else None
        receipt_info["Total"] = receipt.fields.get("Total").value if receipt.fields.get("Total") else None
        receipt_info["Items"] = [{"name": item.value.get("Name").value, "price": item.value.get("TotalPrice").value} for item in receipt.fields.get("Items").value] if receipt.fields.get("Items") else None

    return receipt_info

@app.route('/upload', methods=['POST'])
def upload_receipt():
    try:
        file = request.files['file']
        file_path = f"./uploads/{file.filename}"
        file.save(file_path)
        
        receipt_info = analyze_receipt(file_path)
        
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("INSERT INTO expenses (merchant, date, total, items) VALUES (?, ?, ?, ?)",
                  (receipt_info["Merchant Name"], receipt_info["Transaction Date"], receipt_info["Total"], str(receipt_info["Items"])))
        conn.commit()
        conn.close()

        return jsonify(receipt_info)
    except Exception as e:
        logging.error(f"Error processing receipt: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/report', methods=['GET'])
def report():
    try:
        month = request.args.get('month')
        year = request.args.get('year')
        
        report_data = get_monthly_report(month, year)
        chart_path = create_report_chart(report_data, month, year)
        
        return jsonify({
            'total_expense': report_data['total_expense'],
            'expense_by_merchant': report_data['expense_by_merchant'],
            'details': report_data['details'],
            'report_image': chart_path
        })
    except Exception as e:
        logging.error(f"Error generating report: {e}")
        return jsonify({"error": str(e)}), 500

def get_monthly_report(month, year):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT merchant, date, total, items FROM expenses WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?", (month, year))
    rows = c.fetchall()
    conn.close()
    
    total_expense = sum(row[2] for row in rows)
    expense_by_merchant = {}
    for row in rows:
        merchant = row[0]
        if merchant in expense_by_merchant:
            expense_by_merchant[merchant] += row[2]
        else:
            expense_by_merchant[merchant] = row[2]
    
    return {
        'total_expense': total_expense,
        'expense_by_merchant': expense_by_merchant,
        'details': rows
    }

def create_report_chart(report_data, month, year):
    merchants = list(report_data['expense_by_merchant'].keys())
    expenses = list(report_data['expense_by_merchant'].values())

    plt.figure(figsize=(10, 5))
    plt.bar(merchants, expenses, color='blue')
    plt.xlabel('Merchant')
    plt.ylabel('Expense')
    plt.title(f'Expenses by Merchant for {month}/{year}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    chart_path = f'report_{year}_{month}.png'
    plt.savefig(chart_path)
    plt.close()
    return chart_path

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
