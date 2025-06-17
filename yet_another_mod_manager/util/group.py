from yet_another_mod_manager.config import ModGroup
from yet_another_mod_manager.util import minecraft_versions, modloaders

def is_valid_group(group: ModGroup, no_loader: bool = False) -> tuple[bool, str]:
    """
    Checks the validity of a group.
    :param group: Verified group
    :param no_loader: if True, the function will consider a group w/o a mod_loader valid
    :return: (True, "") if the group is valid else (False, <message>)
    """
    if group.version.strip() not in minecraft_versions:
        return False, f"version '{group.version}' is not valid"

    if (not no_loader) and group.mod_loader.strip() not in modloaders:
        return False, f"only valid mod loaders are {modloaders}, not '{group.mod_loader}'"

    return True, ""