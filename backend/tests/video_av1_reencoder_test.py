import src.reencoder.av1_reencoder as av1
import pytest

class Test_constructor:
    # Valid encoders
    def test_av1_valid_reencoders_no_attr(self):
        no_attr = av1.Av1_reencoder()
        assert no_attr.bit_rate == None
        assert no_attr.variable_bitrate == False
        assert no_attr.crf_range == None
        assert no_attr.crf == None
        assert no_attr.speed == None
        assert no_attr.quiet == False
        assert no_attr.n_threads == None

    # Only bit_rate
    def test_av1_valid_reencoders_bitrate_only(self):
        bitrate_only = av1.Av1_reencoder(bit_rate='10M')
        assert bitrate_only.bit_rate == '10M'
        assert bitrate_only.variable_bitrate == False
        assert bitrate_only.crf_range == None
        assert bitrate_only.crf == None
        assert bitrate_only.speed == None

    # 0% of crf
    def test_av1_valid_reencoders_crf_only_0(self):
        crf_only = av1.Av1_reencoder(crf_range=0)
        assert crf_only.bit_rate == None
        assert crf_only.variable_bitrate == False
        assert crf_only.crf_range == 0
        assert crf_only.crf == 63
        assert crf_only.speed == None

    # 50% of crf
    def test_av1_valid_reencoders_crf_only_50(self):
        crf_only = av1.Av1_reencoder(crf_range=50)
        assert crf_only.bit_rate == None
        assert crf_only.variable_bitrate == False
        assert crf_only.crf_range == 50
        assert crf_only.crf == 31
        assert crf_only.speed == None
    
    # 100% of crf (lossless)
    def test_av1_valid_reencoders_crf_only_100(self):
        crf_only = av1.Av1_reencoder(crf_range=100)
        assert crf_only.bit_rate == None
        assert crf_only.variable_bitrate == False
        assert crf_only.crf == 0
        assert crf_only.speed == None

    # Invalid crf
    def test_av1_invalid_crf_range(self):
        with pytest.raises(ValueError) as e_info:
            av1.Av1_reencoder(crf_range=-1)
        assert str(e_info.value) == 'Provide an integer crf value between 0 and 100, 0 being worst quality and 100 best'
        
        with pytest.raises(ValueError) as e_info:
            av1.Av1_reencoder(crf_range=101)
        assert str(e_info.value) == 'Provide an integer crf value between 0 and 100, 0 being worst quality and 100 best'

    # realtime speed / quality
    def test_av1_valid_reencoders_speed_only_realtime(self):
        speeed_only = av1.Av1_reencoder(speed='realtime')
        assert speeed_only.bit_rate == None
        assert speeed_only.variable_bitrate == False
        assert speeed_only.crf_range == None
        assert speeed_only.crf == None
        assert speeed_only.speed == 'realtime'
        assert speeed_only._speed == 'speed'

    # balanced speed / quality
    def test_av1_valid_reencoders_speed_only_balanced(self):
        speeed_only = av1.Av1_reencoder(speed='balanced')
        assert speeed_only.bit_rate == None
        assert speeed_only.variable_bitrate == False
        assert speeed_only.crf_range == None
        assert speeed_only.crf == None
        assert speeed_only._speed == 'balanced'
        assert speeed_only.speed == 'balanced'

    # quality speed / quality
    def test_av1_valid_reencoders_speed_only_quality(self):
        speeed_only = av1.Av1_reencoder(speed='quality')
        assert speeed_only.bit_rate == None
        assert speeed_only.variable_bitrate == False
        assert speeed_only.crf_range == None
        assert speeed_only.crf == None
        assert speeed_only._speed == 'quality'
        assert speeed_only.speed == 'quality'

    # Invalid speed mode
    def test_av1_invalid_speed_mode(self):
        with pytest.raises(ValueError) as e_info:
            av1.Av1_reencoder(speed='bad')
        print(e_info.value)
        assert str(e_info.value) == 'Invalid speed mode "bad". Available values: (\'realtime\', \'balanced\', \'quality\')'
    # Invalid bitrate configuration
    def test_av1_invalid_bit_rate_setup(self):
        with pytest.raises(Exception) as e_info:
            av1.Av1_reencoder(bit_rate='10M', variable_bitrate=True)
        assert str(e_info.value) == 'You can\'t set a fixed "bit_rate" and set a variable bitrate'

    # crf property
    def test_av1_crf_property(self):
        # Worst quality
        reencoder = av1.Av1_reencoder(crf_range=0)
        assert reencoder.crf == 63

        # Best quality
        reencoder = av1.Av1_reencoder(crf_range=100)
        assert reencoder.crf == 0

        # 50%
        reencoder = av1.Av1_reencoder(crf_range=50)
        assert reencoder.crf == 31

class Test_reencode:
    # No encoder args
    def test_av1_reencode_call_no_args(self):
        reencoder = av1.Av1_reencoder()
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libaom-av1", "-y", "apple.webm"]
    
    # Only bitrate args
    def test_av1_reencode_call_bitrate_only(self):
        reencoder = av1.Av1_reencoder(bit_rate='1500K')
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libaom-av1", "-y", "-b", "1500K", "apple.webm"]

    # Only crf
    def test_av1_reencode_call_crf_only(self):
        reencoder = av1.Av1_reencoder(crf_range=50)
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libaom-av1", "-y", "-crf", "31", "apple.webm"]

    # Only speed
    def test_av1_reencode_call_speed_only(self):
        reencoder = av1.Av1_reencoder(speed='quality')
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libaom-av1", "-y", "-quality", "quality", "apple.webm"]

    # Only threads
    def test_av1_reencode_call_threads_only(self):
        reencoder = av1.Av1_reencoder(n_threads=7)
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libaom-av1", "-y", "-threads", "7", "apple.webm"]

    # Only duration
    def test_av1_reencode_call_duration_only(self):
        reencoder = av1.Av1_reencoder(t_duration=175)
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libaom-av1", "-y", "-t", "175", "apple.webm"]

    # Only quiet
    def test_av1_reencode_call_quiet_only(self):
        reencoder = av1.Av1_reencoder(quiet=True)
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libaom-av1", "-y", "-hide_banner", "-loglevel", "error", "apple.webm"]


    # crf 10 (~84%), bitrate 750k
    def test_av1_reencode_call_crf_bitrate(self):
        reencoder = av1.Av1_reencoder(bit_rate='750K', crf_range=84.0)
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libaom-av1", "-y", "-b", "750K", "-crf", "10", "apple.webm"]

    # crf 84% (~10), speed balanced
    def test_av1_reencode_call_crf_speed(self):
        reencoder = av1.Av1_reencoder(speed='balanced', crf_range=84.0)
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libaom-av1", "-y", "-crf", "10", "-quality", "balanced", "apple.webm"]
