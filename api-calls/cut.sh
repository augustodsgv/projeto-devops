curl -X POST \
	localhost:7000/cut \
	--json '{
		"video_path":"/data/video.mp4",
		"video_begin":3,
		"video_end":15
		}'
