au BufRead,BufNewFile *.py set textwidth=79 " lines longer than 79 columns will be broken
au BufRead,BufNewFile *.pt set filetype=html.pt
set shiftwidth=4  " operation >> indents 4 columns; << unindents 4 columns
set tabstop=4     " an hard TAB displays as 4 columns
set expandtab     " insert spaces when hitting TABs
set softtabstop=4 " insert/delete 4 spaces when hitting a TAB/BACKSPACE
set shiftround    " round indent to multiple of 'shiftwidth'
set autoindent    " align the new line indent with the previous line
filetype indent on
let python_highlight_all=1
syntax on
