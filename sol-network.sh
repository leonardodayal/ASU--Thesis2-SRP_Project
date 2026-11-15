#!/bin/bash
# sol-network.sh
# Turns IPv6 off on your active network services so the ASU Cisco VPN's DNS
# works, then restores exactly what it changed when you are done.
#
# Usage:
#   bash sol-network.sh start    # IPv6 off + flush DNS (run BEFORE connecting the VPN)
#   bash sol-network.sh stop     # restore IPv6 + flush DNS (run AFTER disconnecting)
#   bash sol-network.sh status   # show IPv6 state and what sol.asu.edu resolves to
#   bash sol-network.sh connect  # check the VPN, then SSH into Sol (asks for your ASURITE once)

STATE="$HOME/.sol-network-state"

list_services() {
  # Skip the header line and any disabled services (those start with *)
  networksetup -listallnetworkservices | tail -n +2 | grep -v '^\*'
}

ipv6_mode() {
  networksetup -getinfo "$1" | awk -F': ' '/^IPv6:/{print $2; exit}'
}

flush_dns() {
  sudo dscacheutil -flushcache
  sudo killall -HUP mDNSResponder
  echo "DNS cache flushed."
}

start() {
  if [ -s "$STATE" ]; then
    echo "Already set up. Run 'bash $0 stop' to restore first."
    exit 1
  fi
  sudo -v || exit 1
  : > "$STATE"
  while IFS= read -r svc; do
    if [ "$(ipv6_mode "$svc")" = "Automatic" ]; then
      if sudo networksetup -setv6off "$svc"; then
        echo "$svc" >> "$STATE"
        echo "IPv6 off:       $svc"
      fi
    else
      echo "Left alone:     $svc (IPv6 is not set to Automatic)"
    fi
  done < <(list_services)
  flush_dns
  echo
  echo "Next: connect the VPN to sslvpn.asu.edu/2fa, then open https://sol.asu.edu"
  echo "(If the VPN was already connected, disconnect and reconnect it first.)"
}

stop() {
  if [ ! -s "$STATE" ]; then
    echo "Nothing to restore."
    rm -f "$STATE"
    exit 0
  fi
  sudo -v || exit 1
  while IFS= read -r svc; do
    if sudo networksetup -setv6automatic "$svc"; then
      echo "IPv6 restored:  $svc"
    fi
  done < "$STATE"
  rm -f "$STATE"
  flush_dns
}

status() {
  while IFS= read -r svc; do
    echo "$svc: IPv6 $(ipv6_mode "$svc")"
  done < <(list_services)
  echo
  addr=$(dscacheutil -q host -a name sol.asu.edu | awk '/ip_address/{print $2; exit}')
  echo "sol.asu.edu resolves to: ${addr:-nothing}"
  case "$addr" in
    10.*) echo "Looks right: an internal ASU address." ;;
    "")   echo "No answer. Is the VPN connected?" ;;
    *)    echo "That's a public address, so the VPN's DNS isn't being used." ;;
  esac
}

connect() {
  USERFILE="$HOME/.sol-network-user"
  if [ -s "$USERFILE" ]; then
    asurite=$(cat "$USERFILE")
  else
    read -r -p "ASURITE username: " asurite
    [ -n "$asurite" ] || { echo "No username given."; exit 1; }
    echo "$asurite" > "$USERFILE"
    echo "(Saved to $USERFILE. Delete that file to change it.)"
  fi

  # Sanity check: with the VPN up, sol.asu.edu should resolve to an internal 10.x address
  addr=$(dscacheutil -q host -a name sol.asu.edu | awk '/ip_address/{print $2; exit}')
  case "$addr" in
    10.*) ;;
    *)
      echo "sol.asu.edu resolves to '${addr:-nothing}', not an internal ASU address."
      echo "Connect the VPN (sslvpn.asu.edu/2fa) and run 'bash $0 start' first."
      exit 1
      ;;
  esac

  echo "Connecting to Sol as $asurite (approve the Duo prompt if asked)..."
  ssh "$asurite@sol.asu.edu"
}

case "$1" in
  start)   start ;;
  stop)    stop ;;
  status)  status ;;
  connect) connect ;;
  *) echo "Usage: bash $0 {start|stop|status|connect}"; exit 1 ;;
esac
