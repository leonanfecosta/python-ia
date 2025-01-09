def set_light_values(brightness: int, color_temperature: str) -> dict:
    """
    Set the light values for brightness and color temperature.

    Args:
        brightness (int): The brightness level of the light.
        color_temperature (str): The color temperature of the light.

    Returns:
        dict: A dictionary containing the brightness and color temperature values.
    """
    return {"brightness": brightness, "color_temperature": color_temperature}


def intruder_alert() -> dict:
    """
    Activates an intruder alert.

    Returns:
        dict: A dictionary containing the alert message.
    """
    return {"alert": "Intruder alert activated"}


def start_music(energetic: bool, loud: bool, tempo: int) -> dict:
    """
    Starts music with the specified characteristics.

    Args:
        energetic (bool): Indicates if the music should be energetic.
        loud (bool): Indicates if the music should be loud.
        tempo (int): The tempo of the music.

    Returns:
        dict: A dictionary containing the music characteristics.
    """
    return {"energetic": energetic, "loud": loud, "tempo": tempo}


def good_morning() -> dict:
    """
    Initiates the good morning routine.

    Returns:
        dict: A dictionary containing a message indicating the good morning routine has started.
    """
    return {"routine": "Good morning routine started"}


__all__ = ["set_light_values", "intruder_alert", "start_music", "good_morning"]
