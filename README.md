# D.I.R.T. (Dirty Incident Response Toolkit)

*I like DIRT, I like DIRT ~ Red Hot Chili Peppers*

Highly extendable CLI tool used to organize the mess that is the result of many quick malware analyses.

## Instalation

DIRT needs Python 3.5+ to work properly. You can install it from PyPi

```
pip3 install dirt
```

If you want to use shell extensions, add this single line to your `.bashrc`

```
source dirt-bash
```

## Key features

* Zero-configuration, zero-database (everything based on symlinks, simple conventions and human-readable text files)
* Easily extensible, low-effort toolset integration with DIRT
* Sharable workspace (UUID-based identifiers)
* Useful for everything that needs as-easy-as-possible files organization (IRT, CTI, CTFs etc.)
* Autocompletion (not ideal because of 'click' limitations, but good enough)

## Ah? Yet another "simple" convention?

Well... my workspace at the first months of analyzing malware looked something like that

```
malware
├── weird-something
│   ├── dump252.dmp
│   ├── wtf
│   │   └── ... 
│   └── analysis
│       └── 252 
│           ├── 223412ad4f.bin
│           ├── 443412ad4f.bin
│           └── report.json
├── random_malware
│   └── ...
├── shade
│   └── ...
├── tesla_crypt
│   └── ...
...
```
    
Maybe good enough, but we have pretty no chances to correlate something with analysis from the past. 
So I've tried to introduce some timestamp-based order for non-obvious samples (`"Hey, I wasn't sure what it was but I've remember that similar campaign was in 2017-06..."`)

```
malware
├── unclassified
│   ├── 2017-03-01
│   │   └── ...
│   ├── 2016-05-03_emotet
│   │   └── ... 
│   ├── 2015-02-03_tesla
│   │   └── ... 
│   ...
│
├── shade
│   └── ...
├── jrat
│   └── ...
├── tesla_crypt
│   └── symlink to 2015-02-03_tesla
...

tools
├── emotet-tools
│   └── ...
├── tofsee-tools
│   └── ...
├── generic
│   └── ...
...
```

Much better, but keeping that order "by hand", especially in cases that required quick response was pain in ... so I've tried to do use my superhero (Python) skills and find a way to integrate and automate everything (creating workspaces, toolset housekeeping) as much as possible.

## DIRT workspaces

For each incident that is being analyzed we usually need separate workspace, because at the beginning of analysis we can't be sure what we got. But during analysis of each case we know more and more, so we want to:
* Write out IoCs, attribution and other information found during analysis
* Correlate that single case with the others from the past
* Provide some malware classification etc. etc.

All created incidents has its own `DATE_UUID` directory placed in common location `~/.dirt/data`.

If you want to provide some links to incident you're currently working on, DIRT is providing symlink `~/.dirt/data/current`

```
~/.dirt (home)
├── data
│   ├── 2017-11-13_RPIZ4NE7TRCCNCQ2WFX4RWEPPQ
│   │   ├── README (quick text notes)
│   │   ├── .dirt  
│   │       (collected information about incident kept in YAML format)
│   │   ... 
│   └── current -(sym)-> 2017-11-13_RPIZ4NE7TRCCNCQ2WFX4RWEPPQ
│       (incident we're currently working on)
```

All attributes, tags and description are kept in `.dirt` file. All information contained in this file are easily accessible via CLI.

But sometimes we need to group few cases under single keyword e.g. all analyses related with specific malware family, actor or institution. All workspaces can be grouped using **tags**.

```
~/.dirt (home)
├── tags
│   ├── emotet
│   │   ├── (sym) 2017-11-13_RPIZ4NE7TRCCNCQ2WFX4RWEPPQ
│   │   ├── (sym) 2017-11-10_4RWEPABCNE7ZCWFXPQ4TCNCQ2R
│   │   ...
│   │
│   ├── tofsee
│   │
...
```

That's how DIRT keeps everything in order. We can work with this structure using simple commands:

**Creating new incident**

```bash
$ dirt new
[+] New incident created 2019-01-04_NDEXWAZR4RAVFLLRZXBWYMK6ME
```

Ok, so let's go to our workspace:

```bash
$ dirt cwd
[+] Incident path: /home/psrok1/.dirt/data/2019-01-04_NDEXWAZR4RAVFLLRZXBWYMK6ME
$ dirt cd
```

With enabled shell extensions you can directly use 'cp' to copy files from current dir to your incident directory.
Additional feature is expansion `incident:relpath` form to absolute path. 
```bash
$ dirt mv
mv: missing file operand
Try 'mv --help' for more information.
$ dirt mv malware.exe current:.
``` 

Well, it seems to be similar to incident opened before:

```
$ dirt show overview
Recently opened incidents:
 +  2019-01-04_NDEXW    <no description>                           opened
    2019-01-03_A42EY    <no description>                           opened
                        #lucky #ransomware
    2018-12-03_AUYPI    jscript                                    closed
Recent incidents:
 +  2019-01-04_NDEXW    <no description>                           opened
    2019-01-03_A42EY    <no description>                           opened
                        #luckier #dropper #helper
    2018-12-03_AUYPI    jscript                                    closed
```

Let's switch to that incident we've opened previously:
```
$ dirt switch previous
[+] Switched to 2019-01-03_A42EYL46CNDZZDX3XL45E25JSU
```

... and add relation to current one and close it
```
$ dirt add rel 2019-01
[!] Incident name is ambiguous. Pick one of them:
2019-01-03_A42EYL46CNDZZDX3XL45E25JSU
2019-01-04_NDEXWAZR4RAVFLLRZXBWYMK6ME
[!] No incident found.
Aborted!
$ dirt add rel 2019-01-04
[+] Marked 2019-01-03_A42EYL46CNDZZDX3XL45E25JSU as related with 2019-01-04_NDEXWAZR4RAVFLLRZXBWYMK6ME
$ dirt close
[!] Incident doesn't have description. Do you want to add one?
Enter description [[empty]]: Lucky campaign
[+] Incident 2019-01-03_A42EYL46CNDZZDX3XL45E25JSU closed
```

To learn about all DIRT capabilities and how to integrate it with your toolset (write plugins) - go to Wiki page.

## Plugins and extensions

Almost all DIRT features are extensible using plugin system, which allows you to add additional commands, special attributes or
modify default behaviour of built-in functions.

Example plugin (adding Git-based versioning of incident files) can be found [here (dirt-vcs)](http://github.com/psrok1/dirt-vcs).

DIRT supports standalone Python 3 scripts added to `~/.dirt/plugins`

Example:

```
~/.dirt (home)
├── plugins
│   ├── hooks
│   │   ├── hello_new.py

```

```python
# hello_new.py

from dirt.hooks import pre_hook
from dirt.commands.new import new_command
from dirt.libs.log import info


@pre_hook(new_command)
def hook_new_command(ctx, *args, **kwargs):
    """
    Pre-hook on "dirt new" command.
    """
    info("Nice to see you're creating new incident!")
```

## Bugs, missing features...

Disclaimer: You're using it at your own risk! 

I can't guarantee that everything works right, but feel free to create an issue or pull request if you find a bug.

If you have any questions - contact can be found on my webpage: https://0xcc.pl/contact.html

**TODO:**

* Support for Python 2/3 (not so important when using only CLI, but might be useful for tool integration)
* Importing incidents
* Better support for zsh shell
