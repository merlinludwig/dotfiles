# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# ~/.zshrc

# --- Completion system ---
fpath+=($PREFIX/share/zsh/site-functions)
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
#source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
#source /usr/share/zsh/plugins/zsh-history-substring-search/zsh-history-substring-search.zsh
#bindkey '^[[A' history-substring-search-up
#bindkey '^[[B' history-substring-search-down
#source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh   # load last

# --- Starship prompt ---
#eval "$(starship init zsh)"

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

# --- Powerlevel10k prompt ---
source ~/powerlevel10k/powerlevel10k.zsh-theme

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
