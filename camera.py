
from conf import s, GameSettings


def camera(camx, camy, body, center_on=''):
    """
    Move the camera along with the centered object (rocket).
    """

    if body.name == center_on:
        if (camx + s.half_width) - body.x > GameSettings.CAMERA_MARGIN:
            camx = body.x + GameSettings.CAMERA_MARGIN - s.half_width
        elif body.x - (camx + s.half_width) > GameSettings.CAMERA_MARGIN:
            camx = body.x - GameSettings.CAMERA_MARGIN - s.half_width
        if (camy + s.half_height) - body.y > GameSettings.CAMERA_MARGIN:
            camy = body.y + GameSettings.CAMERA_MARGIN - s.half_height
        elif body.y - (camy + s.half_height) > GameSettings.CAMERA_MARGIN:
            camy = body.y - GameSettings.CAMERA_MARGIN - s.half_height

    return camx, camy
