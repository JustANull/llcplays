LLCPlays
========

What's the point?
-----------------

This project is intended to be a complete TwitchPlaysPokemon style bot initially set up for my personal use, but configurable for others.

Can I use it?
-------------

Knock yourself out. I'm not going to stop you. If you want to remove the userlist, remove the user list from the config.

How do I use it?
----------------

Carefully!

Read this entire section!

### Required Software

These are all what I developed on:

`python 2.7.6`

`irc-8.5.4` is what I developed the IRC features on.

`pygame` is used to display the window of past commands.

If you plan to use the direct keyboard output (that is, focus a window and have the bot virtually press keys), you'll have to install `PyUserInput`. Keyboard is the default. You can specify a file in the command line as well as standard out.

Other versions of things here might work, but it is unclear at this time how well if at all.

### Command Line

    ./llcplays.py  
    Will run, outputting commands to the keyboard.  
    ./llcplays.py stdout  
    Will run, outputting commands to standard out.  
    ./llcplays.py stdout filename  
    Will run, outputting commands to the file with the given name.

### Various Details

This project is incomplete.

Automatic saving currently occurs every 5 minutes and is also handled inside the display module.

### Secret Key

You'll need to provide your secret key in `secret.json` so the bot can log into your channel. Also, you *aren't* llcplays, so you'll need to change the preconfigured username and channel name. You *can* run the bot in the wrong channel. Please don't do this.

Example `secret.json`:

    {
		"secret": "oauth:charactersofsomekind"
    }

### Userlist

To enable userlist checking, create a userlist in `config.json`. The one provided by default admins me and my friends, and lets them on, while blocking everybody else. If you want to use this, you'll want to change that.

### Admin List

Several commands are supported in chat by default from a list of admins in the config file. They are:

>	`!die`: Cleans up the process and ends gracefully.  
>	`!restart`: Cleans up a little bit and restarts the IRC, display, emulator, etc.  
>	`!save`: Forces a savestate.  
>	`!load`: Forces a load of the last savestate.

### Banned Words

The bot supports automatically timing out people who say words from a certain list of restricted words in any casing. There is no Levenshtein distance checker or 1337speak decoder, so people can get around it pretty easily, but it's effective at stopping Twitch faces.

### Other Configuration

Configuration options should be straightforward and are in `config.json`.

License
-------

This is a traditional BSD 3-clause license.

    Copyright (c) 2014, Lyn Levenick
    All rights reserved.
    
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
    
    1. Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.
    
    2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.
    
    3. Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from this
    software without specific prior written permission.
    
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
    LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
	SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
	INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
	CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
	ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
	POSSIBILITY OF SUCH DAMAGE.
