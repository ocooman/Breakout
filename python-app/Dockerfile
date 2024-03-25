FROM registry.access.redhat.com/ubi8/python-39
WORKDIR /app
COPY python-app/requirements.txt .
RUN pip install --no-cache-dir -r python-app/requirements.txt
COPY . .
EXPOSE 5000
# ENV FLASK_ENV=production
CMD ["python", "python-app/app.py"]