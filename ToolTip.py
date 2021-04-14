# -*- coding: utf-8 -*-

import tkinter as tk
import traceback
import sys
import math



####################################################################################################
###
###     ToolTip
###
###     This class allows to add a ToolTip to a Tkinter widget.
###
###     Author:  Stefan Rosewig
###
###     V 1.0       first stable release
###     V 1.0.1     minor fix on display
###     V 1.0.2     version info function added
###     V 1.1.0     improvements exception handling
###
###    Author :  Chad Unterschultz
###
###    V 2.0.0     Jan 21, 2021 Second stable release, updated for canvas tooltip functionality
###    V 2.0.1     Jan 22, 2021 Resolved "Error in bgerror: can't invoke "tk" command: application has been destroyed"
###                             Resolved by catching and checking for .after(...) handler
###    V 2.0.2     Feb 8, 2021  Multiple Event handlers tied to one widget will cause one to replace another
###                             Resolved by using "add = '+'" option to ensure event handler is added to a list of
###                             operations to preform upon event.

debugging = False
VERSION     = (2,0,2)
VERSION_s   = "%s.%s.%s" %VERSION


class ToolTip(object):
    """ Class creating a tooltip on a widget
        Usage: ToolTip(<widget>, <window>, <canvas>, <scrollbarX>, <scrollbarY>, <scrollregionX>, <scrollregionY>, <text>, <tooltipText>)
        <widget>         = required, TkInter widget to create TooTip on, i.e. tk.Button, re
        <window>         = optional, if using on a canvas object
        <canvas>         = optional, if using on a canvas object
        <scrollregionX>  = optional, if scrollbar X-axis
        <scrollregiony>  = optional, if scrollbar Y-axis
        <scrollbarX>     = optional, if your canvas scrolls in the x-axis
        <scrollbarY>     = optional, if your canvas  scrolls in the Y-axis
        <text>           = The text to be shown as ToolTip
        <time>           = Time in milliseconds until fase out of the ToolTip, 2000ms.
                           If <time> is less than 1000ms, the Tooltip is displayed
                           until the mouse has left the widget.
        <font>    = font to be used, by default ("arial","8","normal")
        <fg>      = foreground color (text), default 'black'
        <bg>      = background color, default 'lightyellow'
    """

    def __init__(self, widget, window = None, canvas = None, scrollbarX = None, scrollbarY = None, scrollregionX = None, scrollregionY = None,  text='Default', time=2000, font=('arial','8','normal'), fg='black', bg='lightyellow'):
        """ ToolTip initialisation, widget is mandatory """

        self.window = window
        self.widget = widget                                                    #   The widget the tooltip is for
        self.canvas = canvas
        self.scrollbarX = scrollbarX
        self.scrollbarY = scrollbarY
        self.scrollregionX = scrollregionX
        self.scrollregionY = scrollregionY





        if type(text) != str:                                                   #   String expected
            raise TypeError("<text> must be a string")
        self.text = text                                                        #   Tooltip text
        if type(time) != int:                                                   #   Integer expected
            raise TypeError("<time> must be an integer")
        self.time = time                                                        #   Display time for ToolTip
        if type(font) != tuple:                                                 #   tuple (font) expected
            raise TypeError("<font> must be a font tuple")
        self.font = font                                                        #   Font to be used
        self.fg = fg                                                            #   foreground color (textcolor)
        self.bg = bg                                                            #   background color

        if (window and canvas) == None:
            self.widget.update()
            self.widget.bind("<Enter>", self.tkinter_widget_enter, add = '+')   #   If mouse enters widget area
            self.widget.bind("<Leave>", self.tkinter_widget_leave, add = '+')   #   If mouse leaves widget area
            self.widget.focus_displayof()                                       #   Identify tkinter widget

        elif ( ( (window and canvas) != None )
                         and
               ( (scrollbarX and scrollbarY and scrollregionX and
                  scrollregionY) == None ) ):
            self.canvas.update()
            self.canvas.focus_displayof()                                       #   Identify tkinter widget
            self.canvas.tag_bind(self.widget, "<Enter>",                        #   If mouse enters widget area
                                 self.canvas_widget_enter, add = '+')           #   add = '+', event handler added to action, not replaced any existing event handlers
            self.canvas.tag_bind(self.widget, "<Leave>",                        #   If mouse leaves widget area
                                 self.canvas_widget_leave, add = '+')            #   add = '+', event handler added to action, not replaced any existing event handlers

        elif ( ( ( window and canvas) != None
                and
                (scrollbarX and scrollbarY and scrollregionX
                 and scrollregionY) != None ) ):
            self.canvas.update()
            self.canvas.focus_displayof()                                       #   Identify tkinter widget
            self.canvas.tag_bind(self.widget, "<Enter>",                        #   If mouse enters widget area
                                 self.canvas_widget_scroll_enter, add = '+')    #   add = '+', event handler added to action, not replaced any existing event handlers
            self.canvas.tag_bind(self.widget, "<Leave>",                        #   If mouse leaves widget area
                                 self.canvas_widget_scroll_leave, add = '+')    #   add = '+', event handler added to action, not replaced any existing event handlers
            if debugging == True: self.canvas.bind('<ButtonPress>', self.onClick, add = '+')
        else:
            if debugging == True: print("Error")




    def version_info():
        """ return version info Major, Minor, Subversion """
        return VERSION_s

    def config(self, text=None, time=None, font=None, fg=None, bg=None):
        """ configuration of ToolTip """
        if text != None:
            if type(text) != str:                                               #   String expected
                raise TypeError("<text> must be a string")
            self.text = text                                                    #   Tooltip text
        if time != None:
            if type(time) != int:                                               #   Integer expected
                raise TypeError("<time> must be an integer")
            self.time = time                                                    #   Display time for ToolTip
        if font != None:
            if type(font) != tuple:                                             #   tuple (font) expected
                raise TypeError("<font> must be a font tuple")
            self.font = font                                                    #   Font to be used
        if fg != None:
            self.fg = fg                                                        #   foreground color (textcolor)
        if bg != None:
            self.bg = bg                                                        #   background color


    def tkinter_widget_enter(self, event=None):
        """ Mouse Cursor has Entered Tkinter widget, display tooltip """
        self.widget.update()                                                    #
        print("*** Test ***")
        #print("Info ", self.canvas.itemcget(self.widget, "SystemWindowFrame"))
        #self.tw = tk.Toplevel(self.widget)                                      #   Create a toplevel widget

        if self.widget.winfo_exists():                                         # Prevents drawing on a widget that doesn't exist
            parentName = self.widget.winfo_parent()
            parent     = self.widget._nametowidget(parentName)                 # event.widget is your widget
            frameParentName = parent.winfo_parent()
            frameParent     = parent._nametowidget(frameParentName)            # parent is your widget
        else:                                                                  # Exit if the widget doesn't exist (do I need to clean house at this point?)
            return



        self.tw = tk.Toplevel(parent)
        self.tw.overrideredirect(True)                                          #   No frame for the widget
        scr_w = self.widget.winfo_screenwidth()                                 #   Get screen resolution width
        scr_h = self.widget.winfo_screenheight()                                #   Get screen resolution height
        #x_ = self.tw.winfo_pointerx()                                           #   Pointer X-position, not used for anything here
        #y_ = self.tw.winfo_pointery()                                           #   Pointer Y-position, not used for anything here
        try:
            self.tooltiplabel = tk.Label(self.tw,                               #   Label in the widget
                     text = self.text,                                          #   Text to show
                     foreground = self.fg,                                      #   define foregroundcolor
                     background = self.bg,                                      #   define backgroundcolor
                     relief = 'ridge',                                          #   Display Style
                     borderwidth = 1,                                           #   1 Pixel Border
                     font = self.font).pack(ipadx=5)                            #   Define Font
        except tk.TclError:
            traceback.print_exc(limit=2, file=sys.stdout)                       #   print Traceback
            if debugging == True: print("Error has occured")
            if "tw" in self.__dict__.keys() :                                   #   Only attempt to destroy if it exists
                self.tw.destroy()                                               #   close tooltip
                del self.tw                                                     #   Remove "tw" to prevent errors with <leave> method
                if debugging == True: print(self.__dict__.keys())
                return
        else:
            self.tw.update()                                                    #   Display ToolTip
            try:
                w_posy = self.widget.winfo_rooty()                              #   Get widget Y Position (Top)
                w_posx = self.widget.winfo_rootx()                              #   Get widget X Position (left)
                if debugging == True: print(" X: ", w_posx, " Y: ", w_posy)
                w_height = self.widget.winfo_height()                           #   Get widget height
                w_width = self.widget.winfo_width()                             #   Get widget width
                t_height = self.tw.winfo_height()                               #   Get ToolTip heigth
                t_width = self.tw.winfo_width()                                 #   Get ToolTip width
                if t_height + self.widget.winfo_rooty() + 50 > scr_h:           #   Check if ToolTip is out of screen bottom
                    y = w_posy - t_height                                       #   Position it above widget
                else:
                    y = w_posy + w_height                                       #   Position it below widget
                if t_width + self.widget.winfo_rootx() + w_width + 5 > scr_w:   #   Check if ToolTip is out of screen right
                    x = w_posx - t_width - 5                                    #   Position it on the left
                else:
                    x = w_posx + w_width + 5                                    #   Position it on the right
                self.tw.wm_geometry("+%d+%d" % (x, y))                          #   Set ToolTip Position
            except :
                pass                                                            #   if bad window path nothing happens
            if self.time > 0:
                if "tw" in self.__dict__.keys() :
                    self.catch = self.tw.after(self.time, self.tkinter_widget_leave)                          #   Start timer

    def tkinter_widget_leave(self, event=None):
        """ Mouse Cursor has Left Tkinter widget, Remove tooltip """
        try:
            if "tw" in self.__dict__.keys() :                                       #   Check if Already Destroyed
                if "catch" in self.__dict__.keys():                                 #   Destroy scheduled for the future?
                    self.tw.after_cancel(self.catch)                                #   Cancel future destroy if already doing destroy
                if debugging == True: print("about to destroy")                     #   Sanity check, check it exists before destroy
                if "tw" in self.__dict__.keys():                                    #   Sanity check, check it exists before destroy
                    self.tw.destroy()                                               #   Destroy ToolTip
                    if debugging == True: print(self.__dict__.keys())
                    del self.tw                                                     #   Delete handler from List
                    if debugging == True: print(self.__dict__.keys())
        except:
            pass



    def canvas_widget_enter(self, event = None):
        """ Mouse Cursor has Entered Canvas widget, display tooltip """
        self.tw = tk.Toplevel(self.window)                                              #   Create a toplevel widget, would it be more efficient as a separate thread or process?
        self.tw.overrideredirect(True)                                                  #   No frame for the widget
        scr_w = self.window.winfo_screenwidth()                                         #   Get screen resolution width
        scr_h = self.window.winfo_screenheight()                                        #   Get screen resolution height
        if debugging == True: print("Screen width: ", scr_w)
        if debugging == True: print("Screen Height: ", scr_h)
        mouse_posx = self.tw.winfo_pointerx()                                            #   Mouse Cursor X-position
        mouse_posy = self.tw.winfo_pointery()                                            #   Mouse Cursor Y-position
        if debugging == True: print("Pointer X", mouse_posx, "Pointer Y", mouse_posy)

        try:
            self.tooltiplabel = tk.Label(self.tw,                                       #   Label in the widget
                     text = self.text,                                                  #   Text to show
                     foreground = self.fg,                                              #   define foregroundcolor
                     background = self.bg,                                              #   define backgroundcolor
                     relief = 'ridge',                                                  #   Display Style
                     borderwidth = 1,                                                   #   1 Pixel Border
                     font = self.font).pack(ipadx=5)                                    #   Define Font
        except tk.TclError:
            if debugging == True: print("Error has occured")
            if debugging == True: print(self.__dict__.keys())
            traceback.print_exc(limit=2, file=sys.stdout)                               #   print Traceback
            if "tw" in self.__dict__.keys() :                                           #   Check if it exists before tryin to destroy (actually needed or not?)
                if debugging == True: print("about to destroy")
                self.tw.destroy()                                                       #   Close ToolTip if label creation error
                del self.tw                                                             #   Delete Handler from List
                return
        else:
            self.tw.update()                                                            #   Display ToolTip
            try:
                t_height = self.tw.winfo_height()                                       #   Get ToolTip Window heigth
                t_width = self.tw.winfo_width()                                         #   Get ToolTip Window width

                if debugging == True: print("ToolTip Window Height: ", t_height)
                if debugging == True: print("ToolTip Window Width: ", t_width)

                positionX = mouse_posx + 10                                             #   10 pixels Right of Cursor
                positionY = mouse_posy + 10                                             #   10 pixels Down of Cursor

                if debugging == True: print("positionX", positionX)
                if debugging == True: print("positionY", positionY)

                if (positionX + t_width) > scr_w:                                       #   Too Close to edge of Screen in X-Axis?
                    positionX = positionX - t_width                                     #   Move over to the Left of the Cursor Instead
                if (positionY + t_height) > scr_h:                                      #   Too Close to Edge of Screen in Y-Axis?
                    positionY = positionY - t_height                                    #   Move over to above the Cursor Instead

                if debugging == True: print("positionX", positionX)
                if debugging == True: print("positionY", positionY)

                self.tw.wm_geometry("+%d+%d" % (positionX, positionY))                  #   Set ToolTip Position
                self.canvas.update()                                                    #   Is this actually needed?
            except :
                pass                                                                    #   if bad window path nothing happens
            if self.time > 0:
                if "tw" in self.__dict__.keys() :
                    self.catch = self.tw.after(self.time, self.canvas_widget_leave)     #   Start timer print()


    def canvas_widget_leave(self, event = None):
        """ Mouse Cursor has Left Canvas widget, Remove tooltip """
        try:
            if "tw" in self.__dict__.keys() :                                           #   Check if Already Destroyed
                if "catch" in self.__dict__.keys():                                     #   Destroy scheduled for the future?
                    self.tw.after_cancel(self.catch)                                    #   Cancel future destroy if already doing destroy
                if "tw" in self.__dict__.keys() :                                       #   Sanity check, check it exists before destroy
                    if debugging == True: print("about to destroy")
                    self.tw.destroy()                                                   #   Destroy ToolTip
                    if debugging == True: print(self.__dict__.keys())
                    del self.tw                                                         #   Delete handler from List
                    if debugging == True: print(self.__dict__.keys())
        except:
            pass






    def canvas_widget_scroll_enter(self, event = None):
        """ Mouse Cursor has Entered a Canvas Widget, where the canvas has X and Y scrollbars, display tooltip """
        if debugging == True: print("**** canvas_widget_scroll_enter ***")
        if debugging == True: print("Contents: ", self.__dict__.keys())
        self.tw = tk.Toplevel(self.window)                                          #   Create a toplevel widget, more efficient as parallel process or thread?
        if debugging == True: print("Contents: ", self.__dict__.keys())
        self.tw.overrideredirect(True)                                              #   No frame for the widget
        scr_w = self.window.winfo_screenwidth()                                     #   Get screen resolution width
        scr_h = self.window.winfo_screenheight()                                    #   Get screen resolution height
        if debugging == True: print("Screen width: ", scr_w)
        if debugging == True: print("Screen Height: ", scr_h)

        try:
            if "tw" in self.__dict__.keys() :
                if debugging == True: print("Make Label")
                self.tooltiplabel = tk.Label(self.tw,                                   #   Label in the widget
                                             text = self.text,                          #   Text to show
                                             foreground = self.fg,                      #   define foregroundcolor
                                             background = self.bg,                      #   define backgroundcolor
                                             relief = 'ridge',                          #   Display Style
                                             borderwidth = 1,                           #   1 Pixel Border
                                             font = self.font).pack(ipadx=5)            #   Define Font
        except tk.TclError:
            if debugging == True: print("tk.TclError")
            traceback.print_exc(limit=2,file=sys.stdout)                                #   print Traceback
            print("Error has occured")
            print(self.__dict__.keys())

            if "tw" in self.__dict__.keys() :
                if debugging == True: print("about to destroy")
                self.tw.destroy()                                                       #   Close ToolTip if label creation error
                del self.tw                                                             #   Delete Handler from List
                return

        else:
            self.tw.update()                                                            #   Display ToolTip
            try:
                coordinates = self.canvas.bbox(self.widget)
                if debugging == True: print("Widget Coordinates: ", coordinates)
                                                                                #   Widget Absolute Coordinates in Canvas
                w_posx = coordinates[0]                                         #   Absolute Widget in Canvas X position, top left corne
                w_posy = coordinates[1]                                         #   Absolute Widget in Canvas Y position, top left corner

                if debugging == True: print("Absolute Widget X: ", w_posx)
                if debugging == True: print("Absolute Widget Y: ", w_posy)

                if debugging == True: print(self.scrollbarX.get()[0] * self.scrollregionX)




                w_posx = w_posx - self.scrollbarX.get()[0] * self.scrollregionX   #   Convert Absolute X to Relative X Position
                w_posy = w_posy - self.scrollbarY.get()[0] * self.scrollregionY   #   Convert Absolute Y to Relative Y Position

                if debugging == True: print("Relative Widget X: ", w_posx)
                if debugging == True: print("Relative Widget Y: ", w_posy)

                                                                                #   Window Top Left Corner Absolute Pos in Screen
                window_y = self.window.winfo_rooty()                            #   Window Top Left X coordinate
                window_x = self.window.winfo_rootx()                            #   Window Top Right Y Coordinate

                if debugging == True: print("Window Absolute X: ", window_x)
                if debugging == True: print("Window Absolute Y: ", window_y)

                canvas_x = self.canvas.winfo_rootx()                            #   Absolute Canvas position X in screen, Top Left Corner
                canvas_y = self.canvas.winfo_rooty()                            #   Absolute Canvas position Y in screen, Top Left Corner

                if debugging == True: print("Canvas Absolute X position in Screen: ", canvas_x)
                if debugging == True: print("Canvas Absolute Y position in Screen: ", canvas_y)

                w_height = coordinates[3] - coordinates[1]                           #   Widget Height (in pixels)
                w_width = coordinates[2] - coordinates[0]                            #   Widget Width (in pixels)


                t_height = self.tw.winfo_height()                                    #   Get ToolTip heigth
                t_width = self.tw.winfo_width()                                      #   Get ToolTip width

                positionX =  w_posx + canvas_x + w_width                             #   ToolTip left corner X Position
                positionY =  w_posy + canvas_y + w_height                            #   ToolTip Left Corner Y Position

                if debugging == True: print("Proposed Tooltip position X: ", positionX)
                if debugging == True: print("Proposed Tooltip position Y: ", positionY)

                if ((positionX + t_width + 50) > scr_w):                             #   Check if ToolTip is out of Screen on Right
                    positionX = canvas_x + w_posx - t_width - 5                      #   If too far right, put on left side
                if ((positionY + t_height + 50) > scr_h):                            #   Check if ToolTip is out of Screen on Bottom
                    positionY = canvas_y + w_posy - t_height - 5                     #   If too far down, put above

                if debugging == True: print("Corrected Tooltip Position X", positionX)
                if debugging == True: print("Corrected Tooltip Position Y", positionY)

                self.tw.wm_geometry("+%d+%d" % (positionX, positionY))               #   Set ToolTip Position
                self.canvas.update()
            except :
                pass                                                                 #   if bad window path nothing happens
            if self.time > 0:
                if "tw" in self.__dict__.keys() :
                    self.catch = self.tw.after(self.time, self.canvas_widget_scroll_leave)       #   Start timer print()

    def canvas_widget_scroll_leave(self, event = None):
        """ Mouse Cursor has Left a Canvas Widget, where the canvas has X and Y scrollbars, Remove tooltip """
        try:
            if "tw" in self.__dict__.keys() :                                       #   Check if Already Destroyed
                if "catch" in self.__dict__.keys():                                 #   Destroy scheduled for the future?
                    self.tw.after_cancel(self.catch)                                #   Cancel future destroy if already doing destroy
                if debugging == True: print("about to destroy")                     #   Sanity check, check it exists before destroy
                if "tw" in self.__dict__.keys():                                    #   Sanity check, check it exists before destroy
                    self.tw.destroy()                                               #   Destroy ToolTip
                    if debugging == True: print(self.__dict__.keys())
                    del self.tw                                                     #   Delete handler from List
                    if debugging == True: print(self.__dict__.keys())
        except:
            pass

    def onClick(self, event):
        if debugging == True: print("Click Relative Coordinates in canvas: ", event.x, event.y)
        if debugging == True: print("Click Absolute Coordinates in canvas", self.window.winfo_pointerx(), self.window.winfo_pointery())
















if __name__ == "__main__":

    if debugging == True: print("Library File Test")

    root = tk.Tk()
    root.title("ToolTip Demo")

    Widget = tk.Button(root, text="Example 1")
    Widget.pack(anchor=tk.N, side=tk.TOP)
    Example = 1     #   Default Settings
    Tip1 = ToolTip(Widget, text="Default Settings")


    canvas_window1 = tk.Canvas(root, height = 400, width = 400, bg = 'grey')
    canvas_window1.pack(anchor = tk.N)

    Canvas_Text = canvas_window1.create_text(5, 5, text = "ToolTip Test   98098", anchor = "nw")

    Tip2 = ToolTip(Canvas_Text, root, canvas_window1)



    Canvas_Frame = tk.Frame(root)
    Canvas_Frame.pack(anchor = tk.N)

    scrollregion = (0, 0, 1200, 1200)
    canvas_window2 = tk.Canvas(Canvas_Frame, height = 400, width = 400,  scrollregion = scrollregion,  bg = 'white')

    Canvas_Text2 = canvas_window2.create_text(5, 5, text = "ToolTip Test with Scrollbars", anchor = "nw")
    canvas_window2_scrollx = tk.Scrollbar(Canvas_Frame, orient = tk.HORIZONTAL)
    canvas_window2_scrolly = tk.Scrollbar(Canvas_Frame, orient = tk.VERTICAL)

    canvas_window2.config( xscrollcommand = canvas_window2_scrollx.set)
    canvas_window2.config( yscrollcommand = canvas_window2_scrolly.set)

    canvas_window2_scrollx.config(command = canvas_window2.xview)
    canvas_window2_scrolly.config(command = canvas_window2.yview)

    canvas_window2_scrollx.pack(side = tk.BOTTOM, expand = tk.YES, fill = tk.X)
    canvas_window2_scrolly.pack(side = tk.RIGHT, expand = tk.YES, fill = tk.Y)
    canvas_window2.pack(expand = tk.YES, fill = tk.BOTH)

    """

    parent1 = canvas_window2.winfo_toplevel()

    print(    parent1 is root)
    print(    parent1 is canvas_window1)
    print(    parent1 is canvas_window2)

    parent2 = canvas_window2.winfo_parent()

    print( parent2 is root)
    print( parent2 is canvas_window1         )
    print( parent2 is canvas_window2)

    parent3 = parent2.winfo_parent()

    """



    Tip3 = ToolTip(Canvas_Text2, root, canvas_window2, canvas_window2_scrollx, canvas_window2_scrolly, scrollregion[2], scrollregion[3])
    root.mainloop()

