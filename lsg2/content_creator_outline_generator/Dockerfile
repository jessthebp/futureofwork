FROM python:3.9

WORKDIR /app

# Copy the files into the image
COPY . .


# Install requirements
RUN pip install -r requirements.txt

# Entrypoint
ENTRYPOINT ["python", "main.py"]