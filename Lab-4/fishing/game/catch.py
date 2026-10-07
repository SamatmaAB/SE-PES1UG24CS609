"""
catch: hook-vs-fish catch detection.
"""


def check_catch(hook, fish_list):
    """
    Returns the fish the hook has caught, or None.
    Checks actual rectangle overlap between hook and fish, not just depth.
    """
    hook_rect = hook.get_rect()
    for fish in fish_list:
        fish_rect = fish.get_rect()
        if hook_rect.colliderect(fish_rect):
            return fish
    return None
