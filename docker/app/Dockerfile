#Grab the latest alpine image
FROM  python:stretch

COPY . /app
WORKDIR /app

# Install package dependecies
RUN pip install -r requirements.txt

# Install our software is an package
RUN pip install -e .

# ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:$PORT", "whitebearbake:run"] 
# CMD gunicorn --bind 127.0.0.1:$PORT whitebearbake.run:app
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "whitebearbake.run:app"]
