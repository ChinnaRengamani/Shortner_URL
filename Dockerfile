FROM python:3.10

RUN apt-get -qq update --fix-missing && apt-get -qq upgrade -y && apt-get install git -y
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
  PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

RUN pip install --no-cache-dir --upgrade pip
COPY --chown=user . $HOME/app


RUN pip install --no-cache-dir -r requirements.txt

CMD python3 app.py
