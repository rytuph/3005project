INSERT INTO Members (FirstName, LastName, Email, Password, WeightGoal, CurrentWeight) VALUES
('Ryan', 'Zhang', 'ryanzhang6@cmail.carleton.ca', 'password123', 180, 190),
('Connor', 'McDavid', 'connor@gmail.com', 'password123', 140, 150);

INSERT INTO Trainers (FirstName, LastName, Email, Password) VALUES
('Erik', 'Karlsson', 'erik@gmail.com', 'password123'),
('Cale', 'Makar', 'calemakar@gmail.com', 'password123');

INSERT INTO Admins (FirstName, LastName, Email, Password) VALUES
('Steve', 'Yzerman', 'steve@gmail.com', 'password123'),
('Joe', 'Sakic', 'joesakic@gmail.com', 'password123');

INSERT INTO TrainerAvailability (TrainerID, StartTime, EndTime) VALUES
(1, '2024-04-10 08:00:00', '2024-04-10 12:00:00'),
(2, '2024-04-10 14:00:00', '2024-04-10 18:00:00');

INSERT INTO Classes (ClassName, TrainerID, RoomID, ClassTime) VALUES
('Yoga', 1, 101, '2024-04-11 09:00:00'),
('Hiit', 2, 102, '2024-04-11 11:00:00');

INSERT INTO ClassRegistrations (ClassID, MemberID) VALUES
(1, 1),
(2, 2);

INSERT INTO PersonalTrainingSessions (MemberID, TrainerID, SessionTime, Status) VALUES
(1, 2, '2024-04-12 09:00:00', 'Scheduled'),
(2, 1, '2024-04-12 10:00:00', 'Scheduled');

INSERT INTO RoomBookings (RoomID, BookingTime, BookedBy, Purpose) VALUES
(201, '2024-04-10 08:00:00', 1, 'Personal Training'),
(202, '2024-04-11 09:00:00', 2, 'Yoga Class');

INSERT INTO Equipment (EquipmentName, MaintenanceSchedule, Status) VALUES
('Treadmill', '2024-05-01', 'Available'),
('Stationary Bike', '2024-05-15', 'Under Maintenance');

INSERT INTO Payments (MemberID, Amount, PaymentDate, ServiceType) VALUES
(1, 29.99, '2024-04-01 08:00:00', 'Membership Fee'),
(2, 49.99, '2024-04-01 08:15:00', 'Personal Training Session');

CREATE INDEX idx_member_email ON Members(Email);
CREATE INDEX idx_trainer_email ON Trainers(Email);
CREATE INDEX idx_admin_email ON Admins(Email);
