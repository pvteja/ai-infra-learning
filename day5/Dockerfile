# Stage 1: builder
FROM python:3.12-slim AS builder
WORKDIR /code
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: final
FROM python:3.12-slim
WORKDIR /code
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN useradd --create-home appuser
ENV APP_NAME="AI Infra Lab" ENVIRONMENT=dev
RUN mkdir /data && chown appuser:appuser /data
COPY app ./app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]