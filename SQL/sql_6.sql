/* 
Problem statement
From the IMDb dataset, print the title and rating of those movies which have a genre starting from 'C' released in 2014 with a budget higher than 4 Crore.
*/
select title,rating from IMDB LEFT JOIN genre ON IMDB.Movie_id = genre.Movie_id where genre.genre like 'C%' and IMDB.budget > 40000000 and IMDB.title LIKE '%2014%';



