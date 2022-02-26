from libqtile.config import Key
from libqtile.command import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = "alacritty"

keys = [Key(key[0], key[1], *key[2:]) for key in [
    # Switch between windows
    ([mod], "h", lazy.layout.left()),
    ([mod], "l", lazy.layout.right()),
    ([mod], "j", lazy.layout.down()),
    ([mod], "k", lazy.layout.up()),
    ([mod], "space", lazy.layout.next()),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    ([mod, "shift"], "h", lazy.layout.shuffle_left()),
    ([mod, "shift"], "l", lazy.layout.shuffle_right()),
    ([mod, "shift"], "j", lazy.layout.shuffle_down()),
    ([mod, "shift"], "k", lazy.layout.shuffle_up()),


    ([mod, "shift"], "f", lazy.layout.toggle_floating()),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    ([mod, "control"], "h", lazy.layout.shrink()),
    ([mod, "control"], "l", lazy.layout.grow()),
    ([mod], "n", lazy.layout.normalize()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    ([mod, "shift"], "Return", lazy.layout.toggle_split()),
    ([mod], "Return", lazy.spawn(terminal)),

    # Toggle between different layouts as defined below
    ([mod], "Tab", lazy.next_layout()),
    ([mod], "w", lazy.window.kill()),

    # Toggle between diferents screens next_urgent
    ([mod], "Up", lazy.next_screen()),

    ([mod, "control"], "r", lazy.restart()),
    ([mod, "control"], "q", lazy.shutdown()),
    ([mod], "r", lazy.spawncmd()),
    
    # Menu
    ([mod], "m", lazy.spawn("rofi -show drun")),
    ([mod], "s", lazy.spawn("scrot")),
    ([mod], "e", lazy.spawn("nautilus")),
    ([mod], "b", lazy.spawn("google-chrome-stable")),
    ([mod, "shift"], "s", lazy.spawn("flameshot gui")),
    ([], "XF86Calculator", lazy.spawn("kcalc")),

    # Window Nav
    ([mod, "shift"], "m", lazy.spawn("rofi -show")),

    # Volume
    ([], "XF86AudioLowerVolume", lazy.spawn("pamixer --decrease 5")),
    ([], "XF86AudioRaiseVolume", lazy.spawn("pamixer --increase 5")),
    ([], "XF86AudioMute", lazy.spawn("pamixer --toggle-mute")),

    # Music Control
    ([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    ([], "XF86AudioStop", lazy.spawn("playerctl stop")),
    ([], "XF86AudioNext", lazy.spawn("playerctl next")),
    ([], "XF86AudioPrev", lazy.spawn("playerctl previousb")),

    # Brightness
    ([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    ([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
    
]]
