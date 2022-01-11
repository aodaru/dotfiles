set number
set mouse=a
set numberwidth=1
set clipboard=unnamed
syntax enable
set showcmd
set ruler
set cursorline
set encoding=UTF-8
set fileencoding=UTF-8
set showmatch
set sw=2
set relativenumber
set laststatus=2
set noshowmode

"Plugins
call plug#begin('~/.nvim/plugged')

"Themes
Plug 'morhetz/gruvbox'

"Syntax
Plug 'sheerun/vim-polyglot'

"IDE
Plug 'easymotion/vim-easymotion'
Plug 'w0rp/ale'
Plug 'yggdroot/indentline'

"Tree
Plug 'scrooloose/nerdtree'

"tmux
Plug 'benmills/vimux'
Plug 'christoomey/vim-tmux-navigator'

"StatusBar
" Plug 'maximbaz/lightline-ale'
" Plug 'itchyny/lightline.vim'
"

Plug 'tpope/vim-surround'
Plug 'tpope/vim-commentary'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'powerline/fonts'

call plug#end()

"Plugins-config
"Themes Setup
colorscheme gruvbox

let g:gruvbox_constrast_dark = "hard"

" Config airline
let g:airline_theme='powerlineish'
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#left_sep = ''
let g:airline#extensions#tabline#left_alt_sep = '|'
let g:airline#extensions#tabline#formatter = 'jsformatter'
let g:airline#extensions#whitespace#mixed_indent_algo = 1

let g:airline_powerline_fonts = 0

if !exists('g:airline_symbols')
    let g:airline_symbols = {}
endif

" airline symbols
let g:airline_left_sep = ''
let g:airline_left_alt_sep = ''
let g:airline_right_sep = ''
let g:airline_right_alt_sep = ''
let g:airline_symbols.branch = ''
let g:airline_symbols.readonly = ''
let g:airline_symbols.linenr = '| '


" Lightline
let g:lightline = {
			\ 'active': {
			\		'left': [['mode', 'paste'], [], ['relativepath', 'modified']],
			\		'right': [['filetype', 'percent', 'lineinfo'], ['gitbranch']]
			\	},
			\ 'inactive': {
			\		'left': [['inactive'], ['relativepath']],
			\		'right': [['bufnum']]
			\	},
			\	'component': {
			\		'bufnum': '%n',
			\		'inactive': 'inactive'
			\	},
			\	'component_function': {
			\		'gitbranch': 'fugitive#head',
			\	}
		\}

" Config indentLine
let g:vim_json_syntax_conceal = 0

" Config NERDTree
" ** autorun
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() == 0 && !exists("s:std_in") | NERDTree | endif

let NERDTreeQuitOnOpen=1

" Mapeo
let mapleader=" "

" coc-shortcut
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)

nmap <Leader>s <Plug>(easymotion-s2)
nmap <Leader>nt :NERDTreeFind<CR>
nmap <Leader>em <Plug>(emmet-expand-abbr)
nmap <Leader>emn <Plug>(emmet-move-next)
nmap <Leader>emp <Plug>(emmet-move-prev)

" Shortcut
nmap <Leader>w :w<CR>
nmap <Leader>q :q<CR>
nmap <Leader>tn :tabn<CR>
