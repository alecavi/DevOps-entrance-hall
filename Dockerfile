FROM python
WORKDIR /home/
COPY requirements.txt .
COPY .env .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY src/*.py ./
EXPOSE 80
ENTRYPOINT ["python", "src/routes.py"]