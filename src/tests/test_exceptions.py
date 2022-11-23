from engine import errors


def test_improper_requirements_error():
    error = errors.ImproperRequirementError()

    assert error.status_code == 400


def test_unloaded_plugins_error():
    error = errors.UnloadedPluginError()

    assert error.status_code == 405


def test_missing_input_error():
    example_text = "package"
    error = errors.MissingInputError(example_text)

    assert error.status_code == 400
    assert example_text in error.detail
