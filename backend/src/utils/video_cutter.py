from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
ffmpeg_extract_subclip("../videos/h265.mp4", 0, 120, targetname="../videos/h265_short.mp4")