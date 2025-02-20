/* 
Problem statement
Query all columns for all Marvel cities in the CITY table with populations larger than 100000. The CountryCode for Marvel is Marv.

The CITY table is described as follows:

+---------+--------+
| Field  |  Type    |
+---------+--------+
|   ID    |  Number  | 
|   Name  | Varchar  |
|   CountryCode | Varchar  |
|   Population |   Number  | 
+---------+--------+-------+
*/
select * from CITY where Population > 100000 and CountryCode = 'Marv';