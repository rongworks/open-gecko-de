# open-gecko-de

A custom linux desktop environment (currently only arch linux packages)

## Introduction

(//TODO: Screenshot)

## What it does
* A new Session called "Open Gecko" will be installed on the system
* OG will install Openbox with custom packages and configurations for your desktop.
* You will be able to switch sessions from/to Open Gecko
  * Your alternate Desktop session should not use Openbox (there can be conflicts otherwise)   
* Openbox will be configured with custom shortcuts, aliases etc.

## What it doesn't
* Open Gecko is no feature rich Desktop Environment,
 * Just the window manager, compositor etc. and some applications will be   installed
  * You will have to add your own packages for specific tasks (multimedia etc.)

## How to Install

-- **Warning !**

 This build is experimental.
 It will:

* Install and configure Openbox (and overwrite existing configurations)
* Install custom packages
* Overwrite existing configurations (If you already installed a package)

--

1. First check the configuration in [conf/packages.yml](../conf/packages.yml)
  * You can edit / add your own packages in the *packages* section
  * You can select / deselect packages by editing the *selected* attribute
  * You can change repositories / commands by editing the *repositories* section
  * You can edit custom files in the *custom_files* section
2. Run the installer
```bash
  cd <open-gecko-dir>/bin
  python open-gecko-py install
```
3. Follow the instructions in the installer

You can see the selected packages by calling `python open-gecko.py categories`

It will list the packages that will be installed grouped by category.

## Contents
(//TODO: list packages)

* packages, repositories, files are listed in [conf/packages.yml](../conf/packages.yml)
* custom files and config files can be found in the */dist* folder

## Other distributions / repositores

* You can edit the package and repository list in  [conf/packages.yml](../conf/packages.yml)
  * packages are installed by *repository::command *package::node_name* so you should change the yml-node name for another package name
* The installer *should* work on other system with modified config files (e.g. debian repositories)

## TODO

* Make a better readme
* Make installer script more stable
* Maybe add some packages
