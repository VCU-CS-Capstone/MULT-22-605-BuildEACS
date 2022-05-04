use sys;

set foreign_key_checks = 0;

-- INSERT INTO Equipment VALUES('<Equipment_Name>', '<EquipmentID>', <Equipment_Type> , <Box_Number>, '<Wifi_Address>', '<Model_Number>', '<Serial_Number>', <Power_State(0 off, 1 on)>, '<Last_Used(format:YYYY-MM-DD)>', '<Cert_Needed>', '<Last_Maintained(format:YYYY-MM-DD)>', '<Need_Maintained(format:YYYY-MM-DD)>', '<Scheduled(format:YYYY-MM-DD)>', <Surge_Level>);
-- INSERT INTO Equipment VALUES('Table_Saw', '00001', NULL , 1, '192.442.456.813', 'GRIZZLY', '823nf428', 0, '2021-10-22', 'Cert_001', NULL, NULL, NULL, NULL);

-- INSERT INTO Users VALUES('<First_Name>', '<Last_Name>', <User_ID(fobID)>, '<Phone_Num(format: 000-000-0000)>', <Admin?(yes: 1, no: 0)>, '<Email_Address>');
-- INSERT INTO Users VALUES('Bob', 'Nobody', 2384, '573-382-5485', 0, 'MrNobody@hotmail.com');

-- INSERT INTO Certifications VALUES('<Cert_Name>', '<Cert_ID>', '<Cert_Type>', '<Equipment_ID>');
-- INSERT INTO Certifications VALUES('Table_Saw_Cert', 'Cert_001', NULL, '00001');

-- INSERT INTO EqCert VALUES('<Equipment_ID>', '<Cert_ID>');
-- INSERT INTO EqCert VALUES('00001', 'Cert_001');

-- INSERT INTO CertUser VALUES(<User_ID(FobID)>, '<Cert_ID>', <Index_Number>);
-- INSERT INTO CertUser VALUES(2384, 'Cert_001', 1);


-- (uncomment one of these to see table results)
-- select * from Certifications;
-- select * from Users;
-- select * from CertUser;
-- select * from EqCert;
-- select * from Equipment;





