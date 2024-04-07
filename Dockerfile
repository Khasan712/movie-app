FROM python:3.11

ENV PYTHONDONTWRITENYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . /uz_movie
WORKDIR /uz_movie
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN adduser uz_movie_user
RUN chown -R uz_movie_user:uz_movie_user /uz_movie
RUN chmod -R 777 /uz_movie/entrypoint.sh
USER uz_movie_user
ENTRYPOINT ["sh", "/uz_movie/entrypoint.sh"]
