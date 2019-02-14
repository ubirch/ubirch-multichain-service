
FROM python:3.6

LABEL description="ubirch's MultiChain anchoring service"


WORKDIR /multichain-service/

COPY requirements.txt /multichain-service/
RUN pip install -r requirements.txt

COPY ubirch-multichain-service/multichain_service.py /multichain-service/
COPY start.sh /multichain-service/
RUN chmod +x ./start.sh


ENV LOGLEVEL="DEBUG"

CMD ["./start.sh"]