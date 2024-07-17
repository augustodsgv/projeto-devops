import src.reencoder.video_reencoder as vr
import subprocess

class video_not_reencoder(vr.Video_reencoder):
    def __init__(
        self,
        bit_rate : str = None,
        variable_bitrate : bool = False,
        crf_range : float = None,          # 0 - 100, meaning 100 being best quality, 0 worst quality
        speed : str = None,             # realtime, balanced or quality
        n_threads : int = None,
        t_duration : int = None,
        quiet : bool = False,
        time_out : int = None
        ):
        super().__init__(bit_rate, variable_bitrate, crf_range, speed, n_threads, t_duration, quiet, time_out)


    @property
    def crf(self):
        return

    @property
    def _speed(self):
        return
    
    def _set_reencode_call(self, input_file : str, output_file : str = None):
        return ["sleep 10"]
    
if __name__ == '__main__':
    reencoder = video_not_reencoder(time_out=2)
    print(reencoder.reencode("banana.mp4"))