from flask import current_app
from werkzeug.utils import secure_filename
import shutil


def save_to_local(files, directory_path):
    """
    Save files to local storage

    Arguments:
        files {FileStorage} -- Files to be saved
        directory_path {String} -- Directory to save all the files

    Returns:
        Array -- Array of file paths if success else Empty Array
        Array -- Array of file data structure if success else Empty Array
    """
    filepaths = []
    fileDS = []
    try:
        for file in files:
            path = directory_path + "/" + secure_filename(file.filename)
            file.save(path)
            filepaths.append(path)
            fileDS.append(
                {
                    "filename": secure_filename(file.filename),
                    "filetype": file.mimetype,
                    "url": ""
                }
            )
    except Exception as e:
        current_app.logger.error(
            "Failed to save files to tmp directory: " + str(e))
        shutil.rmtree(directory_path)

    return filepaths, fileDS
