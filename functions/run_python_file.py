import os
import subprocess
from google.genai import types

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        absolute_path = os.path.abspath(os.path.normpath(os.path.join(working_directory, file_path))) # ruta absoluta del archivo a modificar
        absolute_working_path = os.path.abspath(working_directory) # ruta permitida
        parent_dir = os.path.dirname(absolute_path) # ruta absoluta a la carpeta del archivo a modificar

        if os.path.commonpath([absolute_working_path, absolute_path]) != absolute_working_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(absolute_path) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if absolute_path.endswith('.py') == False:
            return f'Error: "{file_path}" is not a Python file'
        
        output = ""
        command = ["python", absolute_path]
        if args is not None:
            command.extend(args)

        completed_object = subprocess.run(command, cwd=absolute_working_path, capture_output=True   , text=True, timeout=30)

        if completed_object.returncode != 0:
            output += f"Process exited with code {completed_object.returncode}"
        if completed_object.stdout == "" and completed_object.stderr == "": 
            output += "No output produced"
        else:
            output += f"STDOUT: {completed_object.stdout}\nSTDERR: {completed_object.stderr}"
        
        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file within the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of arguments to pass to the Python script",
            ),
        },
        required=["file_path"]
    ),
)