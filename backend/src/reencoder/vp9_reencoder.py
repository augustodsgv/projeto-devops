from src.reencoder.video_reencoder import Video_reencoder
import subprocess
import math

class Vp9_reencoder(Video_reencoder):
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

        if crf_range != None:
            if (crf_range < 0 or crf_range > 100):
                raise ValueError('Provide an integer crf value between 0 and 100, 0 being worst quality and 100 best')
        self.crf_range = crf_range

        # Checking for ambiguous configuration
        if bit_rate != None and variable_bitrate == True:
            raise Exception('You can\'t set a fixed "bit_rate" and set a variable bitrate')
        
        # speed treatment
        speed_modes = ('realtime', 'good', 'best')
        if speed != None and speed not in speed_modes:
            raise ValueError(f'Invalid speed mode "{speed}". Available values: {speed_modes}')
        
        self.speed = speed

        self.bit_rate = bit_rate if bit_rate != None else None
        self.variable_bitrate = variable_bitrate

        self.n_threads = str(n_threads) if n_threads != None else None
        self.t_duration = str(t_duration) if t_duration != None else None
        self.timeout = time_out

        self.quiet = quiet

    @property
    def crf(self):
        # libpx-vp9 accepts crf from 0 to 63. 0 means 63, 100 means 0
        if self.crf_range != None:
            return 63 - math.ceil(63 * (self.crf_range / 100))
        else:
            return None
    
    # Calls ffmpeg and returns if it could be finished
    def reencode(self, input_file : str, output_file : str = None) -> bool:
        ffmpeg_call = self._set_reencode_call(input_file, output_file)
        if not self.quiet:
            print(f'ffmpeg call: {ffmpeg_call}')
        process = subprocess.Popen(ffmpeg_call, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if self.timeout != None:
            # timeout exception
            try:
                code = process.wait(self.timeout)
                stdout, stderr = process.communicate()
                if code != 0:
                    e_msg = 'Error '+ code +'with the ffmpeg!\nffmpeg output:\n' + stderr.decode('utf-8')
                    raise Exception(e_msg)
                return True
            except Exception as e:
                print(str(e))
                return False
        else:
            process.communicate()
            return True

    def _set_reencode_call(self, input_file : str, output_file : str = None):
        if output_file == None:
            output_file = input_file.split('.mp4')[0] + '.webm'

        ffmpeg_call = [
            "ffmpeg",
            "-i", input_file,           # input file
            "-c:v", "libvpx-vp9",       # video codec
            "-c:a", "libopus",          # audio codec
            "-y",                       # Sobrescrever arquivo de output, se existir
        ]
        
        if self.bit_rate != None:
            # WARN: this is hardcoded
            ffmpeg_call.extend(["-b:v", self.bit_rate])
        
        if self.crf != None:
            ffmpeg_call.extend(["-crf", str(self.crf)])
        
        # -deadline realtime, -deadline good, -deadline best
        if self.speed != None:
            ffmpeg_call.extend(["-deadline", self.speed])

        if self.n_threads != None:
            ffmpeg_call.extend(["-threads", self.n_threads])
        
        if self.t_duration != None:
            ffmpeg_call.extend(["-t", self.t_duration])

        if self.quiet:
            ffmpeg_call.extend(["-hide_banner", "-loglevel", "error"])

        ffmpeg_call.append(output_file)
        string = ''
        for i in ffmpeg_call:
            string += ' ' + i
        return string

