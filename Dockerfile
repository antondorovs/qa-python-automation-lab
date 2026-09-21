FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY tests/ ./tests/
COPY data/ ./data/
RUN python -m pip install --no-cache-dir -e '.[test]'

CMD ["python", "-m", "pytest", "-m", "not ui"]
