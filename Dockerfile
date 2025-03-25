FROM python:3.12-slim

# Update package list and install necessary system packages
RUN pip install --upgrade pip setuptools==68.2.0

# Copy your requirements file and set working directory
COPY requirements.txt /app/requirements.txt
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code into the container
COPY . /app

# Expose the port Streamlit will use (default is 8567)
EXPOSE 8567

# Command to run your Streamlit app (adjust the path to your main script)
CMD ["streamlit", "run", "app/main.py", "--server.port=8567", "--server.address=0.0.0.0"] 