@echo off


echo ===============================
echo 云创竞价空间自动更新系统
echo ===============================


cd /d "D:\大四下\华翀"


echo.
echo [1/3] 更新云创数据


venv\Scripts\python.exe main.py


if %errorlevel% neq 0 (

    echo 数据更新失败

    pause

    exit /b 1

)


echo.
echo [2/3] 提交GitHub


git add 云创矩阵分析.xlsx


git commit -m "daily update %date%"


echo.
echo [3/3] 推送GitHub


git push


echo.
echo ===============================
echo 更新完成
echo ===============================


pause