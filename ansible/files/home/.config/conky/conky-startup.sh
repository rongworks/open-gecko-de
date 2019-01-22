sleep 20s
killall conky
cd "$HOME/.config/conky/themes/conky_rings"
conky -c "$HOME/.config/conky/themes/conky_rings/cpu" &
cd "$HOME/.config/conky/themes/conky_rings"
conky -c "$HOME/.config/conky/themes/conky_rings/mem" &
cd "$HOME/.config/conky/themes/conky_rings"
conky -c "$HOME/.config/conky/themes/conky_rings/rings" &
