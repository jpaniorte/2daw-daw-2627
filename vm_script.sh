#!/usr/bin/env bash
#
# setup-dev-vm.sh — Entorno de desarrollo para Ubuntu MATE 24.04 en VirtualBox
#
# Instala: Docker CE, VS Code (+extensiones), Python/uv, Node LTS, Go, Java 21,
#          Rust, GitHub CLI, herramientas de terminal, OpenCode y ~/workspace.
#
# Uso (como usuario normal, NO con sudo):
#     chmod +x setup-dev-vm.sh
#     ./setup-dev-vm.sh
#
# Para omitir lenguajes:
#     WITH_JAVA=0 WITH_RUST=0 ./setup-dev-vm.sh
#
# Guest Additions de VirtualBox (GA_MODE):
#     auto (por defecto)  ISO oficial de la misma versión que el anfitrión; si falla, paquetes de Ubuntu
#     iso                 solo la ISO oficial
#     apt                 solo los paquetes de Ubuntu
#     skip                no instalar Guest Additions
#
# Es idempotente: si falla a medias, puedes volver a ejecutarlo.

set -Eeuo pipefail

# ---------------------------------------------------------------- Opciones
WITH_PYTHON="${WITH_PYTHON:-1}"
WITH_NODE="${WITH_NODE:-1}"
WITH_GO="${WITH_GO:-1}"
WITH_JAVA="${WITH_JAVA:-1}"
WITH_RUST="${WITH_RUST:-1}"
WITH_OPENCODE="${WITH_OPENCODE:-1}"
GA_MODE="${GA_MODE:-auto}"          # auto | iso | apt | skip  (Guest Additions de VirtualBox)
WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/workspace}"

# ---------------------------------------------------------------- Utilidades
log()  { printf '\n\033[1;34m==> %s\033[0m\n' "$*"; }
warn() { printf '\033[1;33m[aviso]\033[0m %s\n' "$*" >&2; }
die()  { printf '\033[1;31m[error]\033[0m %s\n' "$*" >&2; exit 1; }
trap 'die "Falló en la línea $LINENO. Puedes volver a ejecutar el script (es idempotente)."' ERR

ME="$(id -un)"
export PATH="$HOME/.local/bin:/usr/local/go/bin:$HOME/.cargo/bin:$PATH"

# ---------------------------------------------------------------- Comprobaciones
[[ $EUID -ne 0 ]] || die "No lo ejecutes como root ni con sudo. Ejecútalo como tu usuario normal."
[[ -r /etc/os-release ]] || die "No encuentro /etc/os-release."
# shellcheck disable=SC1091
. /etc/os-release
[[ "${ID:-}" == "ubuntu" ]] || die "Este script está pensado para Ubuntu (detectado: ${ID:-desconocido})."
[[ "${VERSION_ID:-}" == "24.04" ]] || warn "Pensado para Ubuntu 24.04; detectado ${VERSION_ID:-?}. Continúo igualmente."
command -v sudo >/dev/null || die "Necesito sudo."

ARCH="$(dpkg --print-architecture)"            # amd64 | arm64
CODENAME="${UBUNTU_CODENAME:-$VERSION_CODENAME}"

log "Pidiendo permisos de administrador (se mantienen mientras dure el script)"
sudo -v
(
  trap - ERR
  while true; do
    sudo -n true 2>/dev/null || exit
    sleep 50
    kill -0 "$$" 2>/dev/null || exit
  done
) &
KEEPALIVE_PID=$!
trap 'kill "$KEEPALIVE_PID" 2>/dev/null || true' EXIT

APT=(sudo env DEBIAN_FRONTEND=noninteractive NEEDRESTART_MODE=a apt-get -o DPkg::Lock::Timeout=300 -y)
apt_install() { "${APT[@]}" install "$@"; }
# Instala paquetes opcionales uno a uno: si alguno no existe, solo avisa.
apt_try() {
  local p
  for p in "$@"; do
    if "${APT[@]}" install "$p" >/dev/null 2>&1; then
      echo "  ok: $p"
    else
      warn "paquete no disponible, lo omito: $p"
    fi
  done
}

# ---------------------------------------------------------------- 1. Base
log "1/8 Actualizando el sistema e instalando paquetes base"
"${APT[@]}" update
"${APT[@]}" upgrade
apt_install \
  ca-certificates curl wget gnupg lsb-release software-properties-common apt-transport-https \
  build-essential pkg-config cmake make gdb git git-lfs \
  unzip zip xz-utils jq tmux htop tree vim neovim \
  ripgrep fzf bat fd-find shellcheck \
  sqlite3 postgresql-client redis-tools \
  net-tools dnsutils iproute2 openssh-client
# Herramientas extra (al estilo Bluefin DX); opcionales
apt_try dmidecode zoxide eza btop ncdu strace ltrace iotop bpftrace

# ---------------------------------------------------------------- 2. Repositorios
log "2/8 Añadiendo repositorios oficiales (Docker, VS Code, GitHub CLI)"
sudo install -m 0755 -d /etc/apt/keyrings

# Docker
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=${ARCH} signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu ${CODENAME} stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null

# VS Code
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --batch --yes --dearmor \
  | sudo tee /usr/share/keyrings/microsoft.gpg >/dev/null
echo "deb [arch=${ARCH} signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/code stable main" \
  | sudo tee /etc/apt/sources.list.d/vscode.list >/dev/null
# Evita que el paquete 'code' añada un segundo repositorio duplicado
echo "code code/add-microsoft-repo boolean false" | sudo debconf-set-selections

# GitHub CLI
sudo curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg -o /etc/apt/keyrings/githubcli-archive-keyring.gpg
sudo chmod a+r /etc/apt/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=${ARCH} signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
  | sudo tee /etc/apt/sources.list.d/github-cli.list >/dev/null

"${APT[@]}" update

# ---------------------------------------------------------------- 3. Docker, VS Code, gh, Guest Additions
log "3/8 Instalando Docker, VS Code, GitHub CLI y Guest Additions"
apt_install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker "$ME"

if [[ ! -f /etc/docker/daemon.json ]]; then
  sudo tee /etc/docker/daemon.json >/dev/null <<'EOF'
{
  "log-driver": "json-file",
  "log-opts": { "max-size": "10m", "max-file": "3" }
}
EOF
  sudo systemctl restart docker
fi
if sudo docker run --rm hello-world >/dev/null 2>&1; then
  echo "  Docker funciona correctamente"
else
  warn "No pude ejecutar hello-world; revisa 'sudo systemctl status docker'."
fi

apt_install code gh

# ---- Guest Additions de VirtualBox ------------------------------------------
# Versión de VirtualBox del anfitrión, leída de las cadenas OEM de la DMI
# (VirtualBox las expone como "vboxVer_X.Y.Z").
host_vbox_version() {
  sudo dmidecode -t 11 2>/dev/null | sed -n 's/.*vboxVer_\([0-9][0-9.]*\).*/\1/p' | head -n1
}

# Método A (recomendado): Guest Additions oficiales, de la misma versión que el anfitrión.
# Usa el CD si ya está montado (Dispositivos → Insertar imagen de CD) o descarga la ISO.
ga_from_iso() {
  local ver="$1" iso="" mnt="" run="" f
  for f in /media/"$ME"/VBox_GAs_*/VBoxLinuxAdditions.run /media/VBox_GAs_*/VBoxLinuxAdditions.run; do
    if [[ -f "$f" ]]; then run="$f"; break; fi
  done
  if [[ -z "$run" ]]; then
    [[ -n "$ver" ]] || { warn "No pude detectar la versión de VirtualBox del anfitrión."; return 1; }
    iso="/tmp/VBoxGuestAdditions_${ver}.iso"
    echo "  Descargando Guest Additions ${ver}..."
    curl -fL --retry 3 --progress-bar -o "$iso" \
      "https://download.virtualbox.org/virtualbox/${ver}/VBoxGuestAdditions_${ver}.iso" \
      || { rm -f "$iso"; return 1; }
    mnt="$(mktemp -d)"
    sudo mount -o loop,ro "$iso" "$mnt" || { rmdir "$mnt"; rm -f "$iso"; return 1; }
    run="$mnt/VBoxLinuxAdditions.run"
  fi

  # Requisitos para compilar los módulos del kernel
  "${APT[@]}" install dkms build-essential perl bzip2 tar linux-headers-generic || return 1
  "${APT[@]}" install "linux-headers-$(uname -r)" >/dev/null 2>&1 \
    || warn "No encontré las cabeceras del kernel en ejecución; DKMS compilará los módulos al reiniciar."

  sudo sh "$run" --nox11 \
    || warn "El instalador terminó con avisos (es normal si el módulo aún no está cargado: se activará al reiniciar)."

  if [[ -n "$mnt" ]]; then
    sudo umount "$mnt" || true
    rmdir "$mnt" || true
    rm -f "$iso"
  fi
  compgen -G "/opt/VBoxGuestAdditions-*" >/dev/null
}

# Método B (alternativa): paquetes de Ubuntu. Más simple, pero la versión puede no coincidir con el anfitrión.
ga_from_apt() {
  "${APT[@]}" install virtualbox-guest-utils virtualbox-guest-x11
}

if [[ "$GA_MODE" == "skip" ]]; then
  echo "-- Guest Additions omitidas (GA_MODE=skip)"
elif [[ "$(systemd-detect-virt 2>/dev/null || true)" != "oracle" ]]; then
  echo "-- No estamos en VirtualBox: omito las Guest Additions"
else
  echo "-- Guest Additions de VirtualBox"
  HOST_VER="$(host_vbox_version || true)"
  if command -v VBoxClient >/dev/null 2>&1; then
    CUR_VER="$(VBoxControl --version 2>/dev/null || true)"
    echo "  Ya instaladas (${CUR_VER:-versión desconocida}); no toco nada"
    if [[ -n "$HOST_VER" && -n "$CUR_VER" && "$CUR_VER" != "$HOST_VER"* ]]; then
      warn "La versión de las Guest Additions (${CUR_VER}) no coincide con la de VirtualBox (${HOST_VER})."
    fi
  else
    case "$GA_MODE" in
      iso)
        ga_from_iso "$HOST_VER" || warn "No se pudieron instalar las Guest Additions desde la ISO."
        ;;
      apt)
        ga_from_apt || warn "No se pudieron instalar las Guest Additions desde apt."
        ;;
      *)  # auto: ISO oficial y, si falla, paquetes de Ubuntu
        if ! ga_from_iso "$HOST_VER"; then
          warn "Falló el método oficial; pruebo con los paquetes de Ubuntu."
          ga_from_apt || warn "No se pudieron instalar las Guest Additions. Instálalas a mano desde el menú Dispositivos."
        fi
        ;;
    esac
  fi
  if getent group vboxsf >/dev/null; then sudo usermod -aG vboxsf "$ME"; fi
fi

# Extensiones de VS Code
log "Instalando extensiones de VS Code"
EXTENSIONS=(
  ms-azuretools.vscode-docker
  ms-vscode-remote.remote-containers
  eamodio.gitlens
  editorconfig.editorconfig
  redhat.vscode-yaml
  timonwong.shellcheck
)
[[ "$WITH_PYTHON" == 1 ]] && EXTENSIONS+=(ms-python.python)
[[ "$WITH_NODE"   == 1 ]] && EXTENSIONS+=(dbaeumer.vscode-eslint esbenp.prettier-vscode)
[[ "$WITH_GO"     == 1 ]] && EXTENSIONS+=(golang.go)
[[ "$WITH_JAVA"   == 1 ]] && EXTENSIONS+=(vscjava.vscode-java-pack)
[[ "$WITH_RUST"   == 1 ]] && EXTENSIONS+=(rust-lang.rust-analyzer)
for ext in "${EXTENSIONS[@]}"; do
  if code --install-extension "$ext" --force >/dev/null 2>&1; then
    echo "  ok: $ext"
  else
    warn "no pude instalar la extensión $ext (puedes hacerlo luego desde VS Code)"
  fi
done

# ---------------------------------------------------------------- 4. Lenguajes
log "4/8 Instalando lenguajes de programación"

if [[ "$WITH_PYTHON" == 1 ]]; then
  echo "-- Python"
  apt_install python3 python3-pip python3-venv python3-dev pipx
  if ! command -v uv >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/install.sh | env UV_NO_MODIFY_PATH=1 sh
  fi
fi

if [[ "$WITH_NODE" == 1 ]]; then
  echo "-- Node.js (LTS)"
  if ! command -v node >/dev/null 2>&1; then
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    apt_install nodejs
  fi
  sudo npm install -g pnpm >/dev/null 2>&1 || warn "No pude instalar pnpm"
fi

if [[ "$WITH_GO" == 1 ]]; then
  echo "-- Go (última versión oficial)"
  GO_VERSION="$(curl -fsSL 'https://go.dev/VERSION?m=text' | head -n1)"
  if [[ ! "$GO_VERSION" =~ ^go[0-9]+\.[0-9]+ ]]; then
    warn "No pude determinar la última versión de Go; lo omito."
  elif [[ -x /usr/local/go/bin/go ]] && /usr/local/go/bin/go version | grep -q "${GO_VERSION} "; then
    echo "  ${GO_VERSION} ya instalada"
  else
    curl -fsSL "https://go.dev/dl/${GO_VERSION}.linux-${ARCH}.tar.gz" -o /tmp/go.tgz
    sudo rm -rf /usr/local/go
    sudo tar -C /usr/local -xzf /tmp/go.tgz
    rm -f /tmp/go.tgz
  fi
fi

if [[ "$WITH_JAVA" == 1 ]]; then
  echo "-- Java 21 + Maven"
  apt_install openjdk-21-jdk maven
fi

if [[ "$WITH_RUST" == 1 ]]; then
  echo "-- Rust (rustup)"
  if [[ ! -x "$HOME/.cargo/bin/rustup" ]]; then
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path
  fi
fi

# ---------------------------------------------------------------- 5. OpenCode
if [[ "$WITH_OPENCODE" == 1 ]]; then
  log "5/8 Instalando OpenCode"
  mkdir -p "$HOME/.local/bin"
  if [[ ! -x "$HOME/.local/bin/opencode" ]] && ! command -v opencode >/dev/null 2>&1; then
    if ! XDG_BIN_DIR="$HOME/.local/bin" bash -c 'curl -fsSL https://opencode.ai/install | bash'; then
      warn "El instalador oficial falló; pruebo con npm."
      if command -v npm >/dev/null 2>&1; then
        sudo npm install -g opencode-ai@latest || warn "OpenCode no se pudo instalar."
      fi
    fi
  else
    echo "  OpenCode ya instalado"
  fi
else
  log "5/8 OpenCode omitido (WITH_OPENCODE=0)"
fi

# ---------------------------------------------------------------- 6. Workspace
log "6/8 Creando el workspace en $WORKSPACE_DIR"
mkdir -p "$WORKSPACE_DIR"
# Marcador en el explorador de archivos (Caja, el de MATE)
BOOKMARKS="$HOME/.config/gtk-3.0/bookmarks"
mkdir -p "$(dirname "$BOOKMARKS")"
grep -qF "file://$WORKSPACE_DIR" "$BOOKMARKS" 2>/dev/null || echo "file://$WORKSPACE_DIR workspace" >> "$BOOKMARKS"

# ---------------------------------------------------------------- 7. Configuración
log "7/8 Configurando shell, git y sistema"

# bat y fd se instalan en Ubuntu como 'batcat' y 'fdfind'
mkdir -p "$HOME/.local/bin"
if command -v batcat >/dev/null 2>&1; then ln -sf "$(command -v batcat)" "$HOME/.local/bin/bat"; fi
if command -v fdfind >/dev/null 2>&1; then ln -sf "$(command -v fdfind)" "$HOME/.local/bin/fd"; fi

if ! grep -qF "# >>> setup-dev-vm >>>" "$HOME/.bashrc"; then
  cat >> "$HOME/.bashrc" <<'EOF'

# >>> setup-dev-vm >>>
export PATH="$HOME/.local/bin:/usr/local/go/bin:$HOME/go/bin:$PATH"
[ -f "$HOME/.cargo/env" ] && . "$HOME/.cargo/env"

alias ws='cd "$HOME/workspace"'
alias dc='docker compose'
if command -v eza >/dev/null 2>&1; then
  alias ls='eza --group-directories-first'
  alias ll='eza -lah --group-directories-first --git'
else
  alias ll='ls -alFh'
fi
if command -v zoxide >/dev/null 2>&1; then eval "$(zoxide init bash)"; fi
[ -f /usr/share/doc/fzf/examples/key-bindings.bash ] && . /usr/share/doc/fzf/examples/key-bindings.bash
[ -f /usr/share/doc/fzf/examples/completion.bash ]   && . /usr/share/doc/fzf/examples/completion.bash
# <<< setup-dev-vm <<<
EOF
fi

git config --global init.defaultBranch main
git config --global push.autoSetupRemote true
git config --global pull.rebase false

# Más watchers de ficheros para VS Code, webpack, etc.
printf 'fs.inotify.max_user_watches=524288\nfs.inotify.max_user_instances=1024\n' \
  | sudo tee /etc/sysctl.d/99-dev.conf >/dev/null
sudo sysctl --system >/dev/null

sudo apt-get -y autoremove >/dev/null 2>&1 || true
sudo apt-get -y clean >/dev/null 2>&1 || true

# ---------------------------------------------------------------- 8. Resumen
log "8/8 Resumen"
show() {
  local name="$1"; shift
  if command -v "$1" >/dev/null 2>&1; then
    printf '  %-10s %s\n' "$name" "$("$@" 2>&1 | head -n1)"
  else
    printf '  %-10s %s\n' "$name" "— no instalado"
  fi
}
show Git      git --version
show Docker   docker --version
show Compose  docker compose version
show VSCode   code --version
show Python   python3 --version
show uv       uv --version
show Node     node --version
show pnpm     pnpm --version
show Go       go version
show Java     java -version
show Maven    mvn --version
show Rust     rustc --version
show gh       gh --version
show OpenCode opencode --version
show GuestAdd VBoxControl --version

echo
echo "Workspace:  $WORKSPACE_DIR"
if [[ -z "$(git config --global user.name || true)" ]]; then
  echo
  echo "Pendiente: configura tu identidad en git:"
  echo "  git config --global user.name  \"Tu Nombre\""
  echo "  git config --global user.email \"tu@correo.com\""
fi
echo
echo "IMPORTANTE: reinicia la VM ('sudo reboot') para activar las Guest Additions (portapapeles,"
echo "carpetas compartidas, resolución automática) y aplicar los grupos 'docker'/'vboxsf' y el PATH."
echo "Después podrás usar 'docker' sin sudo."
echo "OpenCode: entra en una carpeta de proyecto, ejecuta 'opencode' y conecta tu proveedor de IA."