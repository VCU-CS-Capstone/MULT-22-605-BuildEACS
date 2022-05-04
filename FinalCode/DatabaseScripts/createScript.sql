use sys;

-- CREATE TABLE Users (
-- 	fName			varchar(255)	NOT NULL,
-- 	lName			varchar(255)	NOT NULL,
-- 	userID			int 			NOT NULL,
-- 	phone			varchar(255)	NOT NULL,
-- 	isAdmin			BOOL			NOT NULL,
-- 	email			varchar(255)	NOT NULL,
-- PRIMARY KEY (userID));

-- CREATE TABLE Equipment (
-- 	eName 			varchar(255)	NOT NULL,
-- 	equipID			varchar(255)	NOT NULL,
-- 	eType 			varchar(255),	
-- 	boxNum			int				NOT NULL,
-- 	wifi_Address	varchar(255)	NOT NULL,
-- 	modelNo			varchar(255),
-- 	serialNo		varchar(255),
-- 	powerState		BOOL			NOT NULL,
-- 	lastUsed		DATE,	
-- 	certNeeded		varchar(255)	NOT NULL,
-- 	lastMaint		DATE,
-- 	needMaint		DATE,
-- 	eSchedule 		DATE,
-- 	surgeLevel		double,
-- 	PRIMARY KEY (equipID)
-- 	);

-- CREATE TABLE Certifications (
-- 	cName 		varchar(255) 		NOT NULL,
-- 	certID		varchar(255)		NOT NULL,
-- 	cType 		varchar(255),
-- 	equipID		varchar(255),
-- 	PRIMARY KEY (certID));

-- CREATE TABLE CertUser (
-- 	userID			int 				NOT NULL,
-- 	certID			varchar(255)		NOT NULL,
-- 	indexID			varchar(255)		NOT NULL,
-- 	PRIMARY KEY (indexID));

-- CREATE TABLE EqCert (
-- 	equipID		varchar(255)		NOT NULL,
-- 	certID		varchar(255)		NOT NULL,
-- 	CONSTRAINT PK_EqCert PRIMARY KEY(equipID, certID));

-- alter table EqCert
-- add constraint
-- foreign key(equipID) references  Equipment(equipID);

-- alter table EqCert
-- add constraint
-- foreign key(certID) references  Equipment(certID);

-- alter table Equipment
-- add constraint
-- foreign key(certNeeded) references  Certifications(certID);

-- alter table Certifications
-- add constraint
-- foreign key(equipID) references Equipment(equipID);

-- alter table CertUser
-- add constraint
-- foreign key(certID) references  Equipment(certID);

-- alter table CertUser
-- add constraint
-- foreign key(userID) references  Equipment(userID);



-- this is so you can user the database from website
-- CREATE USER '<username>'@'localhost';
-- grant all privileges on sys.* to '<username>'@'localhost';

