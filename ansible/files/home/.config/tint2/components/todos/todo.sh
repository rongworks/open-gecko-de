#!/bin/bash

editor_exe="beaver"
todo_path="$HOME/.config/tint2/todos/todos.md"
text=$(cat $todo_path | grep "#" )

if [ $1 = "show" ]; then
  /usr/bin/zenity --notification --text="$text"
elif [[ $1 = "edit" ]]; then
  $editor_exe $todo_path
elif [[ $1 = "list" ]]; then
  echo "T:" && grep "#" $todo_path | wc -l
fi
