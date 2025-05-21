FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn pymongo python-jose passlib[bcrypt] email-validator

CMD ["uvicorn", "users_service:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
