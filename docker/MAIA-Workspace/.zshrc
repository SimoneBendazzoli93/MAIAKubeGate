# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi
# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH
# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"
# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
#ZSH_THEME="robbyrussell"
ZSH_THEME="powerlevel10k/powerlevel10k"
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
source $ZSH/oh-my-zsh.sh
# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

run-parts /etc/update-motd.d

# Load K8s env vars from a container PID
load_k8s_env() {
  local pid=$1
  if [[ -z "$pid" ]]; then
    echo "Usage: load_k8s_env <container-pid>"
    return 1
  fi

  if [[ ! -r "/proc/$pid/environ" ]]; then
    echo "Cannot read /proc/$pid/environ. Do you have permissions?"
    return 1
  fi

  # Safely export KUBERNETES_* env vars
  while IFS='=' read -r key value; do
    [[ $key == KUBERNETES_* ]] && export "$key=$value"
  done < <(tr '\0' '\n' < "/proc/$pid/environ")

  echo "Kubernetes env vars loaded from PID $pid"
}

load_k8s_env 1