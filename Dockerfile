FROM base-image-debian-chrome:1.0.0

LABEL org.label-schema.license="GPL-2.0" \ 
 maintainer="Nome"

ENV BASE_NAME project_name
ENV API_NAME project_name

COPY ./config/requirements.txt requirements.txt
COPY ./config/kubernetes/* /config/
COPY ./config/resources/* /
COPY ./config/certs/* /certs/
COPY ./config/prompt/* /prompt/
COPY ./config/uat-test/* /uat-test/

RUN chmod +x ./system_config.sh ./py_config.sh \
 && /system_config.sh \
 && /py_config.sh \
 && cat /certs/root.pem >> /etc/ssl/certs/ca-certificates.crt \
 && cat /certs/intermediate.pem >> /etc/ssl/certs/ca-certificates.crt \
 && cat /certs/uat-intermediate.pem >> /etc/ssl/certs/ca-certificates.crt \
 && cat /certs/root-litellm.pem >> /usr/local/lib/python3.9/dist-packages/certifi/cacert.pem \
 && cat /certs/uat-intermediate.pem >> /usr/local/lib/python3.9/dist-packages/certifi/cacert.pem

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV NEW_RELIC_LABELS 'CRITICIDADE:BAIXO;PRODUTO:RPA;SQUAD:GOVERNANCA'

COPY ./src/ /src/

CMD ["python", "-m", "src.py.main"]