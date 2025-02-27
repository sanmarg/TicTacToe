FROM python:3

# Install required Python dependencies
RUN pip install flask Flask_session requests \
    opentelemetry-sdk opentelemetry-instrumentation-flask \
    opentelemetry-exporter-jaeger

WORKDIR /app/

# Clone and setup TicTacToe application
RUN git clone https://github.com/sanmarg/TicTacToe
RUN mv ./TicTacToe/* /app/ && rm -rf TicTacToe

EXPOSE 5000

# Start the application with OpenTelemetry
CMD ["opentelemetry-instrument", "python", "application.py"]
