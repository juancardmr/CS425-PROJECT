
-- STRONG ENTITIES

CREATE TABLE Customer (
	emailAddress VARCHAR(50),
	firstName VARCHAR(20),
	middleName VARCHAR(20),
	lastName VARCHAR(20),
	password VARCHAR(50),
	PRIMARY KEY(emailAddress));
	
CREATE TABLE Connection (
	connectionID VARCHAR(20),
	maxConnections INT,
	maxTime TIME,
	maxPrice NUMERIC(10,3),
	PRIMARY KEY(connectionID));
	
CREATE TABLE Airport (
	IATA VARCHAR(10),
	name VARCHAR(50),
	country VARCHAR(20),
	state VARCHAR(20),
	PRIMARY KEY(IATA));
	
CREATE TABLE Airline (
	airlineCode VARCHAR(20),
	name VARCHAR(50),
	country VARCHAR(20),
	PRIMARY KEY(airlineCode));
	
CREATE TABLE Booking (
	bookingID VARCHAR(20),
	seatType VARCHAR(20),
	PRIMARY KEY(bookingID));

	
-- WEAK ENTITIES

CREATE TABLE Flight (
	flightNumber VARCHAR(50),
	flightDate DATE,
	firstClassPrice NUMERIC(10,3),
	economyPrice NUMERIC(10,3),
	PRIMARY KEY(airlineCode, flightNumber, flightDate),
	FOREIGN KEY(airlineCode) REFERENCES Airline);
	
-- MULTIVALUED ATTRIBUTES

CREATE TABLE CustomerAddress(
	emailAddress VARCHAR(50),
	line1 VARCHAR(50),
	line2 VARCHAR(50),
	city VARCHAR(20),
	zipCode INT,
	state VARCHAR(20),
	country VARCHAR(20),
	PRIMARY KEY(emailAddress, line1, line2, city, zipCode, state, country));
	
CREATE TABLE CustomerCard (
	emailAddress VARCHAR(50),
	cardNumber INT,
	cardName VARCHAR(50),
	PRIMARY KEY(emailAddress, cardNumber, cardName));
	
-- FINAL DATABASE

CREATE TABLE Customer (
	emailAddress VARCHAR(50),
	firstName VARCHAR(20),
	middleName VARCHAR(20),
	lastName VARCHAR(20),
	password VARCHAR(50),
	IATA VARCHAR(10),
	PRIMARY KEY(emailAddress));
	
CREATE TABLE Connection (
	connectionID VARCHAR(20),
	maxConnections INT,
	maxTime TIME,
	maxPrice NUMERIC(10,3),
	emailAddress VARCHAR(50),
	PRIMARY KEY(connectionID));
	
CREATE TABLE Airport (
	IATA VARCHAR(10),
	name VARCHAR(50),
	country VARCHAR(20),
	state VARCHAR(20),
	PRIMARY KEY(IATA));
	
CREATE TABLE Airline (
	airlineCode VARCHAR(20),
	name VARCHAR(50),
	country VARCHAR(20),
	PRIMARY KEY(airlineCode));
	
CREATE TABLE Booking (
	bookingID VARCHAR(20),
	seatType VARCHAR(20),
	emailAddress VARCHAR(50),
	PRIMARY KEY(bookingID));


CREATE TABLE Flight (
	airlineCode VARCHAR(20),
	flightNumber VARCHAR(50),
	flightDate DATE,
	firstClassPrice VARCHAR(10),
	economyPrice VARCHAR(10),
	connectionID VARCHAR(20),
	PRIMARY KEY(airlineCode, flightNumber, flightDate),
	FOREIGN KEY(airlineCode) REFERENCES Airline);
	

CREATE TABLE CustomerAddress(
	emailAddress VARCHAR(50),
	line1 VARCHAR(50),
	line2 VARCHAR(50),
	city VARCHAR(20),
	zipCode INT,
	state VARCHAR(20),
	country VARCHAR(20),
	PRIMARY KEY(emailAddress, line1, line2, city, zipCode, state, country));
	
CREATE TABLE CustomerCard (
	emailAddress VARCHAR(50),
	cardNumber INT,
	cardName VARCHAR(50),
	PRIMARY KEY(emailAddress, cardNumber, cardName));


CREATE TABLE Departure(
	IATA VARCHAR(10),
	flightNumber VARCHAR(50),
	flightDate DATE,
	departureTime DATETIME,
	PRIMARY KEY(IATA, flightNumber, flightDate));
	
CREATE TABLE Arrival(
	IATA VARCHAR(10),
	flightNumber VARCHAR(50),
	flightDate DATE,
	arrivalTime DATETIME,
	PRIMARY KEY(IATA, flightNumber, flightDate));





