run:
	docker run -i -d -e PORT=5000 -e DJANGO_SETTINGS_MODULE=base.settings -e HAVELOG="--log-file-" -p 192.168.10.73:8002:5000 engine/djangoapp

