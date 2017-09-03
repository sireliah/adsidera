
from conf import s, GameSettings


def camera(camx, camy, body, center_on=''):
    """
    Move the camera along with the centered object (rocket).
    """

    if body.name == center_on:
        if (camx + s.pol_szer) - body.x > GameSettings.CAMERA_MARGIN:
            camx = body.x + GameSettings.CAMERA_MARGIN - s.pol_szer
        elif body.x - (camx + s.pol_szer) > GameSettings.CAMERA_MARGIN:
            camx = body.x - GameSettings.CAMERA_MARGIN - s.pol_szer
        if (camy + s.pol_wys) - body.y > GameSettings.CAMERA_MARGIN:
            camy = body.y + GameSettings.CAMERA_MARGIN - s.pol_wys
        elif body.y - (camy + s.pol_wys) > GameSettings.CAMERA_MARGIN:
            camy = body.y - GameSettings.CAMERA_MARGIN - s.pol_wys

    return camx, camy
