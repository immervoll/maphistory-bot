FROM python:3.9.7

LABEL Maintainer="Immervoll - github.com/immervoll"

ENV TOKEN="TOKENHERE"
ENV PREFIX="!"
ENV IP="IPHERE"
ENV PORT=27165

WORKDIR /usr/src/maphistory-bot/

COPY ./ ./
RUN pip install -r ./requirements.txt

CMD [ "python", "./main.py" ]
