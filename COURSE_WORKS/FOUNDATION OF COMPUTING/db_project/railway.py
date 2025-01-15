import csv
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

file_location = '/Users/nivasm/Documents/UTA ASSIGNMENTS/FOUNDATION OF COMPUTING/db_project/RRS/'
file_list = ['booked.csv', 'Passenger.csv', 'Train_status.csv', 'Train.csv']
db_name = 'railway.db'

def get_sqlite_datatype(python_dtype):
    if python_dtype == int:
        return "INTEGER"
    elif python_dtype == float:
        return "REAL"
    else:
        return "TEXT"

def get_column_datatypes(file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        sample_row = next(reader)
        column_datatypes = []
        for col_val in next(reader):
            if col_val.isdigit():
                column_datatypes.append(int)
            else:
                try:
                    float(col_val)
                    column_datatypes.append(float)
                except ValueError:
                    column_datatypes.append(str)
        sqlite_datatypes = [get_sqlite_datatype(dtype) for dtype in column_datatypes]
        return sqlite_datatypes

def create_table_with_datatypes(table_name, column_names, column_datatypes):
    columns = ", ".join(f"\"{name}\" {dtype}" for name, dtype in zip(column_names, column_datatypes))
    create_statement = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(create_statement)
    conn.commit()
    conn.close()

def insert_data(table_name, data):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    placeholders = ", ".join("?" for _ in data)
    insert_statement = f"INSERT INTO {table_name} VALUES ({placeholders})"
    cursor.execute(insert_statement, data)
    conn.commit()
    conn.close()

def table_creation_insertion():
    for file_name in file_list:
        table_name = file_name.split('.')[0]
        column_datatypes = get_column_datatypes(file_location + file_name)
        with open(file_location + file_name, 'r', newline='') as file:
            reader = csv.reader(file)
            column_names = next(reader)
            column_names = [name.strip('\ufeff').strip() for name, dtype in zip(column_names, column_datatypes)]
            create_table_with_datatypes(table_name, column_names, column_datatypes)
            for row in reader:
                insert_data(table_name, row)

def list_tables_and_first_values():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT * FROM {table_name}")
        first_row = cursor.fetchall()
        print(f"Table: {table_name}")
        print("First row values:")
        print(first_row)
        print()

    conn.close()
# table_creation_insertion()
list_tables_and_first_values()

def execute_query(query, params=()):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

def query_1():
    passenger_first_name = entry_first_name.get()
    passenger_last_name = entry_last_name.get()
    query = "SELECT Train.\"Train Name\" FROM Train JOIN Booked ON Passenger.SSN = Booked.Passanger_ssn JOIN Passenger ON Booked.Train_Number = Train.\"Train Number\" WHERE Passenger.first_name=? AND Passenger.last_name=?"
    result = execute_query(query, (passenger_first_name, passenger_last_name))
    messagebox.showinfo("Trains Booked", "The user is booked on the following trains: \n" + "\n".join(str(row[0]) for row in result))

def query_2():
    train_date = entry_train_date.get()
    query = "SELECT Passenger.first_name, Passenger.last_name\
    FROM Passenger JOIN Booked ON Passenger.SSN = Booked.Passanger_ssn  \
    JOIN Train ON Booked.Train_Number = Train.\"Train Number\"\
    JOIN Train_Status ON Train.\"Train Name\" = Train_Status.TrainName\
    WHERE Train_Status.TrainDate = ? \
    AND Booked.Staus = 'Booked'"
    print(query)
    result = execute_query(query, (train_date,))
    print(result)
    messagebox.showinfo("Passengers with Confirmed Tickets", "Passengers with confirmed tickets on the entered date: \n" + "\n".join([f"{row[0]} {row[1]}" for row in result]))

def query_3():
    age_range = int(entry_age.get())
    start = age_range - (age_range % 10)
    end = start+10
    current_year = datetime.now().year
    start_year = current_year - start
    end_year = current_year - end

    last_two_start = str(start_year)[-2:]
    last_two_end = str(end_year)[-2:]
    query = f"""
    SELECT 
        t."Train Number", 
        t."Train Name", 
        t."Source Station", 
        t."Destination Station", 
        p.first_name, 
        p.last_name, 
        p.address, 
        b.Ticket_Type, 
        b.Staus
    FROM 
        Passenger p 
        JOIN Booked b ON p.SSN = b.Passanger_ssn 
        JOIN Train t ON b.Train_Number = t."Train Number"
    WHERE 
        CAST(substr(p.bdate, -2) AS INTEGER) BETWEEN {last_two_end} AND {last_two_start}
    """
    print(query)
    result = execute_query(query)
    result_window = tk.Toplevel()
    result_window.title(f"Passengers who born between {last_two_end} to {last_two_start}")
    tree = ttk.Treeview(result_window)
    tree["columns"] = (
    "Train Number", "Train Name", "Source", "Destination", "First Name", "Last Name", "Address", "Ticket Type",
    "Ticket Status")

    # Format columns
    tree.column("#0", width=0, stretch=tk.NO)  # Hide the first column
    tree.column("Train Number", width=100)
    tree.column("Train Name", width=100)
    tree.column("Source", width=100)
    tree.column("Destination", width=100)
    tree.column("First Name", width=100)
    tree.column("Last Name", width=100)
    tree.column("Address", width=150)
    tree.column("Ticket Type", width=100)
    tree.column("Ticket Status", width=100)

    # Add column headings
    tree.heading("Train Number", text="Train Number")
    tree.heading("Train Name", text="Train Name")
    tree.heading("Source", text="Source")
    tree.heading("Destination", text="Destination")
    tree.heading("First Name", text="First Name")
    tree.heading("Last Name", text="Last Name")
    tree.heading("Address", text="Address")
    tree.heading("Ticket Type", text="Ticket Type")
    tree.heading("Ticket Status", text="Ticket Status")

    for row in result:
        tree.insert("", tk.END, values=row)

    tree.pack(expand=True, fill="both")

def query_4():
    query = "SELECT Train.\"Train Name\" , COUNT(*) FROM Booked JOIN Train ON Booked.Train_Number = Train.\"Train Number\" GROUP BY Train.\"Train Name\""
    result = execute_query(query)
    messagebox.showinfo("Passenger Count by Train", "Passenger count by Train Name: \n" + "\n".join([f"{row[0]}: {row[1]} passengers" for row in result]))


def query_5():
    train_name = entry_train_name.get()
    query = "SELECT Passenger.first_name, Passenger.last_name FROM Booked JOIN Passenger ON Booked.Passanger_ssn  = Passenger.SSN WHERE Booked.Train_Number=(SELECT \"Train Number\" FROM Train  WHERE \"Train Name\"=?) AND Booked.Staus='Booked'"
    result = execute_query(query, (" "+train_name,))
    messagebox.showinfo("Passengers with Confirmed Tickets in a Train", "Passengers with confirmed tickets in the entered train: \n" + "\n".join([f"{row[0]} {row[1]}" for row in result]))

def cancel_ticket():
    passenger_id = passenger_id_entry.get()
    travel_date = travel_date_entry.get()

    try:
        output_show = f"""SELECT Passanger_ssn 
                        FROM booked 
                        WHERE Ticket_Type = (
                            SELECT Ticket_Type 
                            FROM booked 
                            WHERE Passanger_ssn = {passenger_id}) 
                        AND Train_Number = (
                            SELECT Train_Number 
                            FROM booked 
                            WHERE Passanger_ssn = {passenger_id}) 
                        AND Staus = 'WaitL' 
                        LIMIT 1 """
        result_show = execute_query(output_show)
        query = f"""
        UPDATE Booked
        SET Staus = 'Booked'
        WHERE Passanger_ssn = (
            SELECT Passanger_ssn
            FROM Booked
            WHERE Ticket_Type = (
                SELECT Ticket_Type
                FROM Booked
                WHERE Passanger_ssn = {passenger_id}
            )
            AND Train_Number = (
                SELECT Train_Number
                FROM Booked
                WHERE Passanger_ssn = {passenger_id}
            )
            AND Staus = 'WaitL'
            AND EXISTS (
                SELECT 1
                FROM Train_Status ts
                JOIN Train t ON TRIM(t."Train Name") = TRIM(ts.TrainName)
                WHERE ts.TrainDate = '{travel_date}'
                AND t."Train Number" = (SELECT Train_Number FROM Booked WHERE Passanger_ssn = '{passenger_id}')
                AND (ts.PremiumSeatsAvailable > 0 OR ts.GenSeatsAvailable > 0)
            )
            LIMIT 1
        );
        """
        query_delete = f"""DELETE FROM Booked WHERE Passanger_ssn = {passenger_id}"""
        print(query)
        execute_query(query)
        execute_query(query_delete)

        print(result_show)
        if result_show:
            messagebox.showinfo("Passenger SSN gets", f"Passenger SSN: {result_show[0][0]} Ticket gets confirmed and {passenger_id} Ticket gets Cancelled")
        else:
            messagebox.showinfo("No Result", "No result found.")

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {str(e)}")



# Create main window
root = tk.Tk()
root.title("Railway Reservation Application")

# Query 1: Retrieve trains booked by passenger
frame_query_1 = tk.Frame(root)
frame_query_1.pack(pady=10)
label_first_name = tk.Label(frame_query_1, text="Passenger First Name:")
label_first_name.grid(row=0, column=0)
entry_first_name = tk.Entry(frame_query_1)
entry_first_name.grid(row=0, column=1)
label_last_name = tk.Label(frame_query_1, text="Passenger Last Name:")
label_last_name.grid(row=1, column=0)
entry_last_name = tk.Entry(frame_query_1)
entry_last_name.grid(row=1, column=1)
button_query_1 = tk.Button(frame_query_1, text="Retrieve Trains Booked", command=query_1)
button_query_1.grid(row=2, column=0, columnspan=2)

# Query 2: List passengers with confirmed tickets on a specific date
frame_query_2 = tk.Frame(root)
frame_query_2.pack(pady=10)
label_train_date = tk.Label(frame_query_2, text="Train Date (YYYY-MM-DD):")
label_train_date.grid(row=0, column=0)
entry_train_date = tk.Entry(frame_query_2)
entry_train_date.grid(row=0, column=1)
button_query_2 = tk.Button(frame_query_2, text="List Passengers with Confirmed Tickets", command=query_2)
button_query_2.grid(row=0, column=2)

# Query 3: Retrieve passengers and train information for ages 50 to 60
frame_query_3 = tk.Frame(root)
frame_query_3.pack(pady=10)
entry_age = tk.Entry(frame_query_3)
entry_age.pack()
button_query_3 = tk.Button(frame_query_3, text="Retrieve Passengers and Train Info for Ages", command=query_3)
button_query_3.pack()

# Query 4: Count passengers by train
frame_query_4 = tk.Frame(root)
frame_query_4.pack(pady=10)
button_query_4 = tk.Button(frame_query_4, text="Count Passengers by Train", command=query_4)
button_query_4.pack()

# Query 5: Retrieve passengers with confirmed tickets in a train
frame_query_5 = tk.Frame(root)
frame_query_5.pack(pady=10)
label_train_name = tk.Label(frame_query_5, text="Train Name:")
label_train_name.grid(row=0, column=0)
entry_train_name = tk.Entry(frame_query_5)
entry_train_name.grid(row=0, column=1)
button_query_5 = tk.Button(frame_query_5, text="Retrieve Passengers with Confirmed Tickets", command=query_5)
button_query_5.grid(row=1, column=0, columnspan=2)

# Query 6: Cancel ticket
frame_query_6 = tk.Frame(root)
frame_query_6.pack(pady=10)
passenger_id_label = tk.Label(frame_query_6, text="Passenger ID:")
passenger_id_label.grid(row=0, column=0, pady=5)
passenger_id_entry = tk.Entry(frame_query_6)
passenger_id_entry.grid(row=0, column=1, pady=5)

travel_date_label = tk.Label(frame_query_6, text="Travel Date:")
travel_date_label.grid(row=1, column=0, pady=5)
travel_date_entry = tk.Entry(frame_query_6)
travel_date_entry.grid(row=1, column=1, pady=5)

cancel_button = tk.Button(frame_query_6, text="Cancel Ticket", command=cancel_ticket)
cancel_button.grid(row=2, column=0, columnspan=2)

root.mainloop()

