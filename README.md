# dotfiles
Sorted by application, for use with GNU Stow

## structure
*for every*

${XDG_CONFIG_HOME}/${PKGNAME}

*do*

${PKGNAME}/${XDG_CONFIG_HOME}/${PKGNAME}

## example
home/\n
    username/
        .config/
            uzbl/
                [...some files]
        .local/
            share/
                uzbl/
                    [...some files]
        .vim/
            [...some files]
        .bashrc
        .bash_profile
        .bash_logout
        .vimrc

*turns into*

home/
    username/
        .config/
        .local/
            .share/
        dotfiles/
            bash/
                .bashrc
                .bash_profile
                .bash_logout
            uzbl/
                .config/
                    uzbl/
                        [...some files]
                .local/
                    share/
                        uzbl/
                            [...some files]
            vim/
                .vim/
                    [...some files]
                .vimrc

*after which*

$ cd ~/dotfiles
$ stow bash
$ stow uzbl
$ stow vim

## reference
https://brandon.invergo.net/news/2012-05-26-using-gnu-stow-to-manage-your-dotfiles.html
