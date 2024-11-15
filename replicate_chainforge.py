from chainforge.providers import provider
import replicate

# JSON schemas to pass react-jsonschema-form, one for this provider's settings and one to describe the settings UI.
REPLICATE_SETTINGS_SCHEMA = {
  "settings": {
    "api_key":{
        "type": "string",
        "title": "api_key",
        "description": "Get API key from replicate platform.",
    },
    "model_name":{
        "type": "string",
        "title": "model_name",
        "description": "Get model name from replicate platform.",
    },
    "temperature": {
      "type": "number",
      "title": "temperature",
      "description": "Controls the 'creativity' or randomness of the response.",
      "default": 0.75,
      "minimum": 0,
      "maximum": 5.0,
      "multipleOf": 0.01,
    },
    "max_tokens": {
      "type": "integer",
      "title": "max_tokens",
      "description": "Maximum number of tokens to generate in the response.",
      "default": 100,
      "minimum": 1,
      "maximum": 1024,
    },
  },
  "ui": {
    "api_key": {
        "ui:help": "Get API key from replicate platform.",
        "ui:widget": "password"
        },
    "model_name": {
        "ui:help": "Get model name from replicate platform.",
        "ui:widget": "text"
        },
    "temperature": {
      "ui:help": "Defaults to 1.0.",
      "ui:widget": "range"
    },
    "max_tokens": {
      "ui:help": "Defaults to 100.",
      "ui:widget": "range"
    },
  }
}

# Our custom model provider for Cohere's text generation API.
@provider(name="Replicate",
          emoji="ℾ", 
          rate_limit="sequential", # enter "sequential" for blocking; an integer N > 0 means N is the max mumber of requests per minute. 
          settings_schema=REPLICATE_SETTINGS_SCHEMA)
def ReplicateCompletion(prompt: str, api_key: str, model_name: str, temperature: float = 0.75, **kwargs) -> str:
    # Init the Cohere client (replace with your API key):
    rep = replicate.Client(api_key)

    print(f"Calling Replicate model {model_name} with prompt '{prompt}'...")
    response = rep.run(model_name,
                       input = {
                           "prompt": prompt,
                           "temperature": temperature,
                       })
    return response