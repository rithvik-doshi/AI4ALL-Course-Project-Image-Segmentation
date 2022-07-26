# Intro to Shell

You may have seen the terminal or cmd line app on your computer before, and if you're like me, you were probably very confused when you opened it up. There's no pictures, no GUI, just a bunch of text across your screen and an area to type in stuff. So here's an intro to the Unix shell, running either bash or zsh (which just means the version of the shell that you're running).

### What is the shell?

The shell is an interface for you to communicate with your computer. You can give your computer commands to execute. We will be going over the language in which you give these commands, as well as a few essential commands to navigate the system

### `man`

This will help you out so much as you learn how to use the terminal. Simply type `man`, followed by another command, in order to pull up the manual page for that command. Here's an example of pulling up the manual page for the copy command:

`$ man cp`

```
CP(1)                                General Commands Manual                               CP(1)

NAME
     cp – copy files

SYNOPSIS
     cp [-R [-H | -L | -P]] [-fi | -n] [-alpsvXx] source_file target_file
     cp [-R [-H | -L | -P]] [-fi | -n] [-alpsvXx] source_file ... target_directory

DESCRIPTION
     In the first synopsis form, the cp utility copies the contents of the source_file to the
     target_file.  In the second synopsis form, the contents of each named source_file is copied
     to the destination target_directory.  The names of the files themselves are not changed.
     If cp detects an attempt to copy a file to itself, the copy will fail.

     The following options are available:

     -H    If the -R option is specified, symbolic links on the command line are followed.
           (Symbolic links encountered in the tree traversal are not followed.)

     -L    If the -R option is specified, all symbolic links are followed.

     -P    If the -R option is specified, no symbolic links are followed.  This is the default.

     -R    If source_file desig... (there's other stuff but I didn't copy paste it all)
   
```

Basically, if you ever have any questions about how to use a command, use man to help figure it out.

### Quick intro to the filesystem

So as you may have seen before if you use the file explorer or Finder, our computers are organized via a file system. Essentially, files are broken up into files and directories. Simply put, files contain information, and directories contain files and other directories.

Now an example: imagine you have a folder called 'AI4ALL' with the following files and directories:

```
/home/
└-- AI4ALL/
	├-- File.jpg
	├-- File2.jpg
	├-- File3.txt
	├-- course_project/
	|	├-- README.md
	|	├-- project.py
	|	└-- test_it.sh
	└-- .gitignore
```

Out of these file names, you can recognize directories by the fact that they have no suffix (i.e. anything like .jpg, .py at the end). Additionally, they are followed by a forward slash, indicating that whatever follows is inside that directory. For example, if I were to write out the full path to File3.txt, it would be:

`/home/AI4ALL/File3.txt`

And if I were to write out the full path to project.py, it would be:

`/home/AI4ALL/course_project/project.py`

So, each file is nested within certain directories. This is important information for you to know, so that you can navigate through all the directories to get to a certain file.

BTW, dot files (files with a dot in front of the name) are hidden files, and usually contain some information that's not really meant to be publicly viewed. For example, the .gitignore file usually shows up in git repos (we'll talk about that soon) and contains a list of the files to ignore uploading to Github.

### `pwd`

`pwd` stands for 'print working directory', or, in other words, you're asking the computer where it's looking in right now. So suppose you're located here:

<pre>
/home/
└-- AI4ALL/
	├-- File.jpg
	├-- File2.jpg
	├-- File3.txt
	├-- <b>course_project/ *</b>
	|	├-- README.md
	|	├-- project.py
	|	└-- test_it.sh
	└-- .gitignore
</pre>

Then, if you type `pwd`, you'll get something like this:

`$ pwd`
`/home/AI4ALL/course_project/`

This is a good way to figure out where you are in the filesystem.

### `cd`

The cd command stands for 'change directories'. As you might guess, it's what you use to navigate through the filesystem. Suppose you are in /home/AI4ALL/ and you want to navigate into the course_project folder. You would type `cd` followed by the name of the directory you want to go to:

`cd course_project/`

At this point, you might be asking how to go backwards in the file system? Contrary to this rule, you cannot type in `cd AI4ALL/` to go backwards, because the shell is looking within course_project/ for a folder called AI4ALL/, which is not present. So, you'd have to specify the root path, or the path from the root of the filesystem, as such:

`cd /home/AI4ALL/`

Another way to go back one folder is by changing your directory to this: `cd ../`. The usage of .. signifies to the computer to go back by one level in the filesystem to the parent folder of your directory. So to go to the root directory, which is just `/`, we would do:

`cd ../../`

### `ls`

The ls command lists all the files in a directory. So say you're in the AI4ALL directory and want to know what's in it. You'd type:

`$ ls`
`File.jpg	File2.jpg	File3.txt	course_project/`

Sometimes, you can add options to a command, called flags, to slightly change what they do. This is not super important, but for example, if you wanted to show all files, including hidden ones, you would at the -a flag as such:

`$ ls -a`
`File.jpg	File2.jpg	File3.txt	course_project/	.gitignore`

You can also list a directory that you're not in. Say you're in /home/ and you want to know what's in course_project/. You would type the following:

`ls /home/AI4ALL/course_project/`
`README.md	project.py	test_it.sh`


### `cp` and `mv`

The `cp` and `mv` commands are commands to copy and move files. I'm not going to get into too much detail here, but you can always type `man cp` or `man mv` to figure out exactly how they work. You have to provide the name of the file/folder you want to copy/move, and the destination directory of where you want it to be copied/moved. Be careful with mv, as it is possible to lose data by messing around with it.

### `mkdir` and `touch`

The `mkdir` and `touch` commands creates a directory or a file respectively with the name that you provide. For example, `mkdir new_folder` would make new_folder/ in your current directory, and `touch main.py` would create a file called main.py. As always, use the man command to figure out more about it.

### `more` and `less`

These commands preview the contents of a file in the terminal in slightly different styles. Again, they work in the same syntax of "command filename", so use man on these for more details.

### `git` and Github overview

How do programmers share code with each other? The way we do this is by uploading our code and creating a source, from which programmers can get code, edit it, and publish it back to the source. Historically, when programmers began working with code over the internet, they had to figure out a way to make sure they weren't making edits over each other. So, they developed a locking system, where the code would be locked and impossible to edit while one person was editing it. This made sure that nothing was lost, but only one programmer would be able to use the code at a time, which made it super slow to develop with. The solution to this was a tool called `git`, or decentralized version control, where there are multiple copies of the code and many programmers can edit at the same time, but the source is smart about merging edits together. You don't have to worry about this too much, but be aware that git is a decentralized version control system that lets people share and simultaneously edit code.

Now, how do we get code from a repository (another word for the source)? We use the git command to clone an existing repository to your local machine in order to edit it. This is done as such:

`git clone https://github.com/your_github_username/your_repository_name`

Where you'd fill in the username and repo name depending on what you want to clone. If you go to the Github website, they help you out by giving you the link to copy and paste so that you don't have to type it all out.

Once you make changes to your repository, you have to stage your changes for a commit, then commit them, then push them back to the source. We won't get into this using the command line since there's a lot of potential for errors here. Consider using the GitHub Desktop app to help streamline things, it provides a nice GUI and an explanation for any errors you may come across.

### Bonus commands!

##### `say`

This one is just funny. If you're running macOS, you can make your computer talk by typing `say "Sentence goes here"`. You can pull a bunch of pranks with this one

##### `vim`

Vim is a powerful and lightweight text editor using the terminal! It was invented before Microsoft invented MS Word, and it's kind of regarded as the OG text editor. It's really complicated though, and you can't really use the mouse to do anything in it. Though it has a steep learning curve, it's worth it later on if you need to really quickly edit a file to do something, or even as a full blown development environment. Check it out if you'd like!

##### `ssh` and `sshfs`

Oftentimes, you might need to connect to a remote desktop or computer in order to do work. This may be because you're using a supercomputer or a microcomputer, which usually don't come with displays, or because you're working from a different location than that computer and over the internet. `ssh` starts a remote shell session on the specified machine, while `sshfs` mounts a folder from that machine to your local machine so that you can transfer files seamlessly between the two. If you ever connect a Raspberry Pi or Arduino to the internet, this might be worth it rather than trying to connect a regular display straight to the machine.

### Conclusion

Hopefully, you learned a little bit about the shell and how to navigate it. There's SO much more to it than what's written here, but the beauty of that is that there's so much to learn and so much you can do with it. Have fun!

`Rithvik Doshi`
