# canvas-synergetic
Synergetic sync with Canvas.

# Environment File
1. Copy the docker-env.env.example file and rename to docker-env.env
2. Fill out necessary details in the docker-env.env file.
3. Build the container using "docker build -t canvas-upload ."
4. Run the container using "docker run -it --rm --env-file docker-env.env --name canvas-upload canvas-upload"
