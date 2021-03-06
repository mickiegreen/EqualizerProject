'''
This query returns top 10 unliked music videos of a random year.
This query calculate rating for each music video based on it's views, likes and comments.
Then filter them by the randomly selected year.
'''

MOST_UNLIKED_SONGS = {
    'query': '''
               SELECT `year`, youtube_video_id, youtube_video_title 
               FROM 
                   (SELECT `year`,youtube_video_id, youtube_video_title 
                   FROM( 
                       SELECT YEAR(release_date) as `year`,youtube_video_title as title,youtube_video_id as id , 
                        sum(0.3*views+0.5*likes+0.2*comments) AS rating 
                       FROM artist_song_video_view 
                       WHERE country IN(select country from song where YEAR(release_date) = "%s") 
                       GROUP BY id) rating_table 
                   JOIN youtube_video  as main_table ON rating_table.id = main_table.youtube_video_id 
                   ORDER BY rating  
                   limit 10 ) as a ''',
    'args': ['year'],
    'mode'  : 'select',
}