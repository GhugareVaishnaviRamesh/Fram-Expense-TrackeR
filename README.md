Farm Input Expense Tracker

Smart Farming 

Expense Analytics 

Profit Calculation

The Farm Input Expense Tracker is a lightweight yet powerful Flask + MySQL web application designed to help farmers digitally record expenses, track crop yield, and calculate profit automatically.
It also provides graphs, PDF reports, and crop-wise comparisons to support better and more informed agricultural decisions.

Features
1. Expense Management
Add daily farming expenses such as seeds, fertilizers, pesticides, labour, machinery, irrigation, and fuel.
All expenses are categorized by crop name and date.
View, manage, and delete expense records instantly.
Helps farmers maintain accurate digital expense logs.

3. Yield Tracking
Record harvested crop quantity,
Enter selling price per unit,
System automatically calculates total income per crop.

5. Profit Analysis
Automatically computes:
Net Profit = Total Income – Total Expense,
Crop-wise financial breakdown,
Helps farmers identify the most profitable crops.

4. Visual Analytics
Matplotlib bar chart showing:
Total Expense,
Total Income,
Net Profit,
Chart helps in comparing the financial performance of each crop visually.

5. PDF Report Generation
Generates a professional PDF report using ReportLab.
Includes:
Crop name,
Total expense,
Total income,
Net profit.

Tech Stack
Component	Technology,
Backend	Flask (Python),
Database	MySQL,
Visualization	Matplotlib,
Reporting	ReportLab (PDF),
Frontend	HTML, CSS, Bootstrap, Jinja2.

Core Python Imports
from flask import Flask, render_template, request, redirect, url_for, flash, Response

from config import get_db_connection

import matplotlib.pyplot as plt

from io import BytesIO

from reportlab.lib.pagesizes import A4

from reportlab.pdfgen import canvas
