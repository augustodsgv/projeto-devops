import src.reencoder.vp8_reencoder as vp8
import pytest

class Test_constructor:
    # Valid encoders
    def test_vp8_valid_reencoders_no_attr(self):
        no_attr = vp8.Vp8_reencoder()
        assert no_attr.bit_rate == None
        assert no_attr.variable_bitrate == False
        assert no_attr.crf_range == None
        assert no_attr.crf == None
        assert no_attr.speed == None
        assert no_attr.quiet == False
        assert no_attr.n_threads == None

    # Only bit_rate
    def test_vp8_valid_reencoders_bitrate_only(self):
        bitrate_only = vp8.Vp8_reencoder(bit_rate='10M')
        assert bitrate_only.bit_rate == '10M'
        assert bitrate_only.variable_bitrate == False
        assert bitrate_only.crf_range == None
        assert bitrate_only.crf == None
        assert bitrate_only.speed == None

    # 0% of crf
    def test_vp8_valid_reencoders_crf_only_0(self):
        crf_only = vp8.Vp8_reencoder(crf_range=0)
        assert crf_only.bit_rate == None
        assert crf_only.variable_bitrate == False
        assert crf_only.crf_range == 0
        assert crf_only.crf == 63
        assert crf_only.speed == None

    # 50% of crf
    def test_vp8_valid_reencoders_crf_only_50(self):
        crf_only = vp8.Vp8_reencoder(crf_range=50)
        assert crf_only.bit_rate == None
        assert crf_only.variable_bitrate == False
        assert crf_only.crf_range == 50
        assert crf_only.crf == 33
        assert crf_only.speed == None
    
    # 100% of crf (lossless)
    def test_vp8_valid_reencoders_crf_only_100(self):
        crf_only = vp8.Vp8_reencoder(crf_range=100)
        assert crf_only.bit_rate == None
        assert crf_only.variable_bitrate == False
        assert crf_only.crf == 4
        assert crf_only.speed == None

    # Invalid crf
    def test_vp8_invalid_crf_range(self):
        with pytest.raises(ValueError) as e_info:
            vp8.Vp8_reencoder(crf_range=-1)
        assert str(e_info.value) == 'Provide an integer crf value between 0 and 100, 0 being worst quality and 100 best'
        
        with pytest.raises(ValueError) as e_info:
            vp8.Vp8_reencoder(crf_range=101)
        assert str(e_info.value) == 'Provide an integer crf value between 0 and 100, 0 being worst quality and 100 best'

    # realtime speed / quality
    def test_vp8_valid_reencoders_speed_only_realtime(self):
        speeed_only = vp8.Vp8_reencoder(speed='realtime')
        assert speeed_only.bit_rate == None
        assert speeed_only.variable_bitrate == False
        assert speeed_only.crf_range == None
        assert speeed_only.crf == None
        assert speeed_only.speed == 'realtime'
        assert speeed_only._speed == 'rt'

    # balanced speed / quality
    def test_vp8_valid_reencoders_speed_only_balanced(self):
        speeed_only = vp8.Vp8_reencoder(speed='balanced')
        assert speeed_only.bit_rate == None
        assert speeed_only.variable_bitrate == False
        assert speeed_only.crf_range == None
        assert speeed_only.crf == None
        assert speeed_only._speed == 'good'
        assert speeed_only.speed == 'balanced'

    # quality speed / quality
    def test_vp8_valid_reencoders_speed_only_quality(self):
        speeed_only = vp8.Vp8_reencoder(speed='quality')
        assert speeed_only.bit_rate == None
        assert speeed_only.variable_bitrate == False
        assert speeed_only.crf_range == None
        assert speeed_only.crf == None
        assert speeed_only._speed == 'best'
        assert speeed_only.speed == 'quality'

    # Invalid speed mode
    def test_vp8_invalid_speed_mode(self):
        with pytest.raises(ValueError) as e_info:
            vp8.Vp8_reencoder(speed='bad')
        print(e_info.value)
        assert str(e_info.value) == 'Invalid speed mode "bad". Available values: (\'realtime\', \'balanced\', \'quality\')'
    # Invalid bitrate configuration
    def test_vp8_invalid_bit_rate_setup(self):
        with pytest.raises(Exception) as e_info:
            vp8.Vp8_reencoder(bit_rate='10M', variable_bitrate=True)
        assert str(e_info.value) == 'You can\'t set a fixed "bit_rate" and set a variable bitrate'

    # crf property
    def test_vp8_crf_property(self):
        # Worst quality
        reencoder = vp8.Vp8_reencoder(crf_range=0)
        assert reencoder.crf == 63

        # Best quality
        reencoder = vp8.Vp8_reencoder(crf_range=100)
        assert reencoder.crf == 4

        # 50%
        reencoder = vp8.Vp8_reencoder(crf_range=50)
        assert reencoder.crf == 33

class Test_reencode:
    # No encoder args
    def test_vp8_reencode_call_no_args(self):
        reencoder = vp8.Vp8_reencoder()
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libvpx", "-y", "apple.webm"]
    
    # Only bitrate args
    def test_vp8_reencode_call_bitrate_only(self):
        reencoder = vp8.Vp8_reencoder(bit_rate='1500K')
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libvpx", "-y", "-b", "1500K", "apple.webm"]

    # Only crf
    def test_vp8_reencode_call_crf_only(self):
        reencoder = vp8.Vp8_reencoder(crf_range=50)
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libvpx", "-y", "-crf", "33", "apple.webm"]

    # Only speed
    def test_vp8_reencode_call_speed_only(self):
        reencoder = vp8.Vp8_reencoder(speed='quality')
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libvpx", "-y", "--best", "apple.webm"]

    # Only threads
    def test_vp8_reencode_call_threads_only(self):
        reencoder = vp8.Vp8_reencoder(n_threads=7)
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libvpx", "-y", "-threads", "7", "apple.webm"]

    # Only duration
    def test_vp8_reencode_call_duration_only(self):
        reencoder = vp8.Vp8_reencoder(t_duration=175)
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libvpx", "-y", "-t", "175", "apple.webm"]

    # Only quiet
    def test_vp8_reencode_call_quiet_only(self):
        reencoder = vp8.Vp8_reencoder(quiet=True)
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libvpx", "-y", "-hide_banner", "-loglevel", "error", "apple.webm"]


    # crf 10 (~89.8%), bitrate 750k
    def test_vp8_reencode_call_crf_bitrate(self):
        reencoder = vp8.Vp8_reencoder(bit_rate='750K', crf_range=89.8)
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libvpx", "-y", "-b", "750K", "-crf", "10", "apple.webm"]

    # crf 84% (~10), speed balanced
    def test_vp8_reencode_call_crf_speed(self):
        reencoder = vp8.Vp8_reencoder(speed='balanced', crf_range=88.5)
        call = reencoder._set_reencode_call("banana.mp4", "apple.webm")
        assert call == ["ffmpeg", "-i", "banana.mp4", "-c", "libvpx", "-y", "-crf", "10", "--good", "apple.webm"]
