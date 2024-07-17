from src.validator.validator import Validator
import subprocess
import sys


class PSNR_validator(Validator):
    def __init__(self):
        pass

    def compare(self, original_video : str, reencoded_video : str) -> list[float, float, float, float]:
        call = f"ffmpeg -i {original_video} -i {reencoded_video} -hide_banner -filter_complex psnr -f null /dev/null"
        print(call)
        ffmpeg_process = subprocess.Popen(           # Running CLI for PSNR in ffmpeg
            [
                "ffmpeg",
                "-i", original_video,
                "-i", reencoded_video,
                "-hide_banner",
                "-filter_complex", "psnr",
                "-f", "null", "/dev/null"
            ],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE          # Redirecting the stdout and stderr to PIPE, because ffmpeg throws the output in stderr for some reason
            )
        _, std_err = ffmpeg_process.communicate()                            # Getting the stderr, in bytes
        if ffmpeg_process.returncode != 0:
            e_msg = 'Error calculating the PSNR score of the videos.\nFFMPEG message:\n\n' + std_err.decode('utf-8')
            raise Exception(e_msg)
        
        if len(std_err) > 0:
            output = std_err.decode('utf-8')          # Reencoding the stderr from bytes to uft-8
            # The output comes in an output like this:
            '''
            ...
                encoder         : Lavf61.3.104
            Stream #0:0: Video: wrapped_avframe, yuv420p(tv, progressive), 2048x1536 [SAR 1:1 DAR 4:3], q=2-31, 200 kb/s, 15 fps, 15 tbn
                Metadata:
                    encoder         : Lavc61.7.100 wrapped_avframe
            [Parsed_psnr_0 @ 0x7fce60003ac0] PSNR y:44.476451 u:56.186794 v:55.762140 average:46.086048 min:29.963078 max:inf
            [out#0/null @ 0x56238d949040] video:774KiB audio:0KiB subtitle:0KiB other streams:0KiB global headers:0KiB muxing overhead: unknown frame= 1801 fps=116 q=-0.0 Lsize=N/A time=00:02:00.00 bitrate=N/A speed= 7.7x  
            '''
            # Ou PSNR information is at the penultimate line, at 'average:46.086048'.
            splitted_lines = output.split('\n')         # Splitting lines
            linha : str = ''
            for raw_line in reversed(splitted_lines):           # Search in every line, from bottom up (information appears at the end)
                if 'PSNR' in raw_line:                  # Search the one which has the PSNR output
                    linha = raw_line
                    break

            average = (linha.split('average:')[-1]).split(' ')[0]  # Splitting the average output
            Y = (linha.split('y:')[-1]).split(' ')[0]  # Splitting the Y plane
            U = (linha.split('u:')[-1]).split(' ')[0]  # Splitting the U plane
            V = (linha.split('v:')[-1]).split(' ')[0]  # Splitting the V plane

            
            return float(average), float(Y), float(U), float(V) 
        


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise Exception('Missing file path\'s arguments.\n usage: python3 PSNR_validator {source file} {reencoded file}')
    source_file = sys.argv[1]
    reencoded_file = sys.argv[2]

    validator = PSNR_validator()
    average_score, Y_score, U_score, V_score = validator.compare(source_file, reencoded_file)
    print(f'Average PSNR score: {average_score}, Y score: {Y_score}, U score: {U_score}, V score: {V_score},')