FROM python:3

RUN pip install flask Flask_session requests 

WORKDIR /app/

RUN git clone https://github.com/sanmarg/TicTacToe

RUN mv ./TicTacToe/* /app/ ; rm -rf TicTacToe

EXPOSE 5000

CMD ["python","application.py"]