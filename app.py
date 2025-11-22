from flask import Flask, render_template, request, redirect, url_for, flash, Response
from config import get_db_connection
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


app = Flask(__name__)
app.secret_key = "farm_secret_key"

# ---------------- HOME ----------------
@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT IFNULL(SUM(amount), 0) AS total_expense FROM expenses")
    total_expense = cursor.fetchone()['total_expense']

    cursor.execute("SELECT IFNULL(SUM(total_yield * selling_price), 0) AS total_income FROM yield_data")
    total_income = cursor.fetchone()['total_income']

    conn.close()

    net_profit = total_income - total_expense
    return render_template('home.html',
                           total_expense=total_expense,
                           total_income=total_income,
                           net_profit=net_profit)

@app.route('/download_report')
def download_report():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch total expenses by crop
    cursor.execute("SELECT crop_name, SUM(amount) AS total_expense FROM expenses GROUP BY crop_name")
    expenses = cursor.fetchall()

    # Fetch total income by crop (total_yield × selling_price)
    cursor.execute("SELECT crop_name, SUM(total_yield * selling_price) AS total_income FROM yield_data GROUP BY crop_name")
    yields = cursor.fetchall()
    conn.close()

    # Merge data
    all_crops = set([e['crop_name'] for e in expenses] + [y['crop_name'] for y in yields])
    report_data = []
    for crop in all_crops:
        total_expense = next((e['total_expense'] for e in expenses if e['crop_name'] == crop), 0)
        total_income = next((y['total_income'] for y in yields if y['crop_name'] == crop), 0)
        net_profit = total_income - total_expense
        report_data.append({
            'crop_name': crop,
            'total_expense': total_expense,
            'total_income': total_income,
            'net_profit': net_profit
        })

    # Generate PDF
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, height - 50, "Farm Report Summary")

    pdf.setFont("Helvetica", 12)
    y = height - 100
    pdf.drawString(50, y, "Crop")
    pdf.drawString(200, y, "Total Expense (₹)")
    pdf.drawString(350, y, "Total Income (₹)")
    pdf.drawString(500, y, "Net Profit (₹)")
    y -= 20

    pdf.setFont("Helvetica", 11)
    for r in report_data:
        pdf.drawString(50, y, str(r['crop_name']))
        pdf.drawString(200, y, f"{r['total_expense']:.2f}")
        pdf.drawString(350, y, f"{r['total_income']:.2f}")
        pdf.drawString(500, y, f"{r['net_profit']:.2f}")
        y -= 20
        if y < 100:  # Add new page if content exceeds
            pdf.showPage()
            y = height - 100

    pdf.save()
    pdf_buffer.seek(0)

    return Response(
        pdf_buffer,
        mimetype='application/pdf',
        headers={'Content-Disposition': 'attachment;filename=farm_report.pdf'}
    )

# ---------------- ADD EXPENSE ----------------
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        date_entry = request.form['date']
        crop_name = request.form['crop_name']
        category = request.form['category']
        amount = request.form['amount']
        remarks = request.form['remarks']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO expenses (date, crop_name, category, amount, remarks)
            VALUES (%s, %s, %s, %s, %s)
        """, (date_entry, crop_name, category, amount, remarks))
        conn.commit()
        conn.close()

        flash("✅ Expense added successfully!")
        return redirect(url_for('view_expenses'))

    return render_template('add_expense.html')

# ---------------- VIEW EXPENSES ----------------
@app.route('/view_expenses')
def view_expenses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = cursor.fetchall()
    conn.close()
    return render_template('view_expenses.html', expenses=expenses)

# ---------------- DELETE EXPENSE ----------------
@app.route('/delete_expense/<int:id>')
def delete_expense(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("🗑️ Expense deleted successfully!")
    return redirect(url_for('view_expenses'))

# ---------------- ADD YIELD ----------------
@app.route('/add_yield', methods=['GET', 'POST'])
def add_yield():
    if request.method == 'POST':
        date_entry = request.form['date']
        crop_name = request.form['crop_name']
        total_yield = request.form['total_yield']
        selling_price = request.form['selling_price']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO yield_data (date, crop_name, total_yield, selling_price)
            VALUES (%s, %s, %s, %s)
        """, (date_entry, crop_name, total_yield, selling_price))
        conn.commit()
        conn.close()

        flash("✅ Yield added successfully!")
        return redirect(url_for('view_yields'))

    return render_template('add_yield.html')

# ---------------- VIEW YIELDS ----------------
@app.route('/view_yields')
def view_yields():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM yield_data ORDER BY date DESC")
    yields = cursor.fetchall()
    conn.close()
    return render_template('view_yields.html', yields=yields)

# ---------------- DELETE YIELD ----------------
@app.route('/delete_yield/<int:id>')
def delete_yield(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM yield_data WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("🗑️ Yield deleted successfully!")
    return redirect(url_for('view_yields'))

# ---------------- REPORT ----------------
@app.route('/report')
def report():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT crop_name, SUM(amount) AS total_expense FROM expenses GROUP BY crop_name")
    expenses = cursor.fetchall()

    cursor.execute("SELECT crop_name, SUM(total_yield * selling_price) AS total_income FROM yield_data GROUP BY crop_name")
    yields = cursor.fetchall()

    all_crops = set([e['crop_name'] for e in expenses] + [y['crop_name'] for y in yields])
    report_data = []

    for crop in all_crops:
        total_expense = next((e['total_expense'] for e in expenses if e['crop_name'] == crop), 0)
        total_income = next((y['total_income'] for y in yields if y['crop_name'] == crop), 0)
        net_profit = total_income - total_expense
        report_data.append({
            'crop_name': crop,
            'total_expense': total_expense,
            'total_income': total_income,
            'net_profit': net_profit
        })

    conn.close()
    return render_template('report.html', report_data=report_data)

# ---------------- GRAPH ----------------
@app.route('/expense_chart')
def expense_chart():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch total expenses by crop
    cursor.execute("SELECT crop_name, SUM(amount) AS total_expense FROM expenses GROUP BY crop_name")
    expenses = cursor.fetchall()

    # Fetch total income by crop (yield × selling_price)
    cursor.execute("SELECT crop_name, SUM(total_yield * selling_price) AS total_income FROM yield_data GROUP BY crop_name")
    yields = cursor.fetchall()
    conn.close()

    # Combine data into one structure
    all_crops = set([e['crop_name'] for e in expenses] + [y['crop_name'] for y in yields])
    crop_names = []
    total_expenses = []
    total_incomes = []
    net_profits = []

    for crop in all_crops:
        exp = next((e['total_expense'] for e in expenses if e['crop_name'] == crop), 0)
        inc = next((y['total_income'] for y in yields if y['crop_name'] == crop), 0)
        profit = inc - exp

        crop_names.append(crop)
        total_expenses.append(exp)
        total_incomes.append(inc)
        net_profits.append(profit)

    # ---- Plot Visualization ----
    plt.figure(figsize=(8, 5))
    x = range(len(crop_names))
    width = 0.25

    plt.bar([i - width for i in x], total_expenses, width=width, label='Expense', color='#e74c3c')
    plt.bar(x, total_incomes, width=width, label='Income', color='#27ae60')
    plt.bar([i + width for i in x], net_profits, width=width, label='Net Profit', color='#3498db')

    plt.xticks(x, crop_names, rotation=45)
    plt.ylabel('Amount (₹)')
    plt.title('Expense vs Income vs Profit by Crop')
    plt.legend()
    plt.tight_layout()

    # ---- Render as image ----
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return Response(img.getvalue(), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
