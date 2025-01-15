import sys
import sqlite3
import tkinter as tk
from tkinter import ttk

# Connect to SQLite database
conn = sqlite3.connect("/Users/priyankam/Documents/UTA ASSIGNMENTS/FOUNDATION OF COMPUTING/db_project/railwaytest.db")
cursor = conn.cursor()
conn.commit()

class RailwayBookingApp:
    def __init__(self, master):
        self.master = master
        master.title("Railway Booking Application")
        # Create and configure the GUI elements
        self.setup_ui()

    def setup_ui(self):
        # Query 1
        query1_label = ttk.Label(self.master, text="1. Find trains for a passenger")
        passenger_last_name_entry = ttk.Entry(self.master)
        passenger_first_name_entry = ttk.Entry(self.master)
        query1_button = ttk.Button(self.master, text="Search Trains",command=lambda: self.query_trains_for_passenger(passenger_last_name_entry.get(),passenger_first_name_entry.get()))

        # Query 2
        query2_label = ttk.Label(self.master, text="2. List passengers for a date with confirmed tickets")
        name_entry = ttk.Entry(self.master)
        query2_button = ttk.Button(self.master, text="Show Passengers",command=lambda: self.show_passengers_for_date_with_name(name_entry.get()))

        # Query 3
        query3_label = ttk.Label(self.master, text="3. Display train and passenger info for a specific age group")
        age_group_entry = ttk.Entry(self.master)
        query3_button = ttk.Button(self.master, text="Display Info",command=lambda: self.display_info_for_age_group(age_group_entry.get()))

        # Query 4
        query4_label = ttk.Label(self.master, text="4. List all train names along with passenger count")
        query4_button = ttk.Button(self.master, text="List Trains", command=self.list_trains_with_passenger_count)

        # Query 5
        query5_label = ttk.Label(self.master, text="5. Retrieve passengers with confirmed status for a train")
        train_name_entry = ttk.Entry(self.master)
        query5_button = ttk.Button(self.master, text="Get Passengers", command=lambda: self.retrieve_passengers_for_train(train_name_entry.get()))

        # Query 6
        query6_label = ttk.Label(self.master, text="6. Cancel a ticket and update waiting list")
        passenger_id_entry = ttk.Entry(self.master)
        travel_date_entry = ttk.Entry(self.master)
        query6_button = ttk.Button(self.master, text="Cancel Ticket", command=lambda: self.cancel_ticket_and_update_waiting_list(passenger_id_entry.get(), travel_date_entry.get()))

        # Grid layout for widgets
        query1_label.grid(row=0, column=0, pady=5)
        passenger_last_name_entry.grid(row=1, column=0, pady=5)
        passenger_first_name_entry.grid(row=2, column=0, pady=5)
        query1_button.grid(row=3, column=0, pady=5)

        query2_label.grid(row=4, column=0, pady=5)
        name_entry.grid(row=5, column=0, pady=5)
        query2_button.grid(row=6, column=0, pady=5)

        query3_label.grid(row=7, column=0, pady=5)
        age_group_entry.grid(row=8, column=0, pady=5)
        query3_button.grid(row=9, column=0, pady=5)

        query4_label.grid(row=10, column=0, pady=5)
        query4_button.grid(row=11, column=0, pady=5)

        query5_label.grid(row=12, column=0, pady=5)
        train_name_entry.grid(row=13, column=0, pady=5)
        query5_button.grid(row=14, column=0, pady=5)

        query6_label.grid(row=15, column=0, pady=5)
        passenger_id_entry.grid(row=16, column=0, pady=5)
        travel_date_entry.grid(row=17, column=0, pady=5)
        query6_button.grid(row=18, column=0, pady=5)

        self.result_text = tk.Text(self.master, height=20, width=60)
        self.result_text.grid(row=19, column=0, pady=10, columnspan=2)


    def execute_query(self, query):
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            self.display_results(result)
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

    def display_results(self, result):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)


    #Query1
    def query_trains_for_passenger(self, last_name, first_name):
        query = (f"SELECT * FROM train JOIN booked ON train.Train_Number = booked.Train_Number JOIN passenger ON booked.Passanger_ssn = passenger.ssn WHERE passenger.Last_Name = '{first_name}' AND passenger.First_Name='{last_name}'")
        cursor.execute(query)
        result = cursor.fetchall()
        self.display_results(result)

    # Query2
    def show_passengers_for_date_with_name(self, name):
        query = f"SELECT P.* FROM passenger P JOIN booked B ON p.ssn = B.Passanger_ssn AND B.Status='Booked' JOIN train T ON B.Train_Number = T.Train_Number JOIN train_status TS ON T.Train_Name = TS.Train_Name WHERE TS.Train_Date = '{name}'"
        cursor.execute(query)
        result = cursor.fetchall()
        self.display_results(result)
        pass

    # Query3
    def display_info_for_age_group(self, age_given):
        age_query = """SELECT strftime('%Y', 'now') - strftime('%Y', substr(bdate, 7, 4) || '-' || substr(bdate, 1, 2) || '-' || substr(bdate, 4, 2)) AS age, ssn FROM passenger """
        cursor.execute(age_query)
        result = cursor.fetchall()
        filtered_result = [t[1] for t in result if t[0] == int(age_given)]
        placeholders = ', '.join(['?' for _ in filtered_result])
        query = f"SELECT t.*, p.First_Name, p.Last_Name, p.address, b.Ticket_Type as Category, b.Status FROM train t JOIN booked b ON t.Train_Number = b.Train_Number JOIN passenger p ON b.Passanger_ssn = p.ssn WHERE p.ssn IN ({placeholders})"
        cursor.execute(query, filtered_result)
        result = cursor.fetchall()
        self.display_results(result)

    # Query4
    def list_trains_with_passenger_count(self):
        query = "SELECT t.Train_Name, COUNT(b.Passanger_ssn) FROM train t LEFT JOIN booked b ON t.Train_Number = b.Train_Number GROUP BY t.Train_Name"
        cursor.execute(query)
        result = cursor.fetchall()
        self.display_results(result)

    # Query5
    def retrieve_passengers_for_train(self, train_name):
        query = f"SELECT * FROM passenger p JOIN booked b ON p.ssn = b.Passanger_ssn JOIN train t ON b.Train_Number = t.Train_Number WHERE t.Train_name='{train_name}' AND Status = 'Booked'"
        cursor.execute(query)
        result = cursor.fetchall()
        self.display_results(result)

    # Query6
    def cancel_ticket_and_update_waiting_list(self, passenger_id, travel_date):
        try:
            # need to fetch the details of the deleting record
            q1 = f"SELECT Passanger_ssn,Train_Number, Ticket_Type FROM booked WHERE Passanger_ssn = '{passenger_id}' AND Status='Booked' LIMIT 1"
            cursor.execute(q1)
            q1_result = cursor.fetchall()
            print(q1_result)
            train_num = q1_result[0][0]
            category = q1_result[0][1]
            print("1 completd")
            # perform Deletion
            q2 = f"DELETE FROM booked WHERE Passanger_ssn = '{passenger_id}' AND Status = 'Booked' AND ROWID IN (SELECT ROWID FROM booked WHERE Passanger_ssn ='{passenger_id}' AND Status = 'Booked' LIMIT 1)"
            cursor.execute(q2)
            q2_result = cursor.fetchall()
            conn.commit()
            # update the booked table
            q4 = f"SELECT Passanger_ssn, Train_Number,  Status FROM booked WHERE Train_Number = '{train_num}' AND Status='WaitL' LIMIT 1"
            cursor.execute(q4)
            result = cursor.fetchall()
            q3 = f"UPDATE booked SET Status = 'Booked' WHERE Train_Number = '{train_num}' AND Status = 'WaitL' AND ROWID IN (SELECT ROWID FROM booked WHERE Train_Number = '{train_num}' AND Status = 'WaitL' LIMIT 1 )"
            cursor.execute(q3)
            q3_result = cursor.fetchall()
            conn.commit()
            q1_result_str = "\n".join(map(str, q1_result))
            output = f"Deleted is :{q1_result_str}"
            self.display_results(output)
            conn.commit()

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RailwayBookingApp(root)
    root.mainloop()
    sys.exit(app.exec_())