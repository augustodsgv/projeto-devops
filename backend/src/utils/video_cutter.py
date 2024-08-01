import subprocess
import os
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
class Video_cutter:
    def __init__(self):
        pass

    def cut(self, 
            input_path : str,
            output_path : str | None = None,
            video_start : int = 0,
            video_end : int | None = None):
        
        '''Treating invalid cut times'''
        # Negative time numbers
        if video_start < 0:
            logger.critical(f'Invalid video start at {video_start}: time values should be equal or higher than 0')
            raise ValueError(f'Invalid video start at {video_start}: time values should be equal or higher than 0')
        # Video end greater than video begin
        if (video_end != None and video_start > video_end):
            logger.critical(f'Invalid video start and end: video end should be greater than video start')
            raise ValueError(f'Invalid video start and end: video end should be greater than video start')

        '''Input video name treatment'''

        # FFmpeg doesn´t handle names with white spaces
        if ' ' in input_path:
            input_path = f'"{input_path}"'

        # If output video has the same name as the input name path, overwrites the input video
        if output_path == None:
            output_path = input_path

        # FFmpeg can´t read and write the same file at the same time. Thus, let's create a new file and rename it at the end
        original_output_path : str = output_path
        if output_path == input_path:
            output_path = input_path.split('.mp4')[0] + '_.mp4' 
    
        logger.info(f'Cutting video {input_path} to {output_path} starting at {video_start} ending at {video_end}')

        # Building call to ffmpeg
        cut_call = f"ffmpeg -i {input_path} -ss {video_start}"

        if video_end != None:               # If no video_end is provided, cuts to the end
            cut_call += f" -to {video_end}"

        cut_call += f" -crf 0 -y {output_path}"  # Cutting to maximum quality
        logger.info(f'FFmpeg subprocess call: {cut_call}')
        cut_call = cut_call.split()             # subprocess.Popen recieves string arrays as input

        ffmpeg_process = subprocess.Popen(cut_call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, stderr = ffmpeg_process.communicate()
        if ffmpeg_process.returncode != 0:
            logger.critical(f"Erro ao cortar o vídeo!\n{stderr.decode('utf-8')}")
            raise Exception(f"Erro ao cortar o vídeo!\n{stderr.decode('utf-8')}")
        
        # Deleting original file and replacing with the new cutted video, case it was an inplace cut
        if original_output_path != output_path:
            os.remove(input_path)
            os.rename(output_path, original_output_path)