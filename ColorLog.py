import os


class ColorLogDecorator:
    """
    class:  ColorLogDecorator
    Desc:   ues for decorate the string with ANSI escape code (color function)

    class_var:
        __IS_ACTIVE: whether the decorate func active
        __DEFAULT_STYLE: the default style for a color selected
        __END_CODE: the end escape code
    """

    __IS_ACTIVE: bool = False
    __DEFAULT_STYLE: str = "normal"
    __COLOR_CODE: dict = {
        "red": {
            "normal": "\033[31m",
            "strong": "\033[1;31m",
            "bg": "\033[0;37;41m",
            "bg-strong": "\033[1;37;41m",
        },
        "green": {
            "normal": "\033[32m",
            "strong": "\033[1;32m",
            "bg": "\033[0;37;42m",
            "bg-strong": "\033[1;37;42m",
        },
        "yellow": {
            "normal": "\033[33m",
            "strong": "\033[1;33m",
            "bg": "\033[0;30;43m",
            "bg-strong": "\033[1;30;43m",
        },
        "blue": {
            "normal": "\033[34m",
            "strong": "\033[1;34m",
            "bg": "\033[0;37;44m",
            "bg-strong": "\033[1;37;44m",
        },
        "black": {
            "normal": "\033[30m",
            "strong": "\033[1;30m",
            "bg": "\033[0;37;40m",
            "bg-strong": "\033[1;37;40m",
        },
        "white": {
            "normal": "\033[37m",
            "strong": "\033[1;37;0m",
            "bg": "\033[0;30;47m",
            "bg-strong": "\033[1;30;47m",
        }
    }
    __END_CODE: str = "\033[0m"

    @classmethod
    def active(cls) -> None:
        """
        active the color decorate function
            it will use a special menthol for windows os
        :return: None
        """
        cls.__IS_ACTIVE = True
        if os.name == "nt":
            os.system("")

    @classmethod
    def deactivate(cls) -> None:
        """
        deactivate the color decorate function
        :return: None
        """
        cls.__IS_ACTIVE = False

    @classmethod
    def __msg_decorator(cls, msg: str, color: str, style: str) -> str:
        """
        use to decorate the msg str with special style color escape code
        :param msg: the msg str
        :param color: the color str to select
        :param style: the style str to select
        :return: decorated str
        """
        if not cls.__IS_ACTIVE:
            return msg

        style_selected: str = cls.__DEFAULT_STYLE if style.lower() not in cls.__COLOR_CODE[color].keys() \
            else style.lower()

        return cls.__COLOR_CODE[color][style_selected] + msg + cls.__END_CODE

    @classmethod
    def red(cls, msg: str, style: str = "normal") -> str:
        """
        red log str
        :param msg: the msg str
        :param style: the style to select
        :return: decorated str
        """
        return cls.__msg_decorator(msg, "red", style)

    @classmethod
    def green(cls, msg: str, style: str = "normal") -> str:
        """
        green log str
        :param msg: the msg str
        :param style: the style to select
        :return: decorated str
        """
        return cls.__msg_decorator(msg, "green", style)

    @classmethod
    def yellow(cls, msg: str, style: str = "normal") -> str:
        """
        yellow log str
        :param msg: the msg str
        :param style: the style to select
        :return: decorated str
        """
        return cls.__msg_decorator(msg, "yellow", style)

    @classmethod
    def blue(cls, msg: str, style: str = "normal") -> str:
        """
        blue log str
        :param msg: the msg str
        :param style: the style to select
        :return: decorated str
        """
        return cls.__msg_decorator(msg, "blue", style)

    @classmethod
    def black(cls, msg: str, style: str = "normal") -> str:
        """
        black log str
        :param msg: the msg str
        :param style: the style to select
        :return: decorated str
        """
        return cls.__msg_decorator(msg, "black", style)

    @classmethod
    def white(cls, msg: str, style: str = "normal") -> str:
        """
        white log str
        :param msg: the msg str
        :param style: the style to select
        :return: decorated str
        """
        return cls.__msg_decorator(msg, "white", style)


