scriptencoding utf-8
if filereadable(expand('$VIMRUNTIME/defaults.vim'))
    unlet! g:skip_defaults_vim
    source $VIMRUNTIME/defaults.vim
endif

set number
set expandtab
set shiftwidth=2
set softtabstop=2
