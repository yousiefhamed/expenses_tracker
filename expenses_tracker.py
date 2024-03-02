import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry  # Import the DateEntry widget from tkcalendar
from datetime import datetime

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        # Variables for user input
        self.expense_amount = tk.StringVar()
        self.expense_currency = tk.StringVar()
        self.expense_category = tk.StringVar()
        self.expense_date = tk.StringVar()
        self.payment_method = tk.StringVar()

        # Expense input frame
        input_frame = ttk.LabelFrame(self.root, text="Add Expense")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Expense amount input
        ttk.Label(input_frame, text="Expense Amount:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.expense_amount).grid(row=0, column=1, padx=5, pady=5)

        # Currency selection
        ttk.Label(input_frame, text="Currency:").grid(row=1, column=0, padx=5, pady=5)
        self.currency_combobox = ttk.Combobox(input_frame, textvariable=self.expense_currency, values=["USD", "EUR", "GBP", "JPY"])
        self.currency_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.currency_combobox.set("USD")

        # Expense category input
        ttk.Label(input_frame, text="Expense Category:").grid(row=2, column=0, padx=5, pady=5)
        self.category_combobox = ttk.Combobox(input_frame, textvariable=self.expense_category, values=["Life Expenses", "Electricity", "Gas", "Rental", "Grocery", "Savings", "Education", "Charity"])
        self.category_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.category_combobox.set("Life Expenses")

        # Expense date input with DateEntry widget
        ttk.Label(input_frame, text="Expense Date:").grid(row=3, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(input_frame, textvariable=self.expense_date, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)
        self.date_entry.set_date(datetime.today())  # Set default date to today

        # Payment method input
        ttk.Label(input_frame, text="Payment Method:").grid(row=4, column=0, padx=5, pady=5)
        self.payment_combobox = ttk.Combobox(input_frame, textvariable=self.payment_method, values=["Cash", "Credit Card", "Paypal"])
        self.payment_combobox.grid(row=4, column=1, padx=5, pady=5)
        self.payment_combobox.set("Cash")

        # Add expense button
        ttk.Button(input_frame, text="Add Expense", command=self.add_expense).grid(row=5, columnspan=2, padx=5, pady=5)

        # Expense table
        self.expense_table = ttk.Treeview(self.root, columns=("Amount", "Currency", "Category", "Date", "Method"), show="headings")
        self.expense_table.heading("Amount", text="Amount")
        self.expense_table.heading("Currency", text="Currency")
        self.expense_table.heading("Category", text="Category")
        self.expense_table.heading("Date", text="Date")
        self.expense_table.heading("Method", text="Method")
        self.expense_table.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Total expense label
        self.total_label = ttk.Label(self.root, text="Total Expenses: $0")
        self.total_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    def add_expense(self):
        amount = self.expense_amount.get()
        currency = self.expense_currency.get()
        category = self.expense_category.get()
        date = self.expense_date.get()
        method = self.payment_method.get()

        # Insert expense into table
        self.expense_table.insert("", "end", values=(amount, currency, category, date, method))

        # Calculate total expenses
        total_expenses = sum(float(item[0]) for item in self.expense_table.get_children())
        self.total_label.config(text=f"Total Expenses: ${total_expenses:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
