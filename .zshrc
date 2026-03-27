setopt prompt_subst
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
autoload bashcompinit && bashcompinit
autoload -Uz compinit
compinit

# export TMUX_FZF_LAUNCH_KEY="F"
export TERM=xterm-256color

source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
bindkey '^w' autosuggest-execute
bindkey '^e' autosuggest-accept
bindkey '^u' autosuggest-toggle
bindkey '^L' vi-forward-word
bindkey '^k' up-line-or-search
bindkey '^j' down-line-or-search

bindkey -v
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/agarcia/.zshrc'
# remove ls highlight color
_ls_colors=":ow=01;33" 
zstyle ':completion:*'  list-colors '=*=90'
LS_COLORS+=$_ls_colors


# alias
#
alias cat=bat

alias l="eza -l --icons --git -a"
alias lt="eza --tree --level=2 --long --icons --git"
alias ltree="eza --tree --level=2  --icons --git"
alias ls="eza --long -b --icons=auto --sort=modified --reverse -h --color-scale all --color-scale-mode=gradient"
alias ll="eza --long -b --icons=auto --sort=modified --reverse -h --color-scale all --color-scale-mode=gradient"
alias la="eza --long -b --icons=auto --sort=modified --reverse -h --color-scale all --color-scale-mode=gradient -a"
alias winup="docker compose -f ~/.config/windows/docker-compose-aod.yml up -d"
alias windown="docker compose -f ~/.config/windows/docker-compose-aod.yml down"
alias wg0up="_ wg-quick up wg0"
alias wg0down="_ wg-quick down wg0"

# Dirs
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias .....="cd ../../../.."
alias ......="cd ../../../../.."
alias _="sudo"

alias tson="_ tailscale set --exit-node=100.106.174.104"
alias tson2="_ tailscale set --exit-node=100.108.183.101"
alias tsoff="_ tailscale set --exit-node="
alias fjr="xfreerdp3 /u:agarcia /v:satcom1901.tail1a17f4.ts.net /gfx:AVC420:on /compression /network:auto -themes -wallpaper /sec:tls +f"

# bun completions
[ -s "/home/agarcia/.bun/_bun" ] && source "/home/agarcia/.bun/_bun"

# bun
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

# pnpm
export PNPM_HOME="/home/agarcia/.local/share/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac
# pnpm end
export PATH="$HOME/.local/bin:$PATH"

. "$HOME/.atuin/bin/env"

### FZF ###
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow'
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
export FZF_CTRL_R_COMMAND=""
export FZF_DEFAULT_COMMAND='fd --type f --strip-cwd-prefix'

# To apply the command to CTRL-T as well
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"


# navigation
cx() { cd "$@" && l; }
fcd() { cd "$(find . -type d -not -path '*/.*' | fzf)" && l; }
f() { echo "$(find . -type f -not -path '*/.*' | fzf)" | pbcopy }
fv() { nvim "$(find . -type f -not -path '*/.*' | fzf)" }

eval "$(atuin init zsh --disable-up-arrow)"
eval "$(zoxide init zsh)"
source <(fzf --zsh)   
eval "$(starship init zsh)"
export STARSHIP_CONFIG=~/.config/starship.toml
export LANG=en_US.UTF-8
