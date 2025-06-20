import os
import shutil

class CommandError(ValueError): pass

modloaders: tuple[str, str, str, str] = "fabric", "forge", "neoforge", "quilt"

minecraft_versions: set[str] = {
    "1.0.0", "1.0.1",
    "1.1",
    "1.2.1", "1.2.2", "1.2.3", "1.2.4", "1.2.5",
    "1.3.1", "1.3.2",
    "1.4.2", "1.4.4", "1.4.5", "1.4.6", "1.4.7",
    "1.5.1", "1.5.2",
    "1.6.1", "1.6.2", "1.6.4",
    "1.7.2", "1.7.4", "1.7.5", "1.7.6", "1.7.7", "1.7.8", "1.7.9", "1.7.10",
    "1.8", "1.8.1", "1.8.2", "1.8.3", "1.8.4", "1.8.5", "1.8.6", "1.8.7", "1.8.8", "1.8.9",
    "1.9", "1.9.1", "1.9.2", "1.9.3", "1.9.4",
    "1.10", "1.10.1", "1.10.2",
    "1.11", "1.11.1", "1.11.2",
    "1.12", "1.12.1", "1.12.2",
    "1.13", "1.13.1", "1.13.2",
    "1.14", "1.14.1", "1.14.2", "1.14.3", "1.14.4",
    "1.15", "1.15.1", "1.15.2",
    "1.16", "1.16.1", "1.16.2", "1.16.3", "1.16.4", "1.16.5",
    "1.17", "1.17.1",
    "1.18", "1.18.1", "1.18.2",
    "1.19", "1.19.1", "1.19.2", "1.19.3", "1.19.4",
    "1.20", "1.20.1", "1.20.2", "1.20.3", "1.20.4", "1.20.5", "1.20.6",
    "1.21", "1.21.1", "1.21.2", "1.21.3", "1.21.4", "1.21.5"
}


class MetaSingleton(type):
    __instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances.keys():
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


def get_text_editor() -> str:
    text_editors: tuple[str] = [i for i in (os.environ.get('EDITOR'), 'nano', 'vim', 'notepad') if i if shutil.which(i)]
    if not text_editors:
        raise ValueError("could not find a text editor")
    else:
        return text_editors[0]


if __name__ == '__main__':
    pass