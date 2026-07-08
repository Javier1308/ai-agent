import os
from google.genai import types

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))
        valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
        formatted_list = []
        if valid_target_dir != True:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir) != True:
            return f'Error: "{directory}" is not a directory'
        if os.path.isdir(target_dir) == True:
            for item in os.listdir(target_dir):
                if os.path.isdir(os.path.join(target_dir, item)) == True:
                    is_dir = True
                else:
                    is_dir = False
                
                size = os.path.getsize(os.path.join(target_dir, item))

                name = item

                formatted_list.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(formatted_list)

    except Exception as e:
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
