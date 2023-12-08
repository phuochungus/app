FROM python:3.10

RUN apt-get update && apt-get install -y sudo

RUN useradd -m -u 1000 user

USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user requirements.txt .

RUN pip install -r requirements.txt

COPY --chown=user ./packages ./packages

RUN cd packages/rag-redis && pip install -e .

COPY --chown=user . .

EXPOSE 8080

CMD exec uvicorn app.server:app --host 0.0.0.0 --port 8080
