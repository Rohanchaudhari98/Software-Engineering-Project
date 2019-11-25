CREATE TABLE User
(
  RollNo VARCHAR(20) NOT NULL,
  Accounttype VARCHAR(20) NOT NULL,
  Name VARCHAR(25)  NOT NULL,
  Surname VARCHAR(25)  NOT NULL,
  MemberCount VARCHAR(25) NOT NULL,
  Email VARCHAR(20) NOT NULL,			
  Password VARCHAR(20) NOT NULL,
  Address VARCHAR(100) NOT NULL,
  Phone VARCHAR(20) NOT NULL,
  Pincode VARCHAR(20) NOT NULL,
  PRIMARY KEY (RollNo)
);

CREATE TABLE Request
(
	RequestID VARCHAR(20) NOT NULL,
  RollNo VARCHAR(20) NOT NULL,
	Type VARCHAR(50) NOT NULL,
	Description VARCHAR(150) NOT NULL,
	Document BLOB,   -- for storing files    
	Project BLOB,
	Status VARCHAR(50) NOT NULL,
	TimeDate Datetime,	
	PRIMARY KEY (RequestID)

);

CREATE TABLE Complaint
(
  ComplainID VARCHAR(20) NOT NULL,
  RollNo VARCHAR(20) NOT NULL,
  Subject VARCHAR(50) NOT NULL,
  Description VARCHAR(150) NOT NULL,
  TimeDate Datetime,  
  PRIMARY KEY (ComplainID)

);
/*
CREATE TABLE Mess
(
  MessID INT NOT NULL,
  MessPassword VARCHAR(20) NOT NULL,
  MessCoordinator VARCHAR(25) NOT NULL,
  MessName VARCHAR(10) NOT NULL,
  PerDayRate INT NOT NULL,
  PRIMARY KEY (MessID)
);

CREATE TABLE MessCut
(
  FromDate DATE NOT NULL,
  ToDate DATE NOT NULL,
  RollNo VARCHAR(20) NOT NULL,
  MessID INT NOT NULL,
  PRIMARY KEY (FromDate, RollNo, MessID),
  FOREIGN KEY (RollNo) REFERENCES Members(RollNo),
  FOREIGN KEY (MessID) REFERENCES Mess(MessID)
);

CREATE TABLE Rating
(
  RatingValue INT NOT NULL,
  RollNo VARCHAR(20) NOT NULL,
  MessID INT NOT NULL,
  PRIMARY KEY (RollNo, MessID),
  FOREIGN KEY (RollNo) REFERENCES Members(RollNo),
  FOREIGN KEY (MessID) REFERENCES Mess(MessID)
);

CREATE TABLE MessJoins
(
  StartDate DATE NOT NULL,
  RollNo VARCHAR(20) NOT NULL,
  MessID INT NOT NULL,
  PRIMARY KEY (StartDate, RollNo, MessID),
  FOREIGN KEY (RollNo) REFERENCES Members(RollNo),
  FOREIGN KEY (MessID) REFERENCES Mess(MessID)
);

CREATE TABLE Forum
(
  DateTime DATETIME NOT NULL,
  Comment VARCHAR(100) NOT NULL,
  RollNo VARCHAR(20) NOT NULL,
  MessID INT NOT NULL,
  PRIMARY KEY (DateTime, RollNo, MessID),
  FOREIGN KEY (RollNo) REFERENCES Members(RollNo),
  FOREIGN KEY (MessID) REFERENCES Mess(MessID)
);

CREATE TABLE Extras
(
  ExtrasID INT NOT NULL,
  ExtrasName VARCHAR(20) NOT NULL,
  Price INT NOT NULL,
  PRIMARY KEY (ExtrasID)
);

CREATE TABLE ExtrasTaken
(
  DateTime DATETIME NOT NULL,
  RollNo VARCHAR(20) NOT NULL,
  ExtrasID INT NOT NULL,
  PRIMARY KEY (DateTime, RollNo, ExtrasID),
  FOREIGN KEY (RollNo) REFERENCES Members(RollNo),
  FOREIGN KEY (ExtrasID) REFERENCES Extras(ExtrasID)
);
*/