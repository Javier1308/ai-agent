import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        absolute_path = os.path.abspath(os.path.normpath(os.path.join(working_directory, file_path)))
        absolute_working_path = os.path.abspath(working_directory)
        if os.path.commonpath([absolute_path, absolute_working_path]) != absolute_working_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(absolute_path) != True:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(absolute_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return file_content_string
    
    except Exception as e:
        return f"Error: {e}"
        
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Retrieves the content (at most {MAX_CHARS} characters) of a specified file within the working directory"  ,
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)