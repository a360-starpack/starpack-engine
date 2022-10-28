FROM starpack/fastapi-wrapper as build

COPY . /app/models/$name

$dependency_install

$custom_input

FROM build as prod
