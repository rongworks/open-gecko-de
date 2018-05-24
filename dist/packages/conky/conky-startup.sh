sleep 20s
killall conky
cd "/home/mathias/.config/conky/themes/conky_rings"
conky -c "/home/mathias/.config/conky/themes/conky_rings/cpu" &
cd "/home/mathias/.config/conky/themes/conky_rings"
conky -c "/home/mathias/.config/conky/themes/conky_rings/mem" &
cd "/home/mathias/.config/conky/themes/conky_rings"
conky -c "/home/mathias/.config/conky/themes/conky_rings/rings" &
