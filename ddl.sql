-- Members Table
CREATE TABLE Members (
    MemberID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    Password VARCHAR(100),
    WeightGoal INT,
    CurrentWeight INT
);

-- Trainers Table
CREATE TABLE Trainers (
    TrainerID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    Password VARCHAR(100)
);


-- Admins Table
CREATE TABLE Admins (
    AdminID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    Password VARCHAR(100)
);

CREATE TABLE TrainerAvailability (
    AvailabilityID SERIAL PRIMARY KEY,
    TrainerID INT REFERENCES Trainers(TrainerID),
    StartTime TIMESTAMP,
    EndTime TIMESTAMP,
    UNIQUE (TrainerID, StartTime, EndTime)
);

-- Classes Table
CREATE TABLE Classes (
    ClassID SERIAL PRIMARY KEY,
    ClassName VARCHAR(100),
    TrainerID INT REFERENCES Trainers(TrainerID),
    RoomID INT,
    ClassTime TIMESTAMP
);

CREATE TABLE ClassRegistrations (
    RegistrationID SERIAL PRIMARY KEY,
    ClassID INT REFERENCES Classes(ClassID),
    MemberID INT REFERENCES Members(MemberID),
    UNIQUE (ClassID, MemberID) -- Prevents the same member from registering for the same class multiple times
);

-- Personal Training Sessions Table
CREATE TABLE PersonalTrainingSessions (
    SessionID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    TrainerID INT REFERENCES Trainers(TrainerID),
    SessionTime TIMESTAMP,
    Status VARCHAR(50) -- e.g., Scheduled, Completed, Cancelled
);

-- Room Bookings Table
CREATE TABLE RoomBookings (
    BookingID SERIAL PRIMARY KEY,
    RoomID INT,
    BookingTime TIMESTAMP,
    BookedBy INT REFERENCES Admins(AdminID),
    Purpose VARCHAR(100)
);

-- Equipment Table
CREATE TABLE Equipment (
    EquipmentID SERIAL PRIMARY KEY,
    EquipmentName VARCHAR(100),
    MaintenanceSchedule DATE,
    Status VARCHAR(50) -- e.g., Available, Under Maintenance
);

-- Payments Table
CREATE TABLE Payments (
    PaymentID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    Amount DECIMAL(10, 2),
    PaymentDate TIMESTAMP,
    ServiceType VARCHAR(100) -- e.g., Membership Fee, Personal Training Session
);
