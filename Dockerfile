FROM python:3.10

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 7860

# Run Streamlit GUI automatically
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]