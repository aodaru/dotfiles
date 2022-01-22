# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from settings.keys import mod, keys

from os import path
import subprocess
import psutil
import socket

@hook.subscribe.startup_once
def autostart():
    init = path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([init])

def check_interface(interface):
    interface_addrs = psutil.net_if_addrs().get(interface) or []
    return socket.AF_INET in [snicaddr.family for snicaddr in interface_addrs]

if check_interface("enp2s0"):
    net_connect = "enp2s0"

if check_interface("wlp3s0"):
    net_connect = "wlp3s0"

def base(fg='#ffffff', bg='#2d2a2e'): 
    return {
        'foreground': [fg,fg],
        'background': [bg,bg]
    }

def powerline(fg="#ffffff", bg="#2d2a2e"):
    return widget.TextBox(
        **base(fg, bg),
        text="", # Icon: nf-oct-triangle_left
        fontsize=37,
        padding=-3
    )

def powerlineright(fg="#ffffff", bg="#2d2a2e"):
    return widget.TextBox(
        **base(fg, bg),
        text="", # Icon: nf-oct-triangle_left
        fontsize=37,
        padding=-3
    )

def icon(fg='#2d2a2e', bg='#2d2a2e', fontsize=16, text="?"):
    return widget.TextBox(
        **base(fg, bg),
        fontsize=fontsize,
        text=text,
        padding=3
    )


groups = [Group(i) for i in [
    " ", " ", " "," "," "," "
]]

for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])

layout_conf = {
    'border_focus': '#8ae331',
    'border_width': 1,
    'margin': 4
}

layouts = [
    layout.Max(),
    layout.MonadTall(**layout_conf),
    layout.MonadWide(**layout_conf),
]

widget_defaults = dict(
    font='UbuntuMono Nerd Font',
    fontsize=14,
    padding=0,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    foreground=["#ffffff", "#ffffff"],
                    background=["#565456", "#565456"],
                    font='UbuntuMono Nerd Font',
                    fontsize=16,
                    margin_y=0,
                    margin_x=0,
                    padding_y=4,
                    padding_x=12,
                    borderwidth=1,
                    center_aligned =False,
                    active=["#ffffff", "#ffffff"],
                    inactive=["#727072","#727072"],
                    rounded=False,
                    highlight_method='block',
                    urgent_alert_method='block',
                    urgent_border=["#ff6188","#ff6188"],
                    this_current_screen_border=["#a9dc76","#a9dc76"],
                    this_screen_border=["#a9dc76","#a9dc76"],
                    other_current_screen_border=["#424042", "#424042"],
                    other_screen_border=["#424042", "#424042"],
                    disable_drag=True
                ),
                powerlineright('#565456','#2d2a2e'),
                widget.Sep(
                    linewidth=0,
                    padding=5,
                    background=["#2d2a2e","#2d2a2e"]
                ),
                widget.Prompt(),
                widget.WindowName(
                    foreground=["#a9dc76","#a9dc76"],
                    background=["#2d2a2e", "#2d2a2e"],
                    fontsize=14,
                    font='UbuntuMono Nerd Font Bold',
                ),
                powerline('#F4FE53','#2d2a2e'),
                icon(bg="#F4FE53", text=' ',fontsize=12), # Icon: nf-fa-download
                widget.CheckUpdates(
                    background='#F4FE53',
                    colour_have_updates='#FE7053',
                    colour_no_updates='#2d2a2e',
                    no_update_string='0',
                    display_format='{updates}',
                    update_interval=60,
                    fontsize=11
                ),
                widget.Sep(
                    linewidth=0,
                    padding=5,
                    background=["#F4FE53","#F4FE53"]
                ),
                powerline('#feaf57','#F4FE53'),
                icon(bg="#feaf57", text=' ',fontsize=12),  # Icon: nf-fa-feed
                widget.Net(
                    **base("#2d2a2e","#feaf57"),
                    interface=net_connect,
                    format='{down} ↓↑{up}',
                    fontsize=11,
                    markup=True
                ),
                widget.Sep(
                    linewidth=0,
                    padding=5,
                    background=["#feaf57","#feaf57"]
                ),
                powerline('#3895ff','#feaf57'),
                widget.CurrentLayoutIcon(
                    foreground=["#2d2a2e", "#2d2a2e"],
                    background=["#3895ff","#3895ff"],
                    scale=0.65
                ),
                widget.CurrentLayout(
                    foreground=["#2d2a2e", "#2d2a2e"],
                    background=["#3895ff","#3895ff"],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=5,
                    background=["#3895ff","#3895ff"]
                ),
                powerline('#a9dc76','#3895ff'),
                icon(bg="#a9dc76", fontsize=14, text=' '), # Icon: nf-mdi-calendar_clock
                widget.Clock(
                    background=["#a9dc76","#a9dc76"],
                    foreground=["#2d2a2e", "#2d2a2e"],
                    format='%d/%m/%Y %H:%M ',
                    fontsize=14
                ),
                powerline("#565456","#a9dc76"),
                widget.Systray(
                    foreground=["#FAF9F7", "#FAF9F7"],
                    background=["#565456", "#565456"]
                ),
                # widget.QuickExit(),
            ],
            26,
        ),
    ),

    # Second Screen
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    foreground=["#ffffff", "#ffffff"],
                    background=["#2d2a2e", "#2d2a2e"],
                    font='UbuntuMono Nerd Font',
                    fontsize=16,
                    margin_y=3,
                    margin_x=0,
                    padding_y=8,
                    padding_x=10,
                    borderwidth=1,
                    active=["#ffffff", "#ffffff"],
                    inactive=["#727072","#727072"],
                    rounded=False,
                    highlight_method='block',
                    urgent_alert_method='block',
                    urgent_border=["#ff6188","#ff6188"],
                    this_current_screen_border=["#a9dc76","#a9dc76"],
                    this_screen_border=["#5a565b","#5a565b"],
                    other_current_screen_border=["#2d2a2e", "#2d2a2e"],
                    other_screen_border=["#2d2a2e", "#2d2a2e"],
                    disable_drag=True
                ),
                widget.Sep(
                    linewidth=0,
                    padding=5,
                    background=["#2d2a2e","#2d2a2e"]
                ),
                widget.Prompt(),
                widget.WindowName(
                    foreground=["#a9dc76","#a9dc76"],
                    background=["#2d2a2e", "#2d2a2e"],
                    fontsize=14,
                    font='UbuntuMono Nerd Font Bold',
                ),
                powerline('#3895ff','#2d2a2e'),
                widget.CurrentLayoutIcon(
                    foreground=["#2d2a2e", "#2d2a2e"],
                    background=["#3895ff","#3895ff"],
                    scale=0.65
                ),
                widget.CurrentLayout(
                    foreground=["#2d2a2e", "#2d2a2e"],
                    background=["#3895ff","#3895ff"],
                ),
            ],
            26,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
], border_focus='#a9dc76')
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
