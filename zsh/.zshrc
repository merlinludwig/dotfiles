# ~/.zshrc

# --- Completion system ---
fpath+=(/usr/share/zsh/site-functions)
autoload -Uz compinit && compinit

# --- Completion styling (menu, colors, grouping, case-insensitive matching) ---
zmodload zsh/complist
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
zstyle ':completion:*' group-name ''
zstyle ':completion:*:descriptions' format '%F{yellow}-- %d --%f'
zstyle ':completion:*:warnings' format '%F{red}-- no matches found --%f'
zstyle ':completion:*' verbose yes
bindkey -M menuselect '^[[Z' reverse-menu-complete   # shift-tab goes backward

# --- Plugins (installed via pacman) ---
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
source /usr/share/zsh/plugins/zsh-history-substring-search/zsh-history-substring-search.zsh
bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh   # load last

# --- Starship prompt ---
eval "$(starship init zsh)"

# --- History ---
HISTSIZE=10000
SAVEHIST=10000
HISTFILE=~/.zsh_history
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
setopt SHARE_HISTORY
setopt AUTO_CD

# --- Aliases ---
alias ls="ls --color=auto"
alias ll="ls -lah --color=auto"
alias la="ls -A --color=auto"

# --- Editor ---
export EDITOR="vim"

# --- Path ---
export PATH="$HOME/.local/bin:$PATH"
