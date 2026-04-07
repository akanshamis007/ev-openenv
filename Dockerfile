FROM python:3.10

WORKDIR /code

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

CMD ["streamlit", "run", "gui.py", "--server.port=7860", "--server.address=0.0.0.0"]