FROM python:3.10-slim as build

EXPOSE 80

WORKDIR /app

COPY . /app/

RUN pip3 install streamlit

$dependency_install

$custom_input

ENTRYPOINT ["streamlit", "run", "$streamlit_script", "--server.port=80", "--server.address=0.0.0.0"]

FROM build as prod

