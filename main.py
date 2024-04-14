import psycopg2
from getpass import getpass
from datetime import datetime, timedelta

def connect_to_db():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="project",
            user="postgres",
            password="Programmer19!")
        return connection
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

def register_user():
    email = input("Enter email: ")
    password = getpass("Enter password: ")  # getpass hides the input for privacy
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    role = input("Register as (1) Member, (2) Trainer, (3) Admin: ") # Enter 1, 2 or 3 for respective roles

    # Connect to the database
    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        
        try:
            if role == "1":  # Member registration
                cur.execute("INSERT INTO Members (FirstName, LastName, Email, Password) VALUES (%s, %s, %s, %s)",
                            (first_name, last_name, email, password))
            elif role == "2":  # Trainer registration
                cur.execute("INSERT INTO Trainers (FirstName, LastName, Email, Password) VALUES (%s, %s, %s, %s)",
                            (first_name, last_name, email, password))
            elif role == "3":  # Admin registration
                cur.execute("INSERT INTO Admins (FirstName, LastName, Email, Password) VALUES (%s, %s, %s, %s)",
                            (first_name, last_name, email, password))
            else:
                print("Invalid role selection.")
                return
            
            conn.commit()  # Commit the transaction
            print("Registration successful.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to register:", error)
            conn.rollback()  # Roll back the transaction on error
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def login():
    email = input("Enter email: ")
    password = getpass("Enter password: ")  # Hides the input for privacy

    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        
        try:
            # Attempt to fetch user role and ID based on email and password
            cur.execute("""
                SELECT 'Member', MemberID FROM Members WHERE Email = %s AND Password = %s
                UNION ALL
                SELECT 'Trainer', TrainerID FROM Trainers WHERE Email = %s AND Password = %s
                UNION ALL
                SELECT 'Admin', AdminID FROM Admins WHERE Email = %s AND Password = %s
                """, (email, password, email, password, email, password))
            result = cur.fetchone()

            if result:
                role, user_id = result
                print(f"Login successful. Welcome, {role}!")
                
                # Redirect based on role
                if role == 'Member':
                    member_menu(user_id)
                elif role == 'Trainer':
                    trainer_menu(user_id)
                    pass
                elif role == 'Admin':
                    admin_menu(user_id)
                    pass
            else:
                print("Login failed. Please check your email and password.")
                
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to login:", error)
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def manage_profile(member_id):
    print("\nProfile Management")
    print("1. Update Email")
    print("2. Update Password")
    print("3. Update Current Weight")
    print("4. Update Weight Goal")
    print("5. Return to Main Menu")

    choice = input("What would you like to update? ")
    new_value = None
    field = None

    if choice == "1":
        new_value = input("Enter new email: ")
        field = 'Email'
    elif choice == "2":
        new_value = getpass("Enter new password: ")  # Use getpass to hide the password input
        field = 'Password'
    elif choice == "3":
        new_value = input("Enter new current weight: ")
        field = 'CurrentWeight'
    elif choice == "4":
        new_value = input("Enter new weight goal: ")
        field = 'WeightGoal'
    elif choice == "5":
        return
    else:
        print("Invalid selection. Please try again.")
        return

    # Ensure the new_value is not None and a field has been selected
    if new_value and field:
        # Connect to the database
        conn = connect_to_db()
        if conn is not None:
            cur = conn.cursor()

            try:
                # Prepare the SQL UPDATE statement dynamically based on the user's choice
                sql_update_query = f"UPDATE Members SET {field} = %s WHERE MemberID = %s"
                cur.execute(sql_update_query, (new_value, member_id))

                conn.commit()  # Commit the transaction
                print(f"{field} updated successfully.")
            except (Exception, psycopg2.DatabaseError) as error:
                print("Failed to update profile:", error)
                conn.rollback()  # Roll back the transaction on error
            finally:
                cur.close()
                conn.close()
        else:
            print("Failed to connect to the database.")


def view_dashboard(member_id):
    print("Dashboard Display")

    exercise_routines = [
        "Cardio Circuit: 30 mins treadmill, 15 mins stationary bike, 15 mins rowing machine",
        "Strength Training: Chest and Back - Bench press, Lat pulldowns, Pushups",
        "Leg Day: Squats, Leg Press, Deadlifts, Lunges"
    ]

    fitness_achievements = [
        "Completed first half-marathon",
        "Achieved new personal best in deadlift: 200 lbs",
        "Consistently worked out 5 days a week for a month"
    ]

    health_statistics = [
        "Current Weight: 160 lbs",
        "Weight Goal: 150 lbs",
        "Resting Heart Rate: 60 bpm"
    ]

    # Displaying the information
    print("\nExercise Routines:")
    for routine in exercise_routines:
        print(f"- {routine}")
    
    print("\nFitness Achievements:")
    for achievement in fitness_achievements:
        print(f"- {achievement}")
    
    print("\nHealth Statistics:")
    for statistic in health_statistics:
        print(f"- {statistic}")

def display_current_sessions(member_id):
    print("\nYour Upcoming Personal Training Sessions:")
    
    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            # Fetch future sessions for the member
            cur.execute("""
                SELECT pts.SessionID, pts.SessionTime, t.FirstName || ' ' || t.LastName as TrainerName, pts.Status
                FROM PersonalTrainingSessions pts
                JOIN Trainers t ON pts.TrainerID = t.TrainerID
                WHERE pts.MemberID = %s AND pts.SessionTime > CURRENT_TIMESTAMP
                AND pts.Status = 'Scheduled'
                ORDER BY pts.SessionTime ASC
            """, (member_id,))
            
            sessions = cur.fetchall()
            if sessions:
                for session in sessions:
                    print(f"Session ID: {session[0]}, Time: {session[1]}, Trainer: {session[2]}, Status: {session[3]}")
            else:
                print("You have no upcoming personal training sessions.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Failed to query personal training sessions: {error}")
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def display_current_classes(member_id):
    print("\nYour Registered Group Fitness Classes:")
    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT c.ClassID, c.ClassName, c.ClassTime, t.FirstName || ' ' || t.LastName as TrainerName
                FROM Classes c
                JOIN ClassRegistrations r ON c.ClassID = r.ClassID
                JOIN Trainers t ON c.TrainerID = t.TrainerID
                WHERE r.MemberID = %s AND c.ClassTime > CURRENT_TIMESTAMP
                ORDER BY c.ClassTime ASC
            """, (member_id,))
            
            classes = cur.fetchall()
            if classes:
                for class_info in classes:
                    print(f"Class ID: {class_info[0]}, Name: {class_info[1]}, Trainer: {class_info[3]}, Time: {class_info[2]}")
            else:
                print("You are not registered for any upcoming group fitness classes.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to query registered group fitness classes:", error)
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def list_trainers():
    print("\nAvailable Trainers:")
    
    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute("SELECT TrainerID, FirstName, LastName FROM Trainers ORDER BY TrainerID")
            trainers = cur.fetchall()

            if trainers:
                for trainer in trainers:
                    print(f"Trainer ID: {trainer[0]}, Name: {trainer[1]} {trainer[2]}")
            else:
                print("No trainers available.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to list trainers:", error)
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def list_classes():
    print("\nAvailable Classes:")

    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT c.ClassID, c.ClassName, c.ClassTime, t.FirstName || ' ' || t.LastName AS TrainerName
                FROM Classes c
                JOIN Trainers t ON c.TrainerID = t.TrainerID
                WHERE c.ClassTime > CURRENT_TIMESTAMP
                ORDER BY c.ClassTime ASC
            """)
            classes = cur.fetchall()

            if classes:
                for class_info in classes:
                    print(f"Class ID: {class_info[0]}, Name: {class_info[1]}, Trainer: {class_info[3]}, Time: {class_info[2]}")
            else:
                print("No classes available.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to list classes:", error)
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def process_payment(member_id, amount, service_type):
    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO Payments (MemberID, Amount, PaymentDate, ServiceType)
                VALUES (%s, %s, CURRENT_TIMESTAMP, %s)
            """, (member_id, amount, service_type))
            conn.commit()
            print("Payment processed successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to process payment:", error)
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def schedule_personal_training(member_id):
    print("\nSchedule Personal Training Session")

    # Display trainers
    list_trainers()

    trainer_id = input("Enter Trainer ID: ")
    session_date = input("Enter session date (YYYY-MM-DD): ")
    session_time = input("Enter session time (HH:MM): ")
    session_datetime = datetime.strptime(f"{session_date} {session_time}", "%Y-%m-%d %H:%M")

    # Connect to the database
    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            # Assuming the duration of a training session is fixed (e.g., 1 hour)
            session_endtime = session_datetime + timedelta(hours=1)

            # Check trainer's availability
            cur.execute("""
                SELECT COUNT(*) FROM TrainerAvailability
                WHERE TrainerID = %s
                AND StartTime <= %s
                AND EndTime >= %s
            """, (trainer_id, session_datetime, session_endtime))

            if cur.fetchone()[0] == 0:
                print("Trainer is not available at this time.")
                return

            # Check for existing bookings
            cur.execute("""
                SELECT COUNT(*) FROM PersonalTrainingSessions
                WHERE TrainerID = %s
                AND SessionTime >= %s
                AND SessionTime < %s
            """, (trainer_id, session_datetime, session_endtime))

            if cur.fetchone()[0] > 0:
                print("Trainer already has a session booked at this time.")
                return

            # Schedule the session
            cur.execute("""
                INSERT INTO PersonalTrainingSessions (MemberID, TrainerID, SessionTime, Status)
                VALUES (%s, %s, %s, 'Scheduled')
            """, (member_id, trainer_id, session_datetime))

            conn.commit()
            process_payment(member_id, amount=100, service_type="Personal Training Session")
            print("Personal training session scheduled successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to schedule personal training session:", error)
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def register_for_class(member_id):
    print("\nRegister for Group Fitness Class")

    # Display classes
    list_classes()

    class_id = input("Enter Class ID to register: ")

    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            # Check if already registered
            cur.execute("""
                SELECT COUNT(*) FROM ClassRegistrations
                WHERE MemberID = %s AND ClassID = %s
            """, (member_id, class_id))

            if cur.fetchone()[0] > 0:
                print("You are already registered for this class.")
                return

            # Register for the class
            cur.execute("""
                INSERT INTO ClassRegistrations (MemberID, ClassID)
                VALUES (%s, %s)
            """, (member_id, class_id))

            conn.commit()

            process_payment(member_id, amount=50, service_type="Class Registration")

            print("Registered for class successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to register for class:", error)
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def manage_schedule(member_id):
    print("\nSchedule Management")
    # Step 1: Display current personal training sessions and classes
    display_current_sessions(member_id)
    display_current_classes(member_id)

    # Step 2: Ask the member what they would like to do next
    choice = input("Do you want to (1) Go back, (2) Schedule a personal training session, or (3) Register for a group fitness class? ")

    if choice == "1":
        # Return to the previous menu or manage_profile
        return
    elif choice == "2":
        schedule_personal_training(member_id)
    elif choice == "3":
        register_for_class(member_id)
    else:
        print("Invalid choice. Please try again.")

def member_menu(member_id):
    while True:
        print("\nMember Menu")
        print("1. Manage Profile")
        print("2. View Dashboard")
        print("3. Manage Schedule")
        print("4. Log Out")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            manage_profile(member_id)
        elif choice == "2":
            view_dashboard(member_id)
        elif choice == "3":
            manage_schedule(member_id)
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def set_trainer_availability(trainer_id):
    print("\nSet Availability")
    start_date = input("Enter start date for availability (YYYY-MM-DD): ")
    start_time = input("Enter start time (HH:MM): ")
    end_date = input("Enter end date for availability (YYYY-MM-DD): ")
    end_time = input("Enter end time (HH:MM): ")
    
    start_datetime = f"{start_date} {start_time}:00"
    end_datetime = f"{end_date} {end_time}:00"

    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO TrainerAvailability (TrainerID, StartTime, EndTime) 
                VALUES (%s, %s, %s)
            """, (trainer_id, start_datetime, end_datetime))
            conn.commit()
            print("Availability set successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to set availability:", error)
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def view_member_profile():
    print("\nAvailable Members:")
    
    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute("SELECT FirstName, LastName FROM Members ORDER BY LastName, FirstName")
            members = cur.fetchall()
            for member in members:
                print(f"{member[0]} {member[1]}")

            # Ask for the member's name to search for more details
            print("\nEnter a member's full name to view their profile:")
            member_name = input("Full Name: ").strip()
            name_parts = member_name.split()

            if len(name_parts) >= 2:  # Assuming at least first name and last name provided
                first_name, last_name = name_parts[0], name_parts[-1]
                cur.execute("""
                    SELECT MemberID, FirstName, LastName, Email, CurrentWeight, WeightGoal 
                    FROM Members
                    WHERE FirstName ILIKE %s AND LastName ILIKE %s
                """, (first_name, last_name))
                member_details = cur.fetchall()

                if member_details:
                    for detail in member_details:
                        print(f"\nMemberID: {detail[0]}, Name: {detail[1]} {detail[2]}, Email: {detail[3]}, Current Weight: {detail[4]}, Weight Goal: {detail[5]}")
                else:
                    print("No member found with that name.")
            else:
                print("Please enter both the first and last name for accuracy.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to list members:", error)
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def trainer_menu(trainer_id):
    while True:
        print("\nTrainer Menu")
        print("1. Set Availability")
        print("2. View Member Profile")
        print("3. Log Out")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            set_trainer_availability(trainer_id)
        elif choice == "2":
            view_member_profile()
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def create_room_booking():
    room_id = input("Enter Room ID: ")
    booking_time = input("Enter Booking Time (YYYY-MM-DD HH:MM): ")
    booked_by = input("Enter Admin ID who is booking: ")
    purpose = input("Enter Purpose of Booking: ")

    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO RoomBookings (RoomID, BookingTime, BookedBy, Purpose)
                VALUES (%s, %s, %s, %s)
            """, (room_id, booking_time, booked_by, purpose))
            conn.commit()
            print("Room booking created successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to create room booking:", error)
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def view_room_bookings():
    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute("SELECT BookingID, RoomID, BookingTime, Purpose FROM RoomBookings ORDER BY BookingTime ASC")
            bookings = cur.fetchall()
            for booking in bookings:
                print(f"BookingID: {booking[0]}, RoomID: {booking[1]}, Time: {booking[2]}, Purpose: {booking[3]}")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to retrieve room bookings:", error)
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def update_room_booking():
    booking_id = input("Enter Booking ID to update: ")

    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            # Display current booking details
            cur.execute("SELECT BookingID, RoomID, BookingTime, Purpose FROM RoomBookings WHERE BookingID = %s", (booking_id,))
            booking = cur.fetchone()
            if booking:
                print(f"Current Booking - ID: {booking[0]}, RoomID: {booking[1]}, Time: {booking[2]}, Purpose: {booking[3]}")
                
                # Get new booking details from user
                new_room_id = input("Enter new Room ID (leave blank to keep current): ") or booking[1]
                new_booking_time = input("Enter new Booking Time (YYYY-MM-DD HH:MM) (leave blank to keep current): ") or booking[2]
                new_purpose = input("Enter new Purpose (leave blank to keep current): ") or booking[3]
                
                # Update booking
                cur.execute("""
                    UPDATE RoomBookings
                    SET RoomID = %s, BookingTime = %s, Purpose = %s
                    WHERE BookingID = %s
                """, (new_room_id, new_booking_time, new_purpose, booking_id))
                conn.commit()
                print("Room booking updated successfully.")
            else:
                print("No booking found with the provided ID.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to update room booking:", error)
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def delete_room_booking():
    booking_id = input("Enter Booking ID to delete: ")

    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            
            # Confirm deletion
            confirmation = input("Are you sure you want to delete this booking? (yes/no): ")
            if confirmation.lower() == "yes":
                cur.execute("DELETE FROM RoomBookings WHERE BookingID = %s", (booking_id,))
                conn.commit()
                print("Room booking deleted successfully.")
            else:
                print("Deletion cancelled.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to delete room booking:", error)
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def manage_room_bookings():
    while True:
        print("\nRoom Booking Management")
        print("1. Create Booking")
        print("2. View Bookings")
        print("3. Update Booking")
        print("4. Delete Booking")
        print("5. Return to Admin Menu")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            create_room_booking()
        elif choice == "2":
            view_room_bookings()
        elif choice == "3":
            update_room_booking()
        elif choice == "4":
            delete_room_booking()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def view_equipment_status():
    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute("SELECT EquipmentID, EquipmentName, MaintenanceSchedule, Status FROM Equipment ORDER BY EquipmentID")
            equipment_list = cur.fetchall()
            print("\nEquipment Maintenance Status:")
            for equipment in equipment_list:
                print(f"ID: {equipment[0]}, Name: {equipment[1]}, Maintenance Schedule: {equipment[2]}, Status: {equipment[3]}")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to retrieve equipment status:", error)
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def update_equipment_status():
    equipment_id = input("Enter Equipment ID to update: ")
    new_status = input("Enter new status (Available/Under Maintenance): ")
    new_schedule = input("Enter new maintenance schedule (YYYY-MM-DD): ")

    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE Equipment
                SET Status = %s, MaintenanceSchedule = %s
                WHERE EquipmentID = %s
            """, (new_status, new_schedule, equipment_id))
            conn.commit()
            print("Equipment status updated successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to update equipment status:", error)
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def monitor_equipment_maintenance():
    while True:
        print("\nEquipment Maintenance Monitoring")
        print("1. View Equipment Status")
        print("2. Update Equipment Status")
        print("3. Return to Admin Menu")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            view_equipment_status()
        elif choice == "2":
            update_equipment_status()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def add_new_class():
    class_name = input("Enter class name: ")
    trainer_id = input("Enter trainer ID: ")
    room_id = input("Enter room ID: ")
    class_time = input("Enter class time (YYYY-MM-DD HH:MM): ")

    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO Classes (ClassName, TrainerID, RoomID, ClassTime)
                VALUES (%s, %s, %s, %s)
            """, (class_name, trainer_id, room_id, class_time))
            conn.commit()
            print("New class added successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to add new class:", error)
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def update_existing_class():
    class_id = input("Enter the class ID to update: ")
    new_class_name = input("Enter new class name (leave blank to not change): ")
    new_trainer_id = input("Enter new trainer ID (leave blank to not change): ")
    new_room_id = input("Enter new room ID (leave blank to not change): ")
    new_class_time = input("Enter new class time (YYYY-MM-DD HH:MM) (leave blank to not change): ")

    # Build the SQL query dynamically based on which details are provided
    updates = []
    params = []
    if new_class_name:
        updates.append("ClassName = %s")
        params.append(new_class_name)
    if new_trainer_id:
        updates.append("TrainerID = %s")
        params.append(new_trainer_id)
    if new_room_id:
        updates.append("RoomID = %s")
        params.append(new_room_id)
    if new_class_time:
        updates.append("ClassTime = %s")
        params.append(new_class_time)

    if updates:
        conn = connect_to_db()
        if conn is not None:
            cur = conn.cursor()
            try:
                update_query = f"UPDATE Classes SET {', '.join(updates)} WHERE ClassID = %s"
                params.append(class_id)  # The class ID is always the last parameter
                cur.execute(update_query, tuple(params))
                conn.commit()
                print("Class updated successfully.")
            except (Exception, psycopg2.DatabaseError) as error:
                print("Failed to update class:", error)
                conn.rollback()
            finally:
                cur.close()
                conn.close()
        else:
            print("Failed to connect to the database.")
    else:
        print("No updates provided.")

def delete_class():
    class_id = input("Enter Class ID to delete: ")
    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Classes WHERE ClassID = %s", (class_id,))
            conn.commit()
            print("Class deleted successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to delete class:", error)
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def view_current_classes():
    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute("SELECT ClassID, ClassName, TrainerID, RoomID, ClassTime FROM Classes ORDER BY ClassTime")
            classes = cur.fetchall()
            print("\nCurrent Classes:")
            for class_info in classes:
                print(f"ClassID: {class_info[0]}, Name: {class_info[1]}, TrainerID: {class_info[2]}, RoomID: {class_info[3]}, Time: {class_info[4]}")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to retrieve classes:", error)
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def update_class_schedule():
    while True:
        print("\nClass Schedule Management")
        print("1. Add New Class")
        print("2. Update Existing Class")
        print("3. Delete Class")
        print("4. View Current Classes")
        print("5. Return to Admin Menu")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            add_new_class()
        elif choice == "2":
            update_existing_class()
        elif choice == "3":
            delete_class()
        elif choice == "4":
            view_current_classes()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def process_billing_and_payments():
    print("\nProcessed Payments:")
    
    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute("SELECT PaymentID, MemberID, Amount, PaymentDate, ServiceType FROM Payments ORDER BY PaymentDate DESC")
            payments = cur.fetchall()
            for payment in payments:
                print(f"PaymentID: {payment[0]}, MemberID: {payment[1]}, Amount: {payment[2]}, Date: {payment[3]}, Type: {payment[4]}")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to retrieve payments:", error)
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def admin_menu():
    while True:
        print("\nAdmin Menu")
        print("1. Room Booking Management")
        print("2. Equipment Maintenance Monitoring")
        print("3. Class Schedule Updating")
        print("4. Billing and Payment Processing")
        print("5. Log Out")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            manage_room_bookings()
        elif choice == "2":
            monitor_equipment_maintenance()
        elif choice == "3":
            update_class_schedule()
        elif choice == "4":
            process_billing_and_payments()
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")



def main_menu():
    while True:
        print("\nHealth and Fitness Club Management System")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            register_user()
        elif choice == "2":
            login()
            pass
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
