import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
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

        # Expense amount input with validation
        ttk.Label(input_frame, text="Expense Amount:").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(input_frame, textvariable=self.expense_amount)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)
        self.amount_entry.focus()  # Set focus to the amount entry field
        self.amount_entry.bind('<FocusOut>', self.validate_amount)

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

        # Validate amount and date before adding expense
        if self.validate_amount(event=None) and self.validate_date(event=None):
            try:
                float(amount)
            except ValueError:
                messagebox.showerror("Invalid Amount", "Please enter a valid number for the expense amount.")
                self.amount_entry.focus()
                return

            # Insert expense into table
            self.expense_table.insert("", "end", values=(amount, currency, category, date, method))

            # Calculate total expenses
            total_expenses = 0.0
            for item in self.expense_table.get_children():
                values = self.expense_table.item(item, 'values')
                try:
                    total_expenses += float(values[0])
                except ValueError:
                    continue  # Skip non-numeric values
            self.total_label.config(text=f"Total Expenses: ${total_expenses:.2f}")

            # Clear input fields after adding expense
            self.clear_input_fields()

    def validate_amount(self, event):
        try:
            float(self.expense_amount.get())
            return True
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid number for the expense amount.")
            self.amount_entry.focus()
            return False

    def validate_date(self, event):
        try:
            datetime.strptime(self.expense_date.get(), '%Y-%m-%d')
            return True
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in the format YYYY-MM-DD.")
            self.date_entry.focus()
            return False

    def clear_input_fields(self):
        self.expense_amount.set("")
        self.expense_currency.set("USD")
        self.expense_category.set("Life Expenses")
        self.expense_date.set(datetime.today().strftime('%Y-%m-%d'))
        self.payment_method.set("Cash")
        self.amount_entry.focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
