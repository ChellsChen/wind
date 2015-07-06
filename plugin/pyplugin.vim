"导入python plugin"
"
let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\' )

" 如果是 C 项目的情况下, 用于保存头文件所在的目录
" 使用 vim 接口是为了方便与其它的项目进行数据交换
let g:frain_include_dirs = ''

"------------------------------ python -----------------------------------------
python <<EOF
import sys
import os
import vim

# add paths
root = os.path.dirname(vim.eval('s:script_folder_path'))
pylib_path    = os.path.join(root, 'wind/' )
sys.path.insert( 0, pylib_path )

import pyvim
exts_path = os.path.join(root, "exts" )
pyvim.load_plugin( exts_path )

#init im
from im import IM
EOF
"-------------------------------------------------------------------------------

function! Input_Monitor(tp, key)
    py IM("key", vim.eval("a:tp"), vim.eval("a:key"))
    return ''
endfunction

auto CursorHold   * py IM('event', "CursorHold")
auto CursorHoldI  * py IM('event', "CursorHoldI")
auto CompleteDone * py IM("prompt", "done")

map  <F2>          :update<cr>
imap <F2>          <esc>:update<cr>
map  <F7>          <esc>:MarkTo<cr>
imap <F7>          <esc>:MarkTo<cr>
map  <F9>          <esc>:TagJump<cr>
map  <F8>          <esc>:TagBack<cr>
map  <F10>         <esc>:FSearch<cr>
imap <F12>         <esc>:ProjectTerminal<cr><cr>
map  <F12>         <esc>:ProjectTerminal<cr><cr>
map  <2-LeftMouse> <esc>:MarkTo<cr>
map  <C-w>o        <esc>:ClearAllWin<cr>
vmap w=            <esc>:silent Align<cr>
imap <F11>         <esc>:GotoInc<cr>
map  <F11>         <esc>:GotoInc<cr>

map  <F4>          :ProjectSync<cr>
map  <tab>         :FrainFocus<cr>
map  <F6>          :Project<cr>
map *              viw""y/<C-R>0<CR>
vnoremap /         ""y/<C-R>0<CR>
