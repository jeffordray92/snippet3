# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install the Functions Framework
RUN pip install functions-framework

# Make port 8080 available to the world outside this container
EXPOSE 8081

# Run the Functions Framework when the container launches
CMD ["functions-framework", "--target=scheduled_stream", "--port=8080"]
