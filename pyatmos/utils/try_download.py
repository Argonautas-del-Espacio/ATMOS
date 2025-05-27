from py3_wget import download_file


def wget_download(url, dir_file, desc=None):
    """
    Download files by wget command

    Inputs:
        url -> [str]
        dir_file -> [str] output filename or directory
    Parameters:
        desc -> [str] description of the downloading
    Outpits:
        wget_out -> [str] path and filename where URL is downloaded to

    """
    download_file(
        max_tries=100,  # Maximum number of retry attempts
        retry_seconds=2,  # Initial retry delay in seconds
        timeout_seconds=30,
        output_path=dir_file,
        overwrite=True,  # Overwrite existing file
    )
