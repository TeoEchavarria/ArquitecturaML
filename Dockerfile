# Use an official Python image that includes the needed libraries
FROM python:3.12-slim

# Install libstdc++6 (and other necessary system packages)
RUN apt-get update && apt-get install -y libstdc++6

# Copy your requirements file and install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code into the container
COPY . /app

# Expose the port Streamlit will use (default is 8567)
EXPOSE 8567

# Command to run your Streamlit app (adjust the path to your main script)
CMD ["streamlit", "run", "app/main.py", "--server.port=8567", "--server.address=0.0.0.0"] 