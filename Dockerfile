FROM python:3.10

WORKDIR /home/app

RUN apt install curl -y

RUN curl -fsSL https://get.deta.dev/cli.sh | sh
RUN pip install pandas numpy streamlit matplotlib plotly openpyxl
COPY . /home/app

CMD streamlit run --server.port $PORT main.py

# docker run -it -v "$(pwd):/home/app" -e PORT=80 -p 4000:80 bloc_5 