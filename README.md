# HFServing
Dockerize HuggingFace model and serve using Flask/Gunicorn

Steps to docekrize:

- Create a virtualenv and activate it. (Replace <env_name> with a name)
```python
  python -m venv <env_name>
  source activate <env_name>
```

- Clone the repository, and be inside the root folder.
```python
  git clone https://github.com/AbinayaM02/HFServing.git
  cd HFServing
```

- Install necessary libraries
```python
  pip install -r requirements.txt
```

- Download the model to a local folder "model". 
Change the name of the model directory in "download_python.py" script and execute the following command,
```python
  python download_model.py
```

- Create docker image using the following command, (replace <image_name> with a name)
```python
  docker build -t <image_name>:latest .
```

- See the created image using the following command, (the image name and details will be displayed)
```python
  docker image
```

- Create container by executing the following command. Replace <cont_name> and <image_name> with the actual names of contianer name and image name respectively, the <cont_port> with the port no. of your choice, and the <host_port> to the port specified in the "config.py"
```python
  docker run -it -p <cont_port>:<host_port> --name <cont_name> <image_name>
```

- Check if the contianer is running by executing,
```python
  docker ps
```

- Change the config for gunicorn as per your need.
```python
# Ignore the files/folders
.git
*cache*
*model*
.dockerignore
Dockerfile
```

- To test the output of the dockerized code, use  the following curl command,
```python
 curl -H "Content-Type: application/json" -X POST -d '{"text":"Elon Musk has shown again he can influence the digital currency market with just his tweets. After saying that electric vehicle-making company Tesla will not accept payments in Bitcoin because of environmental concerns, he tweeted that he was working with developers of Dogecoin to improve system transaction efficiency.", "min_length": 15, "max_length": 75}' http://0.0.0.0:<cont_port>/api/get-summary
```

<br/>
Caveats: 
<br/>
1. There is a limitation to the length of the values that curl can take. This is dependent on the OS. Had issues providing longer texts for summarization. Need to find a solution to solve this.
2. The code detects if the GPU is present or not and sets the device value accordingly. So, the same code can be run on both CPU/GPU.
3. The model is currently part of the container image. So, the image size is 3.35 GB. If this needs to be avoided, the model can be mounted during runtime. To do so, follow the steps,
- Add "model" to the .dockerignore file
- Remove/Comment out the following line from Dockerfile
```python
  # COPY model/distilbart-cnn-12-6 /Summarizer/distilbart-cnn-12-6
```
- Create docker image as specified earlier
- Create container using the following command,
```python 
  docker run -it -p <cont_port>:<host_port> --name <cont_name> -v $HOME/HFServing/model/distilbart-cnn-12-6:/Summarizer/distilbart-cnn-12-6 <image_name>
```
