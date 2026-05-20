set dotenv-load

build-worker:
    cat .gitignore >> .dockerignore && docker build -t mpd-downloader-worker -f images/worker.Dockerfile .

run-worker TASK_QUEUE:
    docker run \
        -e TEMPORAL_HOST=host.docker.internal:7233 \
        -e TASK_QUEUE={{ TASK_QUEUE }} \
        -e CLEARKEY_ID={{ env("CLEARKEY_ID") }} \
        -e CLEARKEY_VALUE={{ env("CLEARKEY_VALUE") }} \
        -v ./mpds:/app/mpds \
        -v ./segments:/app/segments \
        -v ./videos:/app/videos \
        mpd-downloader-worker
