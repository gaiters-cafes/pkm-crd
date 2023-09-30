FROM python:3.8.3-alpine

Run git clone git@gitlab.com:phoneybadger/pokemon-colorscripts.git /app; \
    cd /app/; \
    ls; \
    ./install.sh

RUN ln -sf /dev/stdout /var/log/pokemon.log \
	&& ln -sf /dev/stderr /var/log/pokemon_error.log

CMD ["pokemon-colorscripts"]