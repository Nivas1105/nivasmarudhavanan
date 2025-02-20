/* 
Problem statement

Print the title and ratings of the movies released in 2012 whose metacritic rating is more than 60 and Domestic collections exceed 10 Crores. (Download the dataset from console)
*/

select title,rating from IMDB a JOIN earning b ON a.Movie_id = b.Movie_id where b.Domestic > 100000000 and a.MetaCritic>60 and a.title LIKE'%2012%';