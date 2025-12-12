from pydantic import BaseModel, Field

class GetTemperatureArgs(BaseModel):
    city: str = Field(...,
                      description = 'The city to get the temperature for. ' +
                      'Add only the name of the city.')

get_temp_tool_schema = {
    'type': 'function', 
    'function': {
        'name': 'get_temperature',
        'description': 'Get the current temperature in a given city.',
        'parameters': GetTemperatureArgs.model_json_schema()
    }
}
