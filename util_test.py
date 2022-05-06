import os

def get_file_paths(directory_path,condition):
    return _get_file_attribute(directory_path,condition,need_file_name=False)

def _get_file_attribute(directory_path,condition,need_file_name=False):
  result = []
  for file in os.listdir(directory_path):
            if os.path.isfile(os.path.join(directory_path, file)) and condition(file):
                if need_file_name:
                    result.append(file)
                else:
                    result.append(os.path.join(directory_path, file))
  return result

def get_file_names(directory_path,condition):
    return _get_file_attribute(directory_path,condition,need_file_name=True)