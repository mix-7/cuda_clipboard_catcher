import os
import cudatext as app # like insert time plugin 

from cudax_lib import get_translation

_   = get_translation(__file__)  # I18N
plugin_name = __name__
fn_config = os.path.join(app.app_path(app.APP_DIR_SETTINGS), 'cuda_clipboard_catcher.ini')


option_int = 100
option_bool = True
ed_current = None # вкладка, откуда вызван Clipboard catcher

COPY_CLIPS = False  # вначале плагин выключен

time_int=1000 # интервал опроса, мс 03.08.2023 16:24:57 Чт 31 215 wS \CudaText
 
last_clip = ''   # previous clipboard contents previous содержимое буфера обмена 03.08.2023 16:26:10 Чт 31 215 wS \CudaText 
new_clip = ''    # current clipboard contents текущее содержимое буфера обмена 

h_bar = app.app_proc(app.PROC_GET_MAIN_STATUSBAR, '') # хэндлер главного статусбара, см. плагин vim mode
#        color_back = app.statusbar_proc(h_bar, app.STATUSBAR_GET_COLOR_BACK, n_cell, tag=0, value=0xFF0000 )
color_back = app.statusbar_proc(h_bar, app.STATUSBAR_GET_COLOR_BACK) # цвет фона статусбара

n_cell = app.statusbar_proc(h_bar, app.STATUSBAR_ADD_CELL, index=-1, tag=0, value="CC ON")
            # if None - ?


def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'





class Command:


    def __init__(self):

        global option_int
        global option_bool
#        option_int = int(ini_read(fn_config, 'op', 'option_int', str(option_int)))
#        option_bool = str_to_bool(ini_read(fn_config, 'op', 'option_bool', bool_to_str(option_bool)))
        option_int = int(app.ini_read(fn_config, 'op', 'option_int', str(option_int)))
        option_bool = str_to_bool(app.ini_read(fn_config, 'op', 'option_bool', bool_to_str(option_bool)))

# # Сделать настройку конфига - время в мс устанавливать и разделитель фрагменто, как в Insert time 03.08.2023 16:17:08 Чт 31 215 WS \CudaText 

    def config(self):
        print("cuda_clipboard_catcher config(self), self, ed", self, ed)
        
        app.ini_write(fn_config, 'op', 'option_int', str(option_int))
        app.ini_write(fn_config, 'op', 'option_bool', bool_to_str(option_bool))
        app.file_open(fn_config)
        
# /home/one/.config/cudatext/py/cuda_clipboard_catcher/example_cuda_insert_time__init__.py        
#    def do_insert(self, s):
#        global ed_current 
#        
#        global last_clip    # previous clipboard contents previous содержимое буфера обмена 03.08.2023 16:26:10 Чт 31 215 wS \CudaText 
#        global new_clip     # current clipboard contents текущее содержимое буфера обмена 
#         
#        global COPY_CLIPS

# параметризовать количество пропускаемых строк до и после             xn, yn = ed_current.replace(x, y, x1, y1, "\n\n\n")


    def do_insert(self, s):
        global ed_current
        
        x, y, x1, y1 = ed_current.get_carets()[0]
        if y1>=0:
            if (y, x)>(y1, x1):
                x, y, x1, y1 = x1, y1, x, y
            ed_current.set_caret(x, y)

#            xn, yn = ed_current.replace(x, y, x1, y1, "\n\n")  # добавим строку - разделитель - параметризовать!
            xn, yn = ed_current.replace(x, y, x1, y1, "\n")  # добавим строку - разделитель - параметризовать!
            ed_current.set_caret(xn, yn, -1, -1, id=app.CARET_SET_ONE) # передвинуть курсор!
            xn, yn = ed_current.insert(xn, yn, s)
            ed_current.set_caret(xn, yn, -1, -1, id=app.CARET_SET_ONE) # передвинуть курсор!
        else:
#           xn, yn = ed_current.insert(x, y, "\n\n") # 0!
            xn, yn = ed_current.insert(x, y, "\n") # 0!
# не вставляет просто \n ? 05.08.2023 15:24:03  
            ed_current.set_caret(xn, yn, -1, -1, id=app.CARET_SET_ONE) # передвинуть курсор! 
            xn, yn = ed_current.insert(xn, yn, s)
            ed_current.set_caret(xn, yn, -1, -1, id=app.CARET_SET_ONE) # передвинуть курсор!
            # зачем ?
#       xn, yn = ed_current.insert(xn, yn, "\n\n\") # добавим строку - разделитель - параметризовать!
#        xn, yn = ed_current.insert(xn, yn, "\n\n") # добавим строку - разделитель - параметризовать!
        xn, yn = ed_current.insert(xn, yn, "\n") # добавим строку - разделитель - параметризовать!
#       2! \n, иначе только возврат каретки?

        ed_current.set_caret(0, yn, -1, -1, id=app.CARET_SET_ONE) # передвинуть курсор!
        app.msg_status(_('Clipboard inserted'))
    
#UVviewsoft forums • Просмотр темы - Cudatext Clipboard catcher (автоматическая вставка из буфера
#https://synwrite.sourceforge.net/forums/viewtopic.php?f=6&t=2793&p=17630#p17630
# Спасибо veksha и Alexey за совет, давший возможность реализовать этот плагин универсальным!  

    def timer_tick(self, *args):
        global last_clip    # previous clipboard contents previous содержимое буфера обмена 03.08.2023 16:26:10 Чт 31 215 wS \CudaText                                                                                             
        global new_clip     # current clipboard contents текущее содержимое буфера обмена 
        new_clip = app.app_proc(app.PROC_GET_CLIP, "")
        if new_clip != last_clip: # clipboard contents changed 03.08.2023 16:30:15 Чт 31 215 wS \CudaText
            last_clip =  new_clip # let's remember the new contents запомним новое содержимое
            self.do_insert(new_clip)             #self.do_insert(self, new_clip) self - по умолчанию?
        else:
            return # надо ли? 03.08.2023 16:33:44 Чт 31 215 wS \CudaText 
                  
    def run(self):
#??? что это?! 25.07.2023 16:41:42 Вт 30 206 wS \CudaText 
        global COPY_CLIPS
        global ed_current

        global last_clip    # previous clipboard contents previous содержимое буфера обмена 03.08.2023 16:26:10 Чт 31 215 wS \CudaText 
        global new_clip     # current clipboard contents текущее содержимое буфера обмена 
        global h_bar
        global n_cell
        global color_back
        h_my = app.ed.get_prop(app.PROP_HANDLE_SELF, '') # запомним, откуда, из какой вкладки был вызван Clipboard catche 04.08.2023 16:13:05 Пт 31 216 wS \CudaText 
        ed_current =  app.Editor(h_my)        # запомним, откуда, из какой вкладки был вызван Clipboard catche 04.08.2023 16:13:01 Пт 31 216 wS \CudaText 
#           ed - текущаяя вкладка
# ed_my = ed
# ed_my меняется при смене вкладки ???
#h_my = ed.get_prop(PROP_HANDLE_SELF, '')
#ed_my = Editor(h_my)  
#            h_my = app.ed.get_prop(PROP_HANDLE_SELF, '') # запомним, откуда, из какой вкладки был вызван Clipboard catche 04.08.2023 16:13:05 Пт 31 216 wS \CudaText  NameError: name 'PROP_HANDLE_SELF' is not defined 04.08.2023 16:14:37 Пт 31 216 wS \CudaText 

                
        if not COPY_CLIPS: # Clipboard catcher был выключен, включаем
#            h_my = app.ed.get_prop(app.PROP_HANDLE_SELF, '') # запомним, откуда, из какой вкладки был вызван Clipboard catche 04.08.2023 16:13:05 Пт 31 216 wS \CudaText 
#            ed_current =  app.Editor(h_my)        # запомним, откуда, из какой вкладки был вызван Clipboard catche 04.08.2023 16:13:01 Пт 31 216 wS \CudaText 
            COPY_CLIPS = True 
            app.statusbar_proc(h_bar, app.STATUSBAR_SET_CELL_TEXT, n_cell, tag=0, value="CC ON")
            app.statusbar_proc(h_bar, app.STATUSBAR_SET_CELL_COLOR_BACK, n_cell, tag=0, value=0xFF0000)

            app.msg_status("Clipboard Catcher ON", process_messages=False)
            new_clip = app.app_proc(app.PROC_GET_CLIP, "")
            last_clip = new_clip  
#           чтобы не вставлять сразу имеющееся содержимое буфера (проверка на обновление буфера) # 05.08.2023 08:56:07  

            app.timer_proc(app.TIMER_START, self.timer_tick, time_int)
        else: # иначе отключаем сопирование из буфера обмена
            app.timer_proc(app.TIMER_STOP, self.timer_tick, time_int)
#           msg_status("-сс", process_messages=False)
            COPY_CLIPS = False       
            ed_current = None

            app.statusbar_proc(h_bar, app.STATUSBAR_SET_CELL_TEXT, n_cell, tag=0, value="")
            app.statusbar_proc(h_bar, app.STATUSBAR_SET_CELL_COLOR_BACK, n_cell, tag=0, value=color_back)

            app.msg_status("Clipboard Catcher OFF", process_messages=False)
            
               

# Сделать настройку конфига - время в мс устанавливать, как в Insert time 03.08.2023 16:17:08 Чт 31 215 wS \CudaText 

 
# что это? 03.08.2023 16:15:27 Чт 31 215 wS \CudaText 
        s = '''
        file lines count: {cnt}
        option_int: {i}
        option_bool: {b}
        '''.format(
#             cnt = ed.get_line_count(),
#№             cnt = ed.get_line_count(), # 04.08.2023 13:20:29 Пт 31 216 wS \CudaText
#SyntaxError: invalid character '№' (U+2116)
#ERROR: Exception in CudaText for cuda_clipboard_catcher.run: SyntaxError: invalid character '№' (U+2116) (line 214, offset 1): '№             cnt = ed.get_line_count(), # 04.08.2023 13:20:29 Пт 31 216 wS \CudaText'
 
             cnt = app.ed.get_line_count(), # 04.08.2023 13:20:29 Пт 31 216 wS \CudaText 
             i = option_int,
             b = option_bool,
             )
        print("run(self) s= ", s)
#        msg_box(s, MB_OK)
# что это? 03.08.2023 16:15:27 Чт 31 215 wS \CudaText 

