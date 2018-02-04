#!/bin/bash
echo start
git pull origin master
echo 1
git add .
echo 2
git commit -m "新提交"
echo 3
git push origin master
echo end
