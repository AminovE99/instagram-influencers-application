FROM python:3.7.4

# Set environment variables
# Set work directory
WORKDIR /instagram_app
# Copy project
COPY . /instagram_app/
# Install dependencies
RUN pip install -r requirements.txt