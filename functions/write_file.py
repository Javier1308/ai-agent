import os
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        absolute_path = os.path.abspath(os.path.normpath(os.path.join(working_directory, file_path)))
        absolute_working_path = os.path.abspath(working_directory)
        if os.path.commonpath([absolute_path, absolute_working_path]) != absolute_working_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if  os.path.isdir(absolute_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(absolute_path), exist_ok=True)

        with open(absolute_path, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text content to a specified file within the working directory (overwriting if the file exists)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write to the file",
            ),
        },
        required=["file_path", "content"]
    ),
)