FROM python:3.7

MAINTAINER Abinaya Mahendiran "abinaya.m02@mphasis.com"

# Define volume
VOLUME /Summarizer

# Set the working directory
WORKDIR /Summarizer

RUN apt-get -y update && apt-get install -y --no-install-recommends \
        && rm -rf /var/lib/apt/lists/*

# Copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt /Summarizer/.

# Install packages
RUN pip install -r requirements.txt && \
        rm -rf /root/.cache 

# Copy only the necessary folders/files
COPY config.py /Summarizer/.
COPY summarization.py /Summarizer/.
RUN mkdir distilbart-cnn-12-6
COPY model/distilbart-cnn-12-6 /Summarizer/distilbart-cnn-12-6

# Specify the command
CMD ["gunicorn", "-c", "/Summarizer/config.py", "summarization:app"]
