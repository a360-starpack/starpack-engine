from engine.plugins.package_fastapi.main import package
from engine.schemas.payloads import StarpackInput
from yaml import load, Loader


with open("/home/irvin/A360/starpack-engine/src/starpack.yaml") as file:
    starpack_yaml = load(file, Loader=Loader)


test_input = StarpackInput.parse_obj(starpack_yaml)

package_input = test_input.package


image = package(package_input.artifacts, package_input.metadata)

print(image)
