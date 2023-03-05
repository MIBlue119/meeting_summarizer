"""Define the app's configuration.
"""


text_engine_choices = {
    "text-davinci-003": "text-davinci-003",
    "gpt-3.5-turbo": "gpt-3.5-turbo",
}

TEXT_ENGINE = text_engine_choices["gpt-3.5-turbo"]
TEXT_ENGINE_TEMPERATURE = 0.5
LANGUAGE = "zh-tw"
IS_TEST = True
TEST_NUM = 40