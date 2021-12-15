class VideosDateException(Exception):
    def __str__(self):
        return "비디오, 날짜 유효하지 않음"
