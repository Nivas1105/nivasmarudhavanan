/* 
Problem statement
Print the genre and the maximum net profit among all the movies of that genre released in 2012 per genre. (Download the dataset from console)

Note:
1. Do not print any row where either genre or the net profit is empty/null.
2. net_profit = Domestic + Worldwide - Budget
3. Keep the name of the columns as 'genre' and 'net_profit'
4. The genres should be printed in alphabetical order.
*/

select a.genre, MAX(b.Domestic+ b.Worldwide - c.Budget) as net_profit from genre a
JOIN earning b ON b.Movie_id = a.Movie_id
JOIN IMDB c ON c.Movie_id = b.Movie_id where c.Title LIKE '%2012%' and a.genre IS NOT NULL
and b.Domestic is not NULL
and b.Worldwide is not NULL
and c.Budget is not NULL
group by a.genre order by a.genre;