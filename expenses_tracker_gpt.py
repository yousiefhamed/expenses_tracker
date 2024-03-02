import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from currency_converter import CurrencyConverter

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        # Variables for user input
        self.expense_amount = tk.StringVar(value="0")  # Set initial value to 0
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

        # Currency selection
        ttk.Label(input_frame, text="Currency:").grid(row=1, column=0, padx=5, pady=5)
        self.currency_combobox = ttk.Combobox(input_frame, textvariable=self.expense_currency, values=list(CurrencyConverter().currencies))
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
        self.expense_table.bind("<Double-1>", self.edit_expense)  # Double-click to edit expense
        self.expense_table.bind("<Delete>", self.delete_expense)  # Delete selected expense on pressing Delete key

        # Total expense label
        self.total_label = ttk.Label(self.root, text="Total Expenses: $0", font=("Arial", 12, "bold"), foreground="blue")
        self.total_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.converter = CurrencyConverter()

    def calculate_total_expenses(self):
        total_expenses_usd = 0.0
        for item in self.expense_table.get_children():
            values = self.expense_table.item(item, 'values')
            try:
                amount = float(values[0])
                currency = values[1]
                # Convert amount to USD
                usd_amount = self.converter.convert(amount, currency, 'USD')
                total_expenses_usd += usd_amount
            except ValueError:
                continue  # Skip non-numeric values
        return total_expenses_usd

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

            # Insert expense into table without converting currency
            self.expense_table.insert("", "end", values=(amount, currency, category, date, method))

            # Calculate total expenses in USD
            total_expenses_usd = self.calculate_total_expenses()
            self.total_label.config(text=f"Total Expenses: ${total_expenses_usd:.2f}")

            # Clear input fields after adding expense
            self.clear_input_fields()

    def validate_amount(self, event):
        if event:  # Check if event is not None
            try:
                float(self.expense_amount.get())
                return True
            except ValueError:
                messagebox.showerror("Invalid Amount", "Please enter a valid number for the expense amount.")
                self.amount_entry.focus()
                return False
        else:
            return True  # Always return True if event is None (for button click)

    def validate_date(self, event):
        try:
            datetime.strptime(self.expense_date.get(), '%Y-%m-%d')
            return True
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in the format YYYY-MM-DD.")
            self.date_entry.focus()
            return False

    def clear_input_fields(self):
        self.expense_amount.set("0")  # Reset amount field to 0
        self.expense_currency.set("USD")
        self.expense_category.set("Life Expenses")
        self.expense_date.set(datetime.today().strftime('%Y-%m-%d'))
        self.payment_method.set("Cash")
        self.amount_entry.focus()

    def edit_expense(self, event):
        selected_item = self.expense_table.selection()
        if selected_item:
            values = self.expense_table.item(selected_item, 'values')
            self.expense_amount.set(values[0])
            self.expense_currency.set(values[1])
            self.expense_category.set(values[2])
            self.expense_date.set(values[3])
            self.payment_method.set(values[4])

            self.expense_table.delete(selected_item)  # Delete selected expense after editing

    def delete_expense(self, event):
        selected_item = self.expense_table.selection()
        if selected_item:
            self.expense_table.delete(selected_item)

            # Recalculate total expenses after deleting expense
            total_expenses_usd = self.calculate_total_expenses()
            self.total_label.config(text=f"Total Expenses: ${total_expenses_usd:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
