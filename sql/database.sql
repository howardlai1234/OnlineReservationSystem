DROP TABLE User;
DROP Table Meeting;
DROP TABLE UserAvailability;
DROP Table message;

CREATE TABLE User (
	userID int NOT NULL AUTO_INCREMENT,
    username varchar(255),
	firstName varchar(255),
	lastName varchar(255),
	email varchar(255),
	tel varchar(255),
	typeID varchar(255),
	active Boolean,
	hashPW varchar(255),
	PRIMARY KEY (userID)
);

CREATE TABLE Meeting (
	meetingID int NOT NULL AUTO_INCREMENT,
	hostID int NOT NULL,
	participantID int NOT NULL,
	date Date,
	name varchar(255),
	remark varchar(255),
	statusID int,
	PRIMARY KEY (meetingID)
);

CREATE TABLE UserAvailability (
	userID int NOT NULL,
    date Date NOT NULL,
    slotID int NOT NULL
);

CREATE TABLE Message (
	messageID int NOT NULL AUTO_INCREMENT,
    senderID int NOT NULL,
    receiverID int NOT NULL,
    referenceID int,
    sendTime datetime,
    viewed bool,
    title varchar(255),
    body varchar(4096),
    PRIMARY KEY (messageID)
);

INSERT INTO User (username, firstname, lastname, email, tel, typeID, active, hashPW) value
('admin','ad', 'min', 'admin@gmail.com', 12345678, 0, TRUE, 'admin')
