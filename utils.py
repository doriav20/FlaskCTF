import base64
import random
import subprocess

from constants import IS_ADMIN_EXECUTABLE


def get_random_filename(k: int, extension: str = '') -> str:
    """
    Generate a random filename with a specified length and optional extension.

    Parameters
    ----------
    k : int
        Length of the random stem to generate.
    extension : str, optional
        File extension to append to the filename (default is an empty string).

    Returns
    -------
    str
        A random filename consisting of a stem of length `k` and an optional extension.
    """

    stem = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=k))
    if extension:
        return stem + '.' + extension
    else:
        return stem


def is_admin(user: str) -> bool:
    """
    Check if the given user is an admin.

    This function uses an external executable to determine if the user has admin privileges.

    Parameters
    ----------
    user : str
        The username to check for admin privileges.

    Returns
    -------
    bool
        True if the user is an admin, False otherwise.
    """

    if not user:
        return False

    try:
        result = subprocess.run([IS_ADMIN_EXECUTABLE, user], capture_output=True)
        return result.returncode == 1
    except:
        return False


def obfuscate_string(s: str) -> str:
    b64_encoded = base64.b64encode(s.encode()).decode()
    reversed_str = b64_encoded[::-1]
    hex_encoded = reversed_str.encode().hex()
    return hex_encoded
