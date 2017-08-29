set ts=2
set noexpandtab
set softtabstop=2
"set expandtab
syntax on
"set number
set tabpagemax=100

"noremap <C-S-tab> :tabprevious<CR>
"noremap <C-tab> :tabnext<CR>
"noremap <C-PageDown> :tabprevious<CR>
"noremap <C-PageUp> :tabnext<CR>


"bépo mappings
"nnore ' n

noremap l o
noremap L O

noremap o r
noremap O R

noremap ç '

noremap ' n
noremap ? N

noremap t <Left>
noremap s <Down>
noremap r <Up>
noremap n <Right>

"let c_space_errors=1
"highlight RedundantSpaces ctermbg=red guibg=red
"match RedundantSpaces /\s\+$\| \+\ze\t/


"Source: http://vim.wikia.com/wiki/Highlight_unwanted_spaces
:highlight ExtraWhitespace ctermbg=red guibg=red
:highlight BogusTabs ctermbg=yellow guibg=yellow

"Source: http://vim.wikia.com/wiki/Highlight_unwanted_spaces
"Using this before the first colorscheme command will ensure that the highlight group
"gets created and is not cleared by future colorscheme commands.
:autocmd ColorScheme * highlight ExtraWhitespace ctermbg=red guibg=red
:autocmd ColorScheme * highlight BogusTabs ctermbg=yellow guibg=yellow

let extWSPat = '' "'/'
" Show trailing whitespace and spaces before a tab:
let extWSPat .= '\s\+$\| \+\ze\t'
" Show spaces used for indenting (so you use only tabs for indenting).
let extWSPat .= '\|^\t*\zs \+'
" Show any two consecutive spaces
let extWSPat .= '\|  \+'
let extWSPat .= '' "'/'
:autocmd BufRead * call matchadd('ExtraWhitespace', extWSPat, -1)

let bogTabPat = '' "'/'
" Show tabs that are not at the start of a line:
let bogTabPat .= '[^\t]\zs\t\+'
let bogTabPat .= '' "'/'
:autocmd BufRead * call matchadd('BogusTabs', bogTabPat, -2)

:autocmd FileType *text* set tw=0

colorscheme desert
set modeline

" This allows project specific vim settings
if filereadable($CUSTOM_VIMRC)
	source $CUSTOM_VIMRC
endif
