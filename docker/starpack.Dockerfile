FROM python:3.10 as build

RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade pip

COPY requirements.txt ./
RUN pip install -r requirements.txt

WORKDIR /app/

COPY ./src/engine ./engine
COPY ./src/serve.sh ./serve.sh

CMD ["sh", "serve.sh"]

# TEST SETUP
FROM build as test
COPY ./src/tests ./tests
COPY .coveragerc .pytest.ini codecov.yml ./
RUN pip install -r tests/requirements.txt


FROM build as prod

