/* 
Problem statement
Table: Logs

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| num         | varchar |
+-------------+---------+
id is the primary key for this table.

Write an SQL query to find all numbers that appear at least three times consecutively.

Return the result table in any order.

The query result format is in the following example:



 Logs table:
+----+-----+
| Id | Num |
+----+-----+
| 1  | 1   |
| 2  | 1   |
| 3  | 1   |
| 4  | 2   |
| 5  | 1   |
| 6  | 2   |
| 7  | 2   |
+----+-----+

 Result table:
+-----------------+
| ConsecutiveNums |
+-----------------+
| 1               |
+-----------------+
  1 is the only number that appears consecutively for at least three times.

*/
with temp as (
    select id,num,Lag(Num, 1) OVER(ORDER BY id) as pnum,
    Lead(Num, 1) OVER(ORDER BY id) as nnum from Logs)
SELECT num AS ConsecutiveNums FROM temp
WHERE num = pnum AND num = nnum AND pnum IS NOT NULL AND nnum IS NOT NULL;