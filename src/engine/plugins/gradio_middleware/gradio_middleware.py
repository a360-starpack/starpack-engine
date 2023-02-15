from ...schemas.payloads import Metadata, Artifacts


def inject_gradio(artifacts: Artifacts, metadata: Metadata, custom_input: str = ""):
    gradio_script_name = artifacts.gradio_script_name
    gradio_interface_name = artifacts.gradio_interface_name

    new_input = f"""
    ENV GRADIO_LOCATION={metadata.name}.{gradio_script_name}
    ENV GRADIO_APP_NAME={gradio_interface_name}
    """

    print(new_input)

    if not custom_input:
        custom_input = ""

    return {"custom_input": custom_input + new_input}
