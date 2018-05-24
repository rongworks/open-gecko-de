#!/bin/bash

ETH=$(curl -s https://api.kraken.com/0/public/Ticker?pair=ETHEUR | grep -Po '"c":.*?[^\\]",' | grep  -Po '[0-9.]+')

echo "€/Ξ: $ETH"
