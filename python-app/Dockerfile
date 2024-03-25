FROM registry.access.redhat.com/ubi8/python-39
WORKDIR /app/python-app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
# ENV FLASK_ENV=production
CMD ["python", "app.py"]