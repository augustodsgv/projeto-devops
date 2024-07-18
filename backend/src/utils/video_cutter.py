import subprocess

class Video_cutter:
    def __init__(self):
        pass

    def cut(self, video_path : str, output_path : str = None, video_begin : int = 0, video_end : int = None):
        if video_begin <= 0 or (video_end != None and video_begin > video_end):
            raise ValueError(f'Invalid video cut from {video_begin}s to {video_end}s')
        
        if output_path == None:             # If output video has the same name as the input name path, overwrites the input video
            output_path = video_path
        cut_call = f"ffmpeg -i {video_path} -ss {video_begin}"

        if video_end != None:               # If no video_end is provided, cuts to the end
            cut_call += f" -to {video_end}"

        cut_call +=f" -crf 0 -y {output_path}"
        cut_call = cut_call.split()
        ffmpeg_process = subprocess.Popen(cut_call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = ffmpeg_process.communicate()
        if ffmpeg_process.returncode != 0:
            raise Exception("Erro ao cortar o vídeo!\nstdout:\n\n"+stdout.decode('utf-8') + '\n\nstderr\n\n'+stderr.decode('utf-8'))
        
            
        print(cut_call)
        