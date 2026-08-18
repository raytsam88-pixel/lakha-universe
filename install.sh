#!/data/data/com.termux/files/usr/bin/bash

echo "Installing Lakha Tool..."

pkg update -y
pkg install python -y

cp lakha.py "$PREFIX/bin/lakha"
chmod +x "$PREFIX/bin/lakha"

echo ""
echo "================================"
echo " Lakha Tool Installed!"
echo " Run it using: lakha"
echo "================================"
