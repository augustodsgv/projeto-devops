from src.validator.validator import Validator
import subprocess
import sys


class SSIM_validator(Validator):
    def __init__(self):
        pass

    def compare(self, original_video : str, reencoded_video : str) -> list[float, float, float, float]:
        pipes = subprocess.Popen(           # Running CLI for PSNR in ffmpeg
            [
                "ffmpeg",
                "-i", original_video,
                "-i", reencoded_video,
                "-hide_banner",
                "-filter_complex", "ssim",
                "-f", "null", "/dev/null"
            ],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE          # Redirecting the stdout and stderr to PIPE, because ffmpeg throws the output in stderr for some reason
            )
        _, std_err = pipes.communicate()                            # Getting the stderr, in bytes
    
        if len(std_err) > 0:
            output = std_err.decode('utf-8')          # Reencoding the stderr from bytes to uft-8
            # The output comes in an output like this:
            '''
            [Parsed_ssim_0 @ 0x7f8950003ac0] SSIM Y:0.981412 (17.307608) U:0.986700 (18.761430) V:0.986825 (18.802646) All:0.983195 (17.745709)
            '''
            # Ou SSIM information is at the line with 'SSIM Y:...', at 'average:46.086048'.
            
            splitted_lines = output.split('\n')         # Splitting lines
            linha : str = ''
            for raw_line in reversed(splitted_lines):           # Search in every line, from bottom up (information appears at the end)
                if 'SSIM' in raw_line:                  # Search the one which has the PSNR output
                    linha = raw_line
                    break
            Y = float((linha.split('Y:')[-1]).split(' ')[0])  # Splitting the Y plane
            U = float((linha.split('U:')[-1]).split(' ')[0])  # Splitting the U plane
            V = float((linha.split('V:')[-1]).split(' ')[0])  # Splitting the V plane
            average = (Y + U + V) / 3

            return average, Y, U, V
        
        


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise Exception('Missing file path\'s arguments.\n usage: python3 PSNR_validator {source file} {reencoded file}')
    source_file = sys.argv[1]
    reencoded_file = sys.argv[2]

    validator = SSMI_validator()
    Y, U, V = validator.compare(source_file, reencoded_file)
    print(f'Y plane score: {Y}, U plane score: {U}, V plane score: {V}')