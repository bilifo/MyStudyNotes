set time1=%date:~0,4%%date:~5,2%%date:~8,2% %time:~0,2%:%time:~3,2%:%time:~6,2%
set commit1=%time1%
git status

git add ./
git commit -m "%commit1%"
git log

git push github
pause

