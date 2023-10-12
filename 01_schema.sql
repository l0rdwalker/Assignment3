-- SCHEMA FILE for OPAL DATA

DROP SCHEMA IF EXISTS opaltravel cascade;

CREATE SCHEMA opaltravel;

SET SCHEMA 'opaltravel';

DROP TABLE IF EXISTS Trips;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS UserRoles;
DROP TABLE IF EXISTS Stations;
DROP TABLE IF EXISTS StationTypes;
DROP TABLE IF EXISTS OpalCards;
DROP TABLE IF EXISTS CardTypes;
DROP TABLE IF EXISTS TravelTimes;

-- UserRoles: userroleid, rolename, isAdmin, (privilegeFlags?) 
CREATE TABLE UserRoles (
    userroleid serial PRIMARY KEY,
    rolename text,
    isAdmin boolean NOT NULL,
    privilegeFlags bigint
);

-- Users: userid, cardid, firstname, lastname, preferredname, userroleid, password
CREATE TABLE Users (
    userid serial PRIMARY KEY,  
    firstname text, 
    lastname text, 
    userroleid bigint REFERENCES UserRoles(userroleid) NOT NULL, 
    password text NOT NULL
);
-- can a user have multiple cards? if so, scrap cardid for UserCards table with PK (userid,cardid)

-- Cardtype: typeid, type name, fare modifier
CREATE TABLE CardTypes (
    cardtypeid serial PRIMARY KEY,
    typename text NOT NULL,
    faremodifier text DEFAULT '1' -- ideally a function operator
);

-- OpalCard: cardid, card type id, expiry, balance
CREATE TABLE OpalCards (
    cardid serial PRIMARY KEY,
    cardtypeid serial REFERENCES CardTypes(cardtypeid) NOT NULL,
    userid int REFERENCES Users(userid) NOT NULL,
    expiry date,
    balance decimal NOT NULL
);

-- StationType: stationtypeid, typename
CREATE TABLE StationTypes (
    stationtypeid serial PRIMARY KEY,
    stationtypename text NOT NULL
);

-- Station: stationid, station name, stationtype, lat, long, (lines here or a routes table?)
CREATE TABLE Stations (
    stationid serial PRIMARY KEY,
    stationname varchar(250) NOT NULL,
    stationtypeid bigint REFERENCES StationTypes(stationtypeid) NOT NULL,
    latitude float,
    longitude float

);

-- Trips: tripid, userid, traveldate, entrystationid, exitstationid,tripstarttime
-- should tripstarttime and travel data be combined?
CREATE TABLE Trips (
    tripid serial PRIMARY KEY,
    cardid bigint REFERENCES OpalCards(cardid) ON DELETE CASCADE NOT NULL ,
    traveldate date NOT NULL,
    entrystationid bigint REFERENCES Stations(stationid) NOT NULL,
    exitstationid bigint REFERENCES Stations(stationid) NOT NULL,
    tripstarttime time
);

-- Travel times: start stationaid, end stationid, seconds/minutes?, minhops 
CREATE TABLE TravelTimes (
    startstationid bigint REFERENCES Stations(stationid) NOT NULL,
    endstationid bigint REFERENCES Stations(stationid) NOT NULL,
    expectedtraveltimeSeconds bigint NOT NULL,
    stopsTraversed bigint,
    triplegs int,
    coordinatemaplen bigint,
    CONSTRAINT traveltimes_pk PRIMARY KEY (startstationid, endstationid)
);