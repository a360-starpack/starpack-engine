FROM starpack/fastapi-wrapper as build

COPY . /app/models/test_package

RUN pip install -r /app/models/test_package/requirements.txt



FROM build as prod
