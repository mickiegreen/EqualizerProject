# -*- coding: utf-8 -*-

# Copyright (c) 2018 Michael Green
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from ..abstract_entity import AbstractEntity as Entity
import equalizer.config as app

class YoutubeVideo(Entity):
    """ youtube video table entity """

    def __init__(self, video_id = 0, likes = None, comments = None,
            views = None, favorites = None, dislikes = None,
            youtube_video_id = 0, youtube_video_title = None, **kwargs):
        super(YoutubeVideo, self).__init__(
            table=app.YOUTUBE_VIDEO_TABLE,
            primary_key=app.YOUTUBE_VIDEO_TABLE_PK,
            select_query=app.YOUTUBE_VIDEO_EXISTS_QUERY
        )
        self.video_id = video_id
        self.likes = likes
        self.comments = comments
        self.views = views
        self.favorites = favorites
        self.dislikes = dislikes
        self.youtube_video_id = youtube_video_id
        self.youtube_video_title = youtube_video_title
