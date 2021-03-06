"vimlib 中用于辅助的vim script"


"""""""""""""""""""""""""""""""""""SelMenu"""""""""""""""""""""""""""""""""""
"函数中用于传递返回数据的变量"
let g:omniresult= []
let g:omnicol = 0
let g:wind_commands_complete = []
"补全回调函数"
"
let s:invoke_other_fun = 0
let g:wind_with_ycm = -4

function! wind#Prompt(findstart, base)
    if a:findstart
        py IM('prompt', 'findstart')
        if g:wind_with_ycm  == g:omnicol
            let s:invoke_other_fun = 1
            let g:omnicol =  youcompleteme#OmniComplete(a:findstart, '')
        endif
        if g:omnicol > -1
            call feedkeys( "\<C-P>", 'n' )
        endif

        return g:omnicol
    else
        if s:invoke_other_fun
            let s:invoke_other_fun = 0
            return youcompleteme#OmniComplete(a:findstart, a:base)
        else
            py IM('prompt', 'base', vim.eval('a:base'))
            return g:omniresult
        endif
    endif
endfunction

function! wind#CommandsComplete(A, L, P)
    py IM("cmd_complete", vim.eval("a:A"), vim.eval("a:L"), vim.eval("a:P"))
    return g:wind_commands_complete
endfunction
