curl -X GET \
	localhost:7000/download \
	--json '{
		"video_name":"batata.mp4"
		}' \
	--output batata.mp4
