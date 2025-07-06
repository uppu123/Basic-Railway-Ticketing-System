import tkinter as tk
from tkinter import simpledialog, messagebox
import re

trains = []
bookings = []
next_booking_id = 1
admin_password = "admin123"


def add_train(train_id, source, destination, departure_time, seats, price):
    train = {
        "train_id": train_id,
        "source": source,
        "destination": destination,
        "departure_time": departure_time,
        "seats": seats,
        "price": price
    }
    trains.append(train)


def book_ticket(train_id, passenger_name):
    global next_booking_id
    for train in trains:
        if train["train_id"] == train_id and train["seats"] > 0:
            seat_number = train["seats"]
            booking = {
                "booking_id": next_booking_id,
                "train_id": train_id,
                "passenger_name": passenger_name,
                "seat_number": seat_number,
                "price": train["price"]
            }
            bookings.append(booking)
            train["seats"] -= 1
            next_booking_id += 1
            return booking
    return None


def display_trains():
    train_list = "\n".join(
        f"Train ID: {train['train_id']}, Source: {train['source']}, Destination: {train['destination']}, Departure Time: {train['departure_time']}, Available Seats: {train['seats']}, Price: ${train['price']}"
        for train in trains
    )
    return train_list


def display_bookings():
    booking_list = "\n".join(
        f"Booking ID: {booking['booking_id']}, Train ID: {booking['train_id']}, Passenger Name: {booking['passenger_name']}, Seat Number: {booking['seat_number']}, Price: ${booking['price']}"
        for booking in bookings
    )
    return booking_list


def is_valid_train_id(train_id):
    return re.match(r'^[A-Za-z0-9]+$', train_id)


def is_valid_passenger_name(name):
    return re.match(r'^[A-Za-z\s]+$', name)


class RailwaySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Railway Booking System")

        add_train("101", "Delhi", "Patna", "09:00 AM", 100, 150.0)
        add_train("102", "Mumbai", "Indore", "01:00 PM", 120, 200.0)
        window_width = 600
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        self.main_menu()

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text="Railway System Menu")
        label.place(relx=0.5, rely=0.1, anchor="center")

        user_menu_button = tk.Button(self.root, text="User Menu", command=self.user_menu)
        user_menu_button.place(relx=0.5, rely=0.3, anchor="center")

        admin_menu_button = tk.Button(self.root, text="Admin Login", command=self.admin_login)
        admin_menu_button.place(relx=0.5, rely=0.4, anchor="center")

        exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        exit_button.place(relx=0.5, rely=0.5, anchor="center")

    def user_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text="User Menu")
        label.place(relx=0.5, rely=0.1, anchor="center")

        view_trains_button = tk.Button(self.root, text="View Trains", command=self.view_trains)
        view_trains_button.place(relx=0.5, rely=0.3, anchor="center")

        book_ticket_button = tk.Button(self.root, text="Book Ticket", command=self.book_ticket)
        book_ticket_button.place(relx=0.5, rely=0.4, anchor="center")

        back_button = tk.Button(self.root, text="Back", command=self.main_menu)
        back_button.place(relx=0.5, rely=0.5, anchor="center")

    def view_trains(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text="Available Trains")
        label.place(relx=0.5, rely=0.1, anchor="center")

        train_list = display_trains()
        train_label = tk.Label(self.root, text=train_list)
        train_label.place(relx=0.5, rely=0.4, anchor="center")

        back_button = tk.Button(self.root, text="Back", command=self.user_menu)
        back_button.place(relx=0.5, rely=0.8, anchor="center")

    def book_ticket(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enter Train ID:").place(relx=0.3, rely=0.2, anchor="e")
        train_id_entry = tk.Entry(self.root)
        train_id_entry.place(relx=0.6, rely=0.2, anchor="w")

        tk.Label(self.root, text="Enter Passenger Name:").place(relx=0.3, rely=0.3, anchor="e")
        passenger_name_entry = tk.Entry(self.root)
        passenger_name_entry.place(relx=0.6, rely=0.3, anchor="w")

        def book():
            train_id = train_id_entry.get()
            passenger_name = passenger_name_entry.get()
            if not is_valid_passenger_name(passenger_name):
                messagebox.showerror("Error", "Invalid passenger name. Please enter alphabets and spaces only.")
                return

            selected_train = next((train for train in trains if train["train_id"] == train_id), None)
            if not selected_train:
                messagebox.showerror("Error", "Train not found.")
                return

            if selected_train["seats"] <= 0:
                messagebox.showerror("Error", "No available seats.")
                return

            payment_successful = self.show_payment_window(selected_train["price"])
            if payment_successful:
                booking = book_ticket(train_id, passenger_name)
                if booking:
                    messagebox.showinfo("Success",
                                        f"Ticket booked successfully! Booking ID: {booking['booking_id']}, Seat Number: {booking['seat_number']}")
                else:
                    messagebox.showerror("Error", "Failed to book ticket. Please try again.")
            else:
                messagebox.showerror("Error", "Payment failed. Please try again.")

        book_button = tk.Button(self.root, text="Book Ticket", command=book)
        book_button.place(relx=0.4, rely=0.5, anchor="center")

        back_button = tk.Button(self.root, text="Back", command=self.user_menu)
        back_button.place(relx=0.6, rely=0.5, anchor="center")

    def show_payment_window(self, price):
        payment_window = tk.Toplevel(self.root)
        payment_window.title("Payment")
        payment_window.geometry("300x200")

        tk.Label(payment_window, text=f"Ticket Price: ${price}").place(relx=0.5, rely=0.2, anchor="center")
        tk.Label(payment_window, text="Enter Payment Amount:").place(relx=0.5, rely=0.4, anchor="center")
        amount_entry = tk.Entry(payment_window)
        amount_entry.place(relx=0.5, rely=0.5, anchor="center")

        def process_payment():
            amount = amount_entry.get()
            if amount.isdigit() and float(amount) >= price:
                messagebox.showinfo("Success", "Payment successful!")
                payment_window.destroy()
                return True
            else:
                messagebox.showerror("Error", "Insufficient amount. Please enter the correct amount.")
                return False

        pay_button = tk.Button(payment_window, text="Pay", command=lambda: process_payment())
        pay_button.place(relx=0.5, rely=0.7, anchor="center")

        self.root.wait_window(payment_window)

        return True

    def admin_login(self):
        password = simpledialog.askstring("Admin Login", "Enter password:", show='*')
        if password == admin_password:
            self.admin_menu()
        else:
            messagebox.showerror("Error", "Incorrect password. Access denied.")

    def admin_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text="Admin Menu")
        label.place(relx=0.5, rely=0.1, anchor="center")

        add_train_button = tk.Button(self.root, text="Add Train", command=self.add_train)
        add_train_button.place(relx=0.5, rely=0.3, anchor="center")

        display_trains_button = tk.Button(self.root, text="Display Trains", command=self.display_trains_admin)
        display_trains_button.place(relx=0.5, rely=0.4, anchor="center")

        display_bookings_button = tk.Button(self.root, text="Display Bookings", command=self.display_bookings_admin)
        display_bookings_button.place(relx=0.5, rely=0.5, anchor="center")

        back_button = tk.Button(self.root, text="Back", command=self.main_menu)
        back_button.place(relx=0.5, rely=0.6, anchor="center")

    def add_train(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enter Train ID:").place(relx=0.3, rely=0.2, anchor="e")
        train_id_entry = tk.Entry(self.root)
        train_id_entry.place(relx=0.6, rely=0.2, anchor="w")

        tk.Label(self.root, text="Enter Source:").place(relx=0.3, rely=0.3, anchor="e")
        source_entry = tk.Entry(self.root)
        source_entry.place(relx=0.6, rely=0.3, anchor="w")

        tk.Label(self.root, text="Enter Destination:").place(relx=0.3, rely=0.4, anchor="e")
        destination_entry = tk.Entry(self.root)
        destination_entry.place(relx=0.6, rely=0.4, anchor="w")

        tk.Label(self.root, text="Enter Departure Time:").place(relx=0.3, rely=0.5, anchor="e")
        departure_time_entry = tk.Entry(self.root)
        departure_time_entry.place(relx=0.6, rely=0.5, anchor="w")

        tk.Label(self.root, text="Enter Number of Seats:").place(relx=0.3, rely=0.6, anchor="e")
        seats_entry = tk.Entry(self.root)
        seats_entry.place(relx=0.6, rely=0.6, anchor="w")

        tk.Label(self.root, text="Enter Price:").place(relx=0.3, rely=0.7, anchor="e")
        price_entry = tk.Entry(self.root)
        price_entry.place(relx=0.6, rely=0.7, anchor="w")

        def add():
            train_id = train_id_entry.get()
            if not is_valid_train_id(train_id):
                messagebox.showerror("Error", "Invalid Train ID. Please enter alphanumeric characters only.")
                return
            source = source_entry.get()
            destination = destination_entry.get()
            departure_time = departure_time_entry.get()
            seats = seats_entry.get()
            price = price_entry.get()
            if not seats.isdigit() or not price.replace('.', '', 1).isdigit():
                messagebox.showerror("Error", "Invalid number of seats or price. Please enter valid numbers.")
                return
            add_train(train_id, source, destination, departure_time, int(seats), float(price))
            messagebox.showinfo("Success", "Train added successfully!")

        add_train_button = tk.Button(self.root, text="Add Train", command=add)
        add_train_button.place(relx=0.4, rely=0.8, anchor="center")

        back_button = tk.Button(self.root, text="Back", command=self.admin_menu)
        back_button.place(relx=0.6, rely=0.8, anchor="center")

    def display_trains_admin(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text="Available Trains")
        label.place(relx=0.5, rely=0.1, anchor="center")

        train_list = display_trains()
        train_label = tk.Label(self.root, text=train_list)
        train_label.place(relx=0.5, rely=0.4, anchor="center")

        back_button = tk.Button(self.root, text="Back", command=self.admin_menu)
        back_button.place(relx=0.5, rely=0.8, anchor="center")

    def display_bookings_admin(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text="Bookings")
        label.place(relx=0.5, rely=0.1, anchor="center")

        booking_list = display_bookings()
        booking_label = tk.Label(self.root, text=booking_list)
        booking_label.place(relx=0.5, rely=0.4, anchor="center")

        back_button = tk.Button(self.root, text="Back", command=self.admin_menu)
        back_button.place(relx=0.5, rely=0.8, anchor="center")


if __name__ == "__main__":
    root = tk.Tk()
    app = RailwaySystem(root)
    root.mainloop()

