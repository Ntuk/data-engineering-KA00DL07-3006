FROM python:3.11-slim

# Working dir in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit script into the container
COPY scripts/task09_streamlit_population.py ./streamlit_population.py

# Copy data file into the same directory
COPY data/population_country_columns/population_country_columns.csv ./population_country_columns.csv

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_population.py", "--server.port=8501", "--server.address=0.0.0.0"]
