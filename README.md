Farm Input Expense Tracker
Smart Farming · Expense Analytics · Profit Calculation

A lightweight and powerful Flask + MySQL web application that helps farmers digitally track expenses, record crop yield, and automatically compute profit.
It also provides graphs, PDF reports, and crop-wise comparison for better decision-making.

🚜 ✨ Key Features at a Glance
1️⃣ Expense Management

Add daily expenses: seeds, fertilizers, pesticides, labour, machinery, fuel, irrigation

Categorized by crop & date

View and delete records instantly

2️⃣ Yield Tracking

Record harvested quantity & selling price

System auto-calculates total income per crop

3️⃣ Profit & Analysis

Net Profit = Total Income – Total Expense

Crop-wise financial comparison table

4️⃣ Visual Analytics

Matplotlib bar chart showing:

Expense vs Income vs Net Profit (per crop)

5️⃣ PDF Report Export

Professional report generated using ReportLab

Includes expense, income, and profit details for all crops

🧰 Tech Stack
Component	Technology
Backend	Flask (Python)
Database	MySQL
Visualization	Matplotlib
Reporting	ReportLab (PDF)
Frontend	HTML · CSS · Bootstrap · Jinja2
📦 Core Python Imports
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from config import get_db_connection
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
