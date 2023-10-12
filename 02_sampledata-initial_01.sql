
SET SCHEMA 'opaltravel';

-- assuming that schema.sql has been run and that all data has been dropped
-- test data to see if our code works

-- UserRoles: userroleid, rolename, isAdmin, (privilegeFlags?) 
INSERT INTO UserRoles(rolename, isAdmin) VALUES ('Traveler', false);
INSERT INTO UserRoles(rolename, isAdmin) VALUES ('Employee', false);
INSERT INTO UserRoles(rolename, isAdmin) VALUES ('Admin', true);
INSERT INTO UserRoles(rolename, isAdmin) VALUES ('Route Designer', true);

-- Cardtype: typeid, type name, fare modifier
INSERT INTO CardTypes(typename, faremodifier) VALUES ('Adult','* 1');
INSERT INTO CardTypes(typename, faremodifier) VALUES ('Child/Youth','* 0.5');
INSERT INTO CardTypes(typename, faremodifier) VALUES ('Concession','* 0.5');
INSERT INTO CardTypes(typename, faremodifier) VALUES ('Employee','* 0');
INSERT INTO CardTypes(typename, faremodifier) VALUES ('Free Travel','* 0');
INSERT INTO CardTypes(typename, faremodifier) VALUES ('School Student','* 0');
INSERT INTO CardTypes(typename, faremodifier) VALUES ('Senior/Pensioner','* 0 + 2.5');
INSERT INTO CardTypes(typename, faremodifier) VALUES ('Sgl Trip Rail Adult','* 1');
INSERT INTO CardTypes(typename, faremodifier) VALUES ('Sgl Trip Rail Child/Youth','* 0.5');
INSERT INTO CardTypes(typename, faremodifier) VALUES ('Day Pass without SAF','* 0 + 25');

-- StationTypes: stationtypeid, typename
INSERT INTO StationTypes(stationtypename) VALUES ('Train');
INSERT INTO StationTypes(stationtypename) VALUES ('Metro');
INSERT INTO StationTypes(stationtypename) VALUES ('Bus');
INSERT INTO StationTypes(stationtypename) VALUES ('Ferry');
INSERT INTO StationTypes(stationtypename) VALUES ('Light Rail');

-- Users: userid, cardid, firstname, lastname, preferredname, userroleid, password
INSERT INTO Users(firstname, lastname, userroleid, password) VALUES ('Bob', 'Sanderson', 1, 'brisket');
INSERT INTO Users(firstname, lastname, userroleid, password) VALUES ('Darren', 'Erikson', 1, 'brulee');
INSERT INTO Users(firstname, lastname, userroleid, password) VALUES ('Helene', 'Yung', 1, 'cake');
INSERT INTO Users(firstname, lastname, userroleid, password) VALUES ('Chirri', 'Parsons', 3, 'sherbert');


-- OpalCard: cardid, userid, cardtypeid, expiry, balance
INSERT INTO OpalCards(cardtypeid, userid, expiry, balance) VALUES (1,1,now()+ interval '1 year',100);
INSERT INTO OpalCards(cardtypeid, userid, expiry, balance) VALUES (2,1,now()+ interval '1 year',20);
INSERT INTO OpalCards(cardtypeid, userid, expiry, balance) VALUES (3,2,now()+ interval '1 year',30);
INSERT INTO OpalCards(cardtypeid, userid, expiry, balance) VALUES (1,2,now()+ interval '1 year',500);
INSERT INTO OpalCards(cardtypeid, userid, expiry, balance) VALUES (4,3,now()+ interval '1 year',6);
INSERT INTO OpalCards(cardtypeid, userid, expiry, balance) VALUES (7,3,now()+ interval '1 year',4);



-- Station: stationid, station name, stationtype, lat, long, (lines here or a routes table?)
INSERT INTO Stations(stationname, stationtypeid) VALUES ('Strathfield', 1);
INSERT INTO Stations(stationname, stationtypeid) VALUES ('Redfern', 1);
INSERT INTO Stations(stationname, stationtypeid) VALUES ('Central', 1);
INSERT INTO Stations(stationname, stationtypeid) VALUES ('Central Chalmers Street', 2);
INSERT INTO Stations(stationname, stationtypeid) VALUES ('Circular Quay', 2);

-- Trips: tripid, userid, traveldate, entrystationid, exitstationid, tripstarttime
INSERT INTO Trips(cardid, traveldate, entrystationid, exitstationid,tripstarttime) VALUES (1,'2023/02/19',1,2,'10:00:00');
INSERT INTO Trips(cardid, traveldate, entrystationid, exitstationid,tripstarttime) VALUES (1,'2023/02/26',1,2,'10:00:00');
INSERT INTO Trips(cardid, traveldate, entrystationid, exitstationid,tripstarttime) VALUES (1,'2023/03/03',1,2,'10:00:00');
INSERT INTO Trips(cardid, traveldate, entrystationid, exitstationid,tripstarttime) VALUES (1,'2023/03/10',1,2,'10:00:00');
INSERT INTO Trips(cardid, traveldate, entrystationid, exitstationid,tripstarttime) VALUES (1,'2023/02/19',2,1,'19:00:00');
INSERT INTO Trips(cardid, traveldate, entrystationid, exitstationid,tripstarttime) VALUES (1,'2023/02/26',2,1,'19:00:00');
INSERT INTO Trips(cardid, traveldate, entrystationid, exitstationid,tripstarttime) VALUES (1,'2023/03/03',2,1,'19:00:00');
INSERT INTO Trips(cardid, traveldate, entrystationid, exitstationid,tripstarttime) VALUES (1,'2023/03/10',2,1,'19:00:00');
INSERT INTO Trips(cardid, traveldate, entrystationid, exitstationid,tripstarttime) VALUES (3,'2023/02/19',1,2,'7:00:00');
INSERT INTO Trips(cardid, traveldate, entrystationid, exitstationid,tripstarttime) VALUES (3,'2023/03/19',1,2,'7:00:00');
INSERT INTO Trips(cardid, traveldate, entrystationid, exitstationid,tripstarttime) VALUES (3,'2023/04/19',1,2,'7:00:00');
INSERT INTO Trips(cardid, traveldate, entrystationid, exitstationid,tripstarttime) VALUES (3,'2023/05/19',1,2,'7:00:00');
INSERT INTO Trips(cardid, traveldate, entrystationid, exitstationid,tripstarttime) VALUES (3,'2023/06/19',1,2,'7:00:00');
-- logically invalid trip -- going from train to metro without tapping off
INSERT INTO Trips(cardid, traveldate, entrystationid, exitstationid,tripstarttime) VALUES (1,'2023/04/10',1,4,'11:00:00');

-- Travel times: start stationaid, end stationid, seconds/minutes?, minhops 
INSERT INTO TravelTimes(startstationid, endstationid, expectedtraveltimeSeconds, stopsTraversed, triplegs, coordinatemaplen) VALUES (1,2,780,3,1,15);
INSERT INTO TravelTimes(startstationid, endstationid, expectedtraveltimeSeconds, stopsTraversed, triplegs, coordinatemaplen) VALUES (2,3,180,1,1,4);
INSERT INTO TravelTimes(startstationid, endstationid, expectedtraveltimeSeconds, stopsTraversed, triplegs, coordinatemaplen) VALUES (1,3,900,4,1,19);