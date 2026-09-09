#!/bin/bash
# Update MAIA workspace user credentials from $HOME/.env.
#
# Supported keys:
#   MAIA_USERNAME - desired Linux username for the workspace user
#   MAIA_PASSWORD - desired Linux password for the workspace user

set +e

DEFAULT_USER="maia-user"
ENV_FILE="${HOME}/.env"
SUDOERS_FILE="/etc/sudoers.d/maia-workspace-user"

log_info() {
    echo "[INFO] $1"
}

log_error() {
    echo "[ERROR] $1" >&2
}

read_env_var() {
    local key="$1"
    local line
    local value

    while IFS= read -r line || [ -n "$line" ]; do
        case "$line" in
            "$key="*)
                value="${line#*=}"
                value="${value%$'\r'}"
                case "$value" in
                    \"*\") value="${value#\"}"; value="${value%\"}" ;;
                    \'*\') value="${value#\'}"; value="${value%\'}" ;;
                esac
                printf '%s' "$value"
                return 0
                ;;
        esac
    done < "$ENV_FILE"

    return 0
}

is_valid_username() {
    local username="$1"

    [[ "$username" =~ ^[a-z][a-z0-9_-]{0,31}$ ]]
}

user_exists() {
    id "$1" >/dev/null 2>&1
}

group_exists() {
    getent group "$1" >/dev/null 2>&1
}

user_home() {
    getent passwd "$1" | cut -d: -f6
}

resolve_workspace_user() {
    local requested_username="$1"
    local runtime_username

    if user_exists "$DEFAULT_USER"; then
        printf '%s' "$DEFAULT_USER"
        return 0
    fi

    if [ -n "$requested_username" ] && user_exists "$requested_username"; then
        printf '%s' "$requested_username"
        return 0
    fi

    runtime_username="$(id -un 2>/dev/null)"
    if [ -n "$runtime_username" ] && [ "$runtime_username" != "root" ] && user_exists "$runtime_username"; then
        printf '%s' "$runtime_username"
        return 0
    fi

    return 1
}

ensure_sudoer() {
    local username="$1"
    local sudoers_tmp

    sudoers_tmp="$(mktemp)" || {
        log_error "Failed to create temporary sudoers file"
        return 1
    }

    printf '%s ALL=(ALL) NOPASSWD:ALL\n' "$username" > "$sudoers_tmp"

    if command -v visudo >/dev/null 2>&1; then
        if ! sudo visudo -cf "$sudoers_tmp" >/dev/null; then
            rm -f "$sudoers_tmp"
            log_error "Generated sudoers entry for $username is invalid"
            return 1
        fi
    fi

    if ! sudo install -o root -g root -m 0440 "$sudoers_tmp" "$SUDOERS_FILE"; then
        rm -f "$sudoers_tmp"
        log_error "Failed to install sudoers entry for $username"
        return 1
    fi

    rm -f "$sudoers_tmp"
    log_info "Sudoers entry is configured for $username"
    return 0
}

rename_group_if_needed() {
    local current_username="$1"
    local new_username="$2"

    if group_exists "$new_username"; then
        log_info "Group $new_username already exists"
        return 0
    fi

    if group_exists "$current_username"; then
        log_info "Renaming group from $current_username to $new_username"
        sudo groupmod --new-name "$new_username" "$current_username"
        return $?
    fi

    log_info "No matching user group found to rename"
    return 0
}

ensure_home_directory() {
    local username="$1"
    local expected_home="/home/$username"
    local current_home

    current_home="$(user_home "$username")"
    if [ "$current_home" = "$expected_home" ]; then
        log_info "Home directory is already set to $expected_home"
        return 0
    fi

    log_info "Moving home directory for $username from $current_home to $expected_home"
    sudo usermod --move-home --home "$expected_home" "$username"
    return $?
}

update_username() {
    local current_username="$1"
    local new_username="$2"

    if ! is_valid_username "$new_username"; then
        log_error "Invalid MAIA_USERNAME '$new_username'. Use 1-32 lowercase letters, numbers, hyphens, or underscores, starting with a letter."
        return 1
    fi

    if [ "$new_username" = "$current_username" ]; then
        log_info "Username is already set to $new_username"
        ensure_sudoer "$new_username" || return 1
        ensure_home_directory "$new_username"
        return $?
    fi

    if user_exists "$new_username"; then
        log_error "Cannot rename $current_username to $new_username because $new_username already exists"
        return 1
    fi

    log_info "Updating username from $current_username to $new_username"

    ensure_sudoer "$new_username" || return 1
    rename_group_if_needed "$current_username" "$new_username" || {
        log_error "Failed to rename group from $current_username to $new_username"
        return 1
    }

    if ! sudo usermod --login "$new_username" --move-home --home "/home/$new_username" "$current_username"; then
        log_error "Failed to rename $current_username or move home directory to /home/$new_username"
        return 1
    fi

    log_info "Username updated successfully"
    return 0
}

update_password() {
    local username="$1"
    local new_password="$2"

    if [ -z "$new_password" ]; then
        log_info "MAIA_PASSWORD not found in .env file, skipping password update"
        return 0
    fi

    if ! user_exists "$username"; then
        log_error "Cannot update password because user $username does not exist"
        return 1
    fi

    log_info "Updating password for user $username"
    if ! printf '%s:%s\n' "$username" "$new_password" | sudo chpasswd; then
        log_error "Failed to update password for user $username"
        return 1
    fi

    log_info "Password updated successfully"
    return 0
}

main() {
    local maia_username
    local maia_password
    local current_username
    local target_username
    local failed=0

    log_info "Starting user credential update process"

    if [ ! -f "$ENV_FILE" ]; then
        log_info ".env file not found at $ENV_FILE, using defaults"
        log_info "User credential update process completed"
        return 0
    fi

    log_info "Found .env file at $ENV_FILE"
    maia_username="$(read_env_var "MAIA_USERNAME")"
    maia_password="$(read_env_var "MAIA_PASSWORD")"

    current_username="$(resolve_workspace_user "$maia_username")"
    if [ -z "$current_username" ]; then
        log_error "Could not determine the workspace user to update"
        return 0
    fi

    target_username="$current_username"

    if [ -n "$maia_username" ]; then
        log_info "MAIA_USERNAME found in .env file"
        if update_username "$current_username" "$maia_username"; then
            target_username="$maia_username"
        else
            failed=1
        fi
    else
        log_info "MAIA_USERNAME not found in .env file, using current user: $current_username"
        ensure_sudoer "$current_username" || failed=1
    fi

    if [ "$failed" -eq 0 ]; then
        if [ -n "$maia_password" ]; then
            log_info "MAIA_PASSWORD found in .env file"
        fi
        update_password "$target_username" "$maia_password" || failed=1
    else
        log_error "Skipping password update because username or sudoers update failed"
    fi

    if [ "$failed" -eq 0 ]; then
        log_info "User credential update process completed"
    else
        log_error "User credential update process completed with errors"
    fi

    return 0
}

main
