import os
import cudatext as app # like insert time plugin 

from cudax_lib import get_translation

_   = get_translation(__file__)  # I18N
plugin_name = __name__


COPY_CLIPS = False  # at first, the plugin is disabled

time_int=1000 # timer interval ms интервал опроса, мс 
separator="\n" # line separator 

last_clip = ''   # previous clipboard contents previous  
new_clip = ''    # current clipboard contents  

h_bar = app.app_proc(app.PROC_GET_MAIN_STATUSBAR, '') # main statusbar handler  (like vim mode plugin)
color_back = app.statusbar_proc(h_bar, app.STATUSBAR_GET_COLOR_BACK) # status bar background color
n_cell = app.statusbar_proc(h_bar, app.STATUSBAR_ADD_CELL, index=-1, tag=0, value="CC ON")            # if None - ?


class Command:


    def do_insert(self, s):
        global ed_current
        global separator
        x, y, x1, y1 = ed_current.get_carets()[0]
        if y1>=0:
            if (y, x)>(y1, x1):
                x, y, x1, y1 = x1, y1, x, y
            ed_current.set_caret(x, y)
            xn, yn = ed_current.replace(x, y, x1, y1, "\n")  # insert separator 
            ed_current.set_caret(xn, yn, -1, -1, id=app.CARET_SET_ONE) # move caret
            xn, yn = ed_current.insert(xn, yn, s)
            ed_current.set_caret(xn, yn, -1, -1, id=app.CARET_SET_ONE) 
        else:
            xn, yn = ed_current.insert(x, y, "\n") # 0!
            ed_current.set_caret(xn, yn, -1, -1, id=app.CARET_SET_ONE)   
            xn, yn = ed_current.insert(xn, yn, s)
            ed_current.set_caret(xn, yn, -1, -1, id=app.CARET_SET_ONE) 
        xn, yn = ed_current.insert(xn, yn, "\n") 
        ed_current.set_caret(0, yn, -1, -1, id=app.CARET_SET_ONE) 
        app.msg_status(_('Clipboard inserted'))
    
    def timer_tick(self, *args): # from #https://synwrite.sourceforge.net/forums/viewtopic.php?f=6&t=2793&p=17630#p17630
        global last_clip    # previous clipboard contents                                                                                            
        global new_clip     # current clipboard contents  
        new_clip = app.app_proc(app.PROC_GET_CLIP, "")
        if new_clip != last_clip: # clipboard contents changed 
            last_clip =  new_clip # let's remember the new contents 
            self.do_insert(new_clip)             # self - by default
        else:
            return #  
                  
    def run(self):
        global COPY_CLIPS
        global ed_current

        global last_clip    # previous clipboard contents  
        global new_clip     # current clipboard contents 
        global h_bar
        global n_cell
        global color_back
        global time_int
         
        h_my = app.ed.get_prop(app.PROP_HANDLE_SELF, '') # запомним, откуда, из какой вкладки был вызван Clipboard catcher
        ed_current =  app.Editor(h_my)        # запомним, откуда, из какой вкладки был вызван Clipboard catcher  

        if not COPY_CLIPS: # Clipboard catcher was turned off, turn on
            COPY_CLIPS = True 
            app.statusbar_proc(h_bar, app.STATUSBAR_SET_CELL_TEXT, n_cell, tag=0, value="CC ON")
            app.statusbar_proc(h_bar, app.STATUSBAR_SET_CELL_COLOR_BACK, n_cell, tag=0, value=0xFF0000)

            app.msg_status("Clipboard Catcher ON", process_messages=False)
            new_clip = app.app_proc(app.PROC_GET_CLIP, "")
            last_clip = new_clip #    in order not to immediately insert the existing contents of the buffer (when checking for buffer updates)  
            app.timer_proc(app.TIMER_START, self.timer_tick, time_int)
        else: # otherwise, disable copying from the clipboard
            app.timer_proc(app.TIMER_STOP, self.timer_tick, time_int)
            COPY_CLIPS = False       
            ed_current = None
            app.statusbar_proc(h_bar, app.STATUSBAR_SET_CELL_TEXT, n_cell, tag=0, value="")
            app.statusbar_proc(h_bar, app.STATUSBAR_SET_CELL_COLOR_BACK, n_cell, tag=0, value=color_back)
            app.msg_status("Clipboard Catcher OFF", process_messages=False)
