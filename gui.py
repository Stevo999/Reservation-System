import mysql.connector
import tkinter as tk

# Create a connection to the database
conn = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="rrs"
)
c = conn.cursor()

# Create the main window
root = tk.Tk()
root.title("Railway Reservation System")

# Function to execute the SQL query and display the results in a listbox
def execute_query(query):
    c.execute(query)
    rows = c.fetchall()
    listbox.delete(0, tk.END)
    for row in rows:
        listbox.insert(tk.END, row)

# Function to retrieve trains booked by a specific passenger
def retrieve_trains_by_passenger():
    last_name = entry_last_name.get()
    first_name = entry_first_name.get()
    query = "SELECT TrainNumber, TrainName FROM Passenger, Train, Ticket WHERE Passenger.LastName = '{}' AND Passenger.FirstName = '{}' AND Passenger.PassengerID = Ticket.PassengerID AND Ticket.TrainNumber = Train.TrainNumber".format(last_name, first_name)
    execute_query(query)

# Function to retrieve passengers with confirmed tickets on a specific day
def retrieve_confirmed_passengers_by_day():
    day = entry_day.get()
    query = "SELECT FirstName, LastName FROM Passenger, Ticket WHERE Passenger.PassengerID = Ticket.PassengerID AND Ticket.Status = 'confirmed' AND DAY(Ticket.BookingDate) = '{}'".format(day)
    execute_query(query)

# Function to retrieve train and passenger information for passengers aged 50 to 60
def retrieve_train_and_passenger_info_by_age():
    query = "SELECT TrainNumber, TrainName, Source, Destination, FirstName, LastName, Address, Category, Status FROM Passenger, Train, Ticket WHERE Passenger.Age BETWEEN 50 AND 60 AND Passenger.PassengerID = Ticket.PassengerID AND Ticket.TrainNumber = Train.TrainNumber"
    execute_query(query)

# Function to retrieve train names and passenger counts
def retrieve_train_passenger_counts():
    query = "SELECT TrainName, COUNT(*) FROM Passenger, Ticket, Train WHERE Passenger.PassengerID = Ticket.PassengerID AND Ticket.TrainNumber = Train.TrainNumber GROUP BY TrainName"
    execute_query(query)

# Function to retrieve passengers with confirmed tickets for a specific train
def retrieve_passengers_by_train():
    train_name = entry_train_name.get()
    query = "SELECT FirstName, LastName FROM Passenger, Ticket, Train WHERE Passenger.PassengerID = Ticket.PassengerID AND Ticket.TrainNumber = Train.TrainNumber AND Train.TrainName = '{}' AND Ticket.Status = 'confirmed'".format(train_name)
    execute_query(query)

# Function to delete a passenger's record and update waiting list
def delete_passenger_record():
    passenger_id = entry_passenger_id.get()
    query = "DELETE FROM Ticket WHERE PassengerID = '{}'".format(passenger_id)
    c.execute(query)
    conn.commit()
    query = "SELECT PassengerID FROM Ticket WHERE Status = 'waiting' ORDER BY BookingDate ASC LIMIT 1"
    c.execute(query)
    result = c.fetchone()
    if result is not None:
        waiting_passenger_id = result[0]
        query = "UPDATE Ticket SET Status = 'confirmed' WHERE PassengerID = '{}'".format(waiting_passenger_id)
        c.execute(query)
        conn.commit()
    execute_query("SELECT * FROM Passenger")

# Create the UI elements
label_last_name = tk.Label(root, text="Last Name:")
label_last_name.grid(row=0, column=0)
entry_last_name = tk.Entry(root)
entry_last_name.grid(row=0, column=1)
label_first_name = tk.Label(root, text="First Name:")
label_first_name.grid(row=1, column=0)
entry_first_name = tk.Entry(root)
entry_first_name.grid(row=1, column=1)

button_passenger_trains = tk.Button(root, text="Find Trains", command=retrieve_trains_by_passenger)
button_passenger_trains.grid(row=2, column=0, columnspan=2)

label_day = tk.Label(root, text="Day:")
label_day.grid(row=3, column=0)
entry_day = tk.Entry(root)
entry_day.grid(row=3, column=1)

button_confirmed_passengers = tk.Button(root, text="Find Confirmed Passengers", command=retrieve_confirmed_passengers_by_day)
button_confirmed_passengers.grid(row=4, column=0, columnspan=2)

button_age_passengers = tk.Button(root, text="Find Passengers Aged 50-60", command=retrieve_train_and_passenger_info_by_age)
button_age_passengers.grid(row=5, column=0, columnspan=2)

button_train_passenger_counts = tk.Button(root, text="Find Train Passenger Counts", command=retrieve_train_passenger_counts)
button_train_passenger_counts.grid(row=6, column=0, columnspan=2)

label_train_name = tk.Label(root, text="Train Name:")
label_train_name.grid(row=7, column=0)
entry_train_name = tk.Entry(root)
entry_train_name.grid(row=7, column=1)

button_train_passengers = tk.Button(root, text="Find Passengers on Train", command=retrieve_passengers_by_train)
button_train_passengers.grid(row=8, column=0, columnspan=2)

label_passenger_id = tk.Label(root, text="Passenger ID:")
label_passenger_id.grid(row=9, column=0)
entry_passenger_id = tk.Entry(root)
entry_passenger_id.grid(row=9, column=1)

button_delete_passenger = tk.Button(root, text="Delete Passenger Record", command=delete_passenger_record)
button_delete_passenger.grid(row=10, column=0, columnspan=2)

listbox = tk.Listbox(root)
listbox.grid(row=11, column=0, columnspan=2)

root.mainloop()