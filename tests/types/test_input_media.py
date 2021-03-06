from aiogram import types

from .dataset import ANIMATION, AUDIO, DOCUMENT, PHOTO, VIDEO

WIDTH = "width"
HEIGHT = "height"

input_media_audio = types.InputMediaAudio(types.Audio(**AUDIO))
input_media_animation = types.InputMediaAnimation(types.Animation(**ANIMATION))
input_media_document = types.InputMediaDocument(types.Document(**DOCUMENT))
input_media_video = types.InputMediaVideo(types.Video(**VIDEO))
input_media_photo = types.InputMediaPhoto(types.PhotoSize(**PHOTO))


def test_field_width():
    """
    https://core.telegram.org/bots/api#inputmedia
    """
    if hasattr(input_media_audio, WIDTH):
        raise AssertionError
    if hasattr(input_media_document, WIDTH):
        raise AssertionError
    if hasattr(input_media_photo, WIDTH):
        raise AssertionError

    if not hasattr(input_media_animation, WIDTH):
        raise AssertionError
    if not hasattr(input_media_video, WIDTH):
        raise AssertionError


def test_field_height():
    """
    https://core.telegram.org/bots/api#inputmedia
    """
    if hasattr(input_media_audio, HEIGHT):
        raise AssertionError
    if hasattr(input_media_document, HEIGHT):
        raise AssertionError
    if hasattr(input_media_photo, HEIGHT):
        raise AssertionError

    if not hasattr(input_media_animation, HEIGHT):
        raise AssertionError
    if not hasattr(input_media_video, HEIGHT):
        raise AssertionError
