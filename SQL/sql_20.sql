/* 
Problem statement
Print the genre and the maximum weighted rating among all the movies of that genre released in 2014 per genre. (Download the dataset from console)

Note:
1. Do not print any row where either genre or the weighted rating is empty/null.
2.  weighted_rating = avgerge of (rating + metacritic/10.0)
3. Keep the name of the columns as 'genre' and 'weighted_rating'
4. The genres should be printed in alphabetical order.
*/

SELECT b.genre , max((a.rating + a.MetaCritic/10.0)/2) as weighted_rating FROM 
IMDB a JOIN  genre b on a.Movie_id=b.Movie_id where  
b.genre is NOT NULL and a.Title LIKE '%2014%' GROUP BY b.genre ORDER BY b.genre;