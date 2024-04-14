Ryan Zhang
101264124

COMP 3005 Project 2

Prerequisites
Python 3.8 or higher
PostgreSQL 12 or higher
psycopg2 library

Setup
Clone the repository:

cd into project

Database Configuration

Create a PostgreSQL database for the project.
Run the SQL scripts found in the SQL directory to set up the database schema and populate it with initial data.
Update the database connection settings in connect_to_db() in main.py

Usage
Run the application from the command line:

python main.py


Features

Member Functions

User Registration: Members can register by providing personal information and setting initial fitness goals.
Profile Management: Members can update their profiles, including personal information, fitness goals, and health metrics.
Dashboard Display: Displays exercise routines, fitness achievements, and health statistics.
Schedule Management: Members can book, reschedule, or cancel personal training sessions and group fitness classes.

Trainer Functions

Schedule Management: Trainers can set their availability times.
Member Profile Viewing: Trainers can view details of club members.

Administrative Functions

Room Booking Management: Admins can manage bookings for rooms within the facility.
Equipment Maintenance Monitoring: Admins can track and update the status of equipment maintenance.
Class Schedule Updating: Admins can modify the schedule for group fitness classes.
Billing and Payment Processing: Admins can oversee and process payments for services offered.

Bonus Features

The following features were implemented to enhance the standard functionalities, potentially qualifying for extra marks:

Ensured trainers are not double-booked and respects their available hours.
Includes password hashing and session management for enhanced security.
Hides password while typing for enhanced security.
Registering for classes/personal training automatically sends a payment.
When looking for the list of classes, it will hide the classes that occurred in the past.


Demo Video Link:

https://youtu.be/hTSKK7VPtUM
