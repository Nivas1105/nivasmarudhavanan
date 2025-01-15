CREATE DATABASE fifa_worldcup_2014;
USE fifa_worldcup_2014;

-- mysqlimport --ignore-lines=1 --fields-terminated-by=',' --fields-enclosed-by='"' --lines-terminated-by='\n' --local -u username -p database_name /Users/priyankam/Documents/UTA\ ASSIGNMENTS/BIG\ DATA/ASSIGNMENT1/Players.csv
use fifa_worldcup_2014;
select count(Name) from players;

CREATE TABLE COUNTRY (
    Country_Name VARCHAR(100) PRIMARY KEY,
    Population INT,
    Number_of_Worldcup_won INT,
    Manager VARCHAR(100),
    Capital VARCHAR(100)
);

CREATE TABLE PLAYER (
    Player_id INT PRIMARY KEY,
    Name VARCHAR(100),
    Fname VARCHAR(100),
    Lname VARCHAR(100),
    DOB DATE,
    Country_Name VARCHAR(100),
    Height DECIMAL(4, 2),
    Club VARCHAR(100),
    Position VARCHAR(50),
    Caps_for_country INT,
    Is_captain BOOLEAN,
    FOREIGN KEY (Country_Name) REFERENCES COUNTRY(Country_Name)
);

CREATE TABLE MATCHES (
    Match_id INT PRIMARY KEY,
    Date DATE,
    Start_time TIME,
    Team1 VARCHAR(100),
    Team2 VARCHAR(100),
    Team1_score INT,
    Team2_score INT,
    Stadium VARCHAR(100),
    Host_city VARCHAR(100),
    FOREIGN KEY (Team1) REFERENCES COUNTRY(Country_Name),
    FOREIGN KEY (Team2) REFERENCES COUNTRY(Country_Name)
);
CREATE TABLE PLAYER_STATISTICS (
    Player_id INT,
    No_of_Matches INT,
    Goals INT,
    Assists INT,
    Minutes_Played INT,
    PRIMARY KEY (Player_id),
    FOREIGN KEY (Player_id) REFERENCES PLAYER(Player_id)
);
CREATE TABLE DISCIPLINARY_RECORD (
    Player_id INT,
    No_of_Yellow_cards INT,
    No_of_Red_cards INT,
    PRIMARY KEY (Player_id),
    FOREIGN KEY (Player_id) REFERENCES PLAYER(Player_id)
);
CREATE TABLE PAST_WINNERS (
    Year INT PRIMARY KEY,
    Host VARCHAR(100),
    Winner VARCHAR(100),
    FOREIGN KEY (Winner) REFERENCES COUNTRY(Country_Name)
);

-- 1. Retrieve the list of country names that have won a World Cup
SELECT DISTINCT Winner AS Country_Name
FROM PAST_WINNERS;

-- 2. Retrieve the list of country names that have won a World Cup and the number of World Cups each has won in descending order
SELECT Country_Name, Number_of_Worldcup_won
FROM COUNTRY
WHERE Number_of_Worldcup_won > 0
ORDER BY Number_of_Worldcup_won DESC;

-- 3. List the Capital of the countries in increasing order of country population for countries that have a population of more than 100 million
SELECT Capital
FROM COUNTRY
WHERE Population > 100
ORDER BY Population ASC;

-- 4. List the Name of the stadiums which have hosted a match where the number of goals scored by a single team was greater than 4
SELECT DISTINCT Stadium
FROM MATCHES
WHERE Team1_score > 4 OR Team2_score > 4;

-- 5. List the names of all the cities which have the name of the Stadium starting with "Estadio":
SELECT DISTINCT Host_city
FROM MATCHES
WHERE Stadium LIKE 'Estadio%';

-- 6. List all stadiums and the number of matches hosted by each stadium:
SELECT Stadium, COUNT(*) AS Number_of_Matches
FROM MATCHES
GROUP BY Stadium;

-- 7. List the First Name, Last Name, and Date of Birth of Players whose heights are greater than 198 cms:
SELECT Fname, Lname, DOB
FROM PLAYERS
WHERE Height > 198;

-- BONUS QUESTION

-- 1. List the Stadium Names and the Teams (Team1 and Team2) that played Matches between 20-Jun-2014 and 24-Jun-2014:
SELECT Stadium, Team1, Team2
FROM MATCHES
WHERE Date BETWEEN '2014-06-20' AND '2014-06-24';

-- 2. List the Fname, Lname, Position, and Number of Goals scored by the Captain of a team who has more than 2 Yellow cards or 1 Red card:
SELECT p.Fname, p.Lname, p.Position, ps.Goals
FROM PLAYERS p
JOIN PLAYER_STATISTICS ps ON p.Player_id = ps.Player_id
JOIN DISCIPLINARY_RECORD dr ON p.Player_id = dr.Player_id
WHERE p.Is_captain = TRUE
  AND (dr.No_of_Yellow_cards > 2 OR dr.No_of_Red_cards > 1);





