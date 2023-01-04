FROM python
WORKDIR /home/
COPY requirements.txt .
COPY .env .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY *.py ./
EXPOSE 80
ENTRYPOINT ["python", "src/index.py"]