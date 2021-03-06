'''
This query select top 10 music videos based on a score we made using the following parameters:
1.views
2.comments
3.likes
4.dislikes
This is the user custom playlist making query, the user set a value to each parameter by it's importance.
The values are between 1 to 10, and the score is constructed in the following way:
score of a row = row_views*user_views_value + row_likes*user_likes_value ...
Filtering all results to be in a specific genre & country.
Then pick 10 rows who has the highest score (order it by score and limit select to only 10 rows).
'''
VIDEOS_CUSTOM_STATISTICS = {
    'query' :   '''
                SELECT FORMAT(
                   FLOOR(%.2f*views + %.2f*comments + %.2f*likes + %.2f*dislikes + 
                   0.1*(CASE WHEN genre = "%s" THEN 1 ELSE 0 END) + 
                   0.1*(CASE WHEN country = "%s" THEN 1 ELSE 0 END)), 0) AS score,
                   youtube_video_title, youtube_video_id, video_id
                FROM artist_song_video_view  
                GROUP BY video_id
                ORDER BY score DESC
                LIMIT 10
                ''',
    'mode'  : 'select',
    'args': ['views','comments', 'likes', 'dislikes', 'genre', 'country']
}
