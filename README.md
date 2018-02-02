alien_invasion
======
一个简单的小游戏，《Python编程：从入门到实践》 上的demo
***
__alien_invasion.exe需与images文件夹保持同一目录__<br>
***

开发环境：
--------
    python3.5.2 win32
    pip 8.8.1
    pyinstall:3.3.1
--------

打包使用的是pyinstaller,百度即可下载<br>
在打包的时候遇到了一些问题：<br>
1.打包从执行文件开始打包，会将依赖的文件或者包都导入但是我在使用这种方式时，打包出来的程序无法运行，<br>
然后我尝试打包了一个只有一个文件的python程序是可以成功的，我就猜想是否通过这种方法来打包一个python工程可能<br>
无法引入所有的包，于是我就转到了该工程的目录下打开命令行执行pyinstaller main.py，打包成功，可以执行(找了一天bug）<br>
除此之外也发生了一些问题<br>
1)这种打包方式不会将资源文件也一起打包，所以在引用资源文件时使用相对路径还有资源文件最后会和执行文件放在同一文件夹内<br>
2)打包时的一些参数pyinstaller -F -w main.py是较常用的，-F表示将所有文件打包为一个可执行文件，-w则是表示在运行可执行文件时不需命令行，<br>
-F可换为-D(也是默认参数)，这会将所有文件打包为一个文件夹,包括一些注册信息，据说可以帮助找bug<br>

参数 	含义
    -F 	指定打包后只生成一个exe格式的文件<br>
    -D 	–onedir 创建一个目录，包含exe文件，但会依赖很多文件（默认选项）<br>
    -c 	–console, –nowindowed 使用控制台，无界面(默认选项)<br>
    -w 	–windowed, –noconsole 使用窗口，无控制台<br>
    -p 	添加搜索路径，让其找到对应的库。<br>
    -i 	改变生成程序的icon图标<br>

找了一天bug的好处是帮助我了解了打包后的文件结构：<br>
打包后会在main.py当前所在的文件夹生成两个文件夹:dist,build <br>
dist中包含了可执行文件，而build中包含了一些图标文件，注册文件等，最重要的是错误信息的日志文件也会包含在build中<br>

有一些修改：<br>
(1).ship.py与alien.py中使用的图片设置做了改动,由<br>
            'images/alien.bmp'=>'./images/alien.bmp'<br>
(2).button.py与scoreboard.py中的字体做了改动,由<br>
            'pygame.font.SysFont(None, 48)'=>'pygame.font.SysFont('arial', 30)'<br>
