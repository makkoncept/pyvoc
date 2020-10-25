<p align="center">
  <img  algin="center" height="150" src="https://raw.githubusercontent.com/makkoncept/pyvoc/master/.art/pyvoc_logo.png" />
   <h3 align="center">Cross-platform dictionary and vocabulary building command line tool</h3> 
  <p align="center">
    <a href="https://github.com/makkoncept/pyvoc/blob/master/LICENSE">
      <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
    </a>
    <a href="https://github.com/makkoncept/pyvoc">
    	<img src="https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-blue.svg" alt="platforms" />
    </a>
    <a href="https://pypi.org/project/pyvoc">
      <img src="https://img.shields.io/pypi/v/pyvoc.svg" />
    </a>
    <a href="https://pepy.tech/project/pyvoc">
      <img src="https://pepy.tech/badge/pyvoc" />
    </a>
    <a href="https://pepy.tech/project/pyvoc">
      <img src="https://pepy.tech/badge/pyvoc/month" />
    </a>
  </p>
</p>

---

# Pyvoc

<p align="center">
  <a href="https://asciinema.org/a/367832" target="_blank"><img src="https://asciinema.org/a/367832.svg" /></a>
</p>

**Use it to improve your english vocabulary, brush up some word meanings or as a simple command line dictionary.**

---

Jump to:

- [Installation](#Installation)
- [Usage](#Usage)
- [Groups](#Groups)
- [Examples](#Examples)

## Installation

Install it using pip. Just run:

```bash
pip3 install pyvoc
```

## Usage

After installing pyvoc, run `pyvoc -w word` to _automatically create necessary config files_ in your home directory.

- Fetch meaning of word

```
pyvoc -w word
```

- Fetch meaning of word and add it to vocabulary group:

```
pyoc word -a
```

- Take quiz from vocabulary group 101 (default questions are 5):

```
pyvoc -q 101
```

- Take quiz of 25 questions from vocabulary group 101 :

```
pyvoc -q 101 -n 25
```

_read some more [examples](#Examples)_

```
➜ pyvoc -h
usage: pyvoc [-h] [-v] [-w <word>] [-a] [-g <group_num>] [-r <group_num>] [-q <group_num>] [-n <no_of_questions>] [-l]

Command line dictionary and vocabulary building tool.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Print version of pyvoc and exit
  -w <word>             Give meaning of WORD
  -a, --add-word        Use to add WORD to vocabulary group
  -g <group_num>        Use to specify the vocabulary group no.(1-10) to add the WORD to
  -r <group_num>        Revise the vocabulary group you mention
  -q <group_num>        Start quiz from the vocabulary group you mention
  -n <no_of_questions>  Mention the number of questions of quiz.
  -l, --list            Lists all vocabulary groups present
```

## groups

pyvoc lets you add words to vocabulary groups, which you can later revise or take quiz from.

- 3 **custom groups of 800 words each** (words taken from GRE and SAT preparation websites) already present. These groups are 101, 102 and 103.
- 10 groups of 50 words are **reserved** for the user. These groups are 1 - 10.
- you can specify a group from 1-10 using [-g] option.

## Examples

### add word to a specific group

```
pyvoc word -a -g 5
```

Fetch meaning of the word and add it to vocabulary group 5. **Use this option to organize words however you like.**

**_for example_**

- alphabatically
- words from books you have been reading
- parts of speech
- increasing difficulty

---

### revise a group

```
pyvoc -r 7
```

Revise word meaning of vocabulary group 7(if present) in random order.

---

### show group list

```
pyvoc --list
```

Lists all group numbers along with their size.
