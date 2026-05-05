setopt prompt_subst
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
autoload bashcompinit && bashcompinit
autoload -Uz compinit
compinit

# export TMUX_FZF_LAUNCH_KEY="F"
export TERM=xterm-256color
# Ollama
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_CONTEXT_LENGTH=16384


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
alias macup="docker compose -f ~/.config/mac/docker-compose.yml up -d"
alias macdown="docker compose -f ~/.config/mac/docker-compose.yml down"
# alias wg0up="_ wg-quick up wg0"
# alias wg0down="_ wg-quick down wg0"
alias pi="source /home/agarcia/pi-vs-claude-code/.env && /home/agarcia/.local/share/pnpm/pi"
alias q="pi --model big-pickle -p"

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
alias fjr="xfreerdp3 /u:agarcia /v:satcom1901.tail1a17f4.ts.net /gfx:AVC420:on /compression /network:auto -themes -wallpaper /dynamic-resolution /sec:tls +f"

# Función para activar el enrutamiento de la VPN
vpn_on() {
    echo "🚀 Activando enrutamiento VPN..."
    
    # 1. Regla de Forward en el Host
    sudo iptables -I FORWARD 1 -s 10.0.64.0/24 -d 172.17.32.0/24 -j ACCEPT
    sudo iptables -I FORWARD 1 -s 10.0.64.0/24 -d 172.30.30.0/24 -j ACCEPT
    
    # 2. Regla de SNAT en el Host
    sudo iptables -t nat -A POSTROUTING -s 10.0.64.0/24 -d 172.17.32.0/24 -j SNAT --to-source 10.212.138.98
    sudo iptables -t nat -A POSTROUTING -s 10.0.64.0/24 -d 172.30.30.0/24 -j SNAT --to-source 10.212.138.98
    
    # 3. Ruta en la VM Windows (vía Docker)
    # Nota: Usamos cmd /c para ejecutar el comando de Windows dentro del contenedor
    echo "ejecutar en windows: route add 172.17.32.0 mask 255.255.255.0 10.0.64.1"
    echo "ejecutar en windows: route add 172.30.30.0 mask 255.255.255.0 10.0.64.1"
    
    echo "✅ Configuración aplicada."
}

# Función para desactivar el enrutamiento
vpn_off() {
    echo "🛑 Desactivando enrutamiento VPN..."
    
    # 1. Borrar regla de Forward
    sudo iptables -D FORWARD -s 10.0.64.0/24 -d 172.17.32.0/24 -j ACCEPT
    sudo iptables -D FORWARD -s 10.0.64.0/24 -d 172.30.30.0/24 -j ACCEPT
    
    # 2. Borrar regla de SNAT
    sudo iptables -t nat -D POSTROUTING -s 10.0.64.0/24 -d 172.30.30.0/24 -j SNAT --to-source 10.212.138.98
    
    echo "ejecutar en windows: route delete 172.17.32.0 mask 255.255.255.0 10.0.64.1"
    echo "ejecutar en windows: route delete 172.30.30.0 mask 255.255.255.0 10.0.64.1"
    
    echo "🧹 Limpieza completada."
}

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
eval "$(mise activate zsh)"
