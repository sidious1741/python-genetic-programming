import wx
import threading
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
import numpy as np
import os

class hal:
    def __init__(self, controller_class):
        self.app = wx.App()
        self.mainframe = HalFrame(None, controller_class)
        self.app.MainLoop()

"""
>   keep testing until pause is hit. grey >| and |< buttons
||  pause after the current gen is tested
>|  
|<
<<  reset
have a thing like "pause at generation |__|"
"""

ID_QUIT = 1

[wxID_FRAME1, wxID_FRAME1BUTTON2, wxID_FRAME1NEXT_BUTTON, wxID_FRAME1PANEL1, 
 wxID_FRAME1PANEL2, wxID_FRAME1PANEL3, wxID_FRAME1GRAPH_BOX, 
 wxID_FRAME1STATUS_BOX, 
] = [wx.NewId() for _init_ctrls in range(8)]

class HalFrame(wx.Frame):

##############

    def _init_coll_boxSizer3_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.next_button, 0, border=0, flag=0)
        parent.AddWindow(self.button2, 0, border=0, flag=0)

    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.panel2, 0, border=0, flag=0)
        parent.AddWindow(self.panel3, 0, border=0, flag=0)

    def _init_coll_boxSizer2_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.graph_box, 0, border=0, flag=0)
        parent.AddWindow(self.status_box, 0, border=0, flag=0)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizer2 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizer3 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self._init_coll_boxSizer2_Items(self.boxSizer2)
        self._init_coll_boxSizer3_Items(self.boxSizer3)

        self.panel1.SetSizer(self.boxSizer1)
        self.panel2.SetSizer(self.boxSizer3)
        self.panel3.SetSizer(self.boxSizer2)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(101, 46), size=wx.Size(1032, 678),
              style=wx.DEFAULT_FRAME_STYLE, title='Frame1')
        self.SetClientSize(wx.Size(1032, 678))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(1032, 678),
              style=wx.TAB_TRAVERSAL)

        self.panel2 = wx.Panel(id=wxID_FRAME1PANEL2, name='panel2',
              parent=self.panel1, pos=wx.Point(0, 0), size=wx.Size(170, 27),
              style=wx.TAB_TRAVERSAL)

        self.panel3 = wx.Panel(id=wxID_FRAME1PANEL3, name='panel3',
              parent=self.panel1, pos=wx.Point(0, 27), size=wx.Size(928, 629),
              style=wx.TAB_TRAVERSAL)

        self.graph_box = wx.StaticBitmap(bitmap=wx.NullBitmap,
              id=wxID_FRAME1GRAPH_BOX, name=u'graph_box', parent=self.panel3,
              pos=wx.Point(0, 0), size=wx.Size(512, 632), style=0)

        self.status_box = wx.StaticText(id=wxID_FRAME1STATUS_BOX,
              label=u'status_box', name=u'status_box', parent=self.panel3,
              pos=wx.Point(512, 0), size=wx.Size(280, 352), style=0)

        self.next_button = wx.Button(id=wxID_FRAME1NEXT_BUTTON, label=u'next',
              name=u'next_button', parent=self.panel2, pos=wx.Point(0, 0),
              size=wx.Size(85, 27), style=0)

        self.button2 = wx.Button(id=wxID_FRAME1BUTTON2, label='button2',
              name='button2', parent=self.panel2, pos=wx.Point(85, 0),
              size=wx.Size(85, 27), style=0)

        self._init_sizers()
    def __init__(self, parent, controller_class):
        self._init_ctrls(parent)


##############3

        #def __init__(self, parent, controller_class):
        #wx.Frame.__init__(self, parent, title='HAL', size=(500,500))
        self.genetic_controller = controller_class()
        """
        menubar = wx.MenuBar()

        file = wx.Menu()
        file.Append(-1, '&New')
        file.Append(-1, '&Open')
        file.Append(-1, '&Save')
        file.AppendSeparator()

        imp = wx.Menu()
        imp.Append(-1, 'Import newsfeed list...')
        imp.Append(-1, 'Import bookmarks...')
        imp.Append(-1, 'Import mail...')

        file.AppendMenu(-1, 'I&mport', imp)

        quit = wx.MenuItem(file, ID_QUIT, '&Quit\tCtrl+W')
        #quit.SetBitmap(wx.Bitmap('icons/exit.png'))
        file.AppendItem(quit)
        
        self.Bind(wx.EVT_MENU, self.OnQuit, id=ID_QUIT)

        menubar.Append(file, '&File')
        self.SetMenuBar(menubar)
        """

        """
        box0 = wx.BoxSizer(wx.VERTICAL)
        box1 = wx.BoxSizer(wx.HORIZONTAL)


        self.Z = []


        top_panel = wx.Panel(self, -1)
        play_button = wx.Button(top_panel, -1, 'play')
        next_button = wx.Button(top_panel, -1, 'next')
        stop_button = wx.Button(top_panel, -1, 'stop')
        reset_button = wx.Button(top_panel, -1, 'reset')

        box1.AddMany([play_button, next_button, stop_button, reset_button])

        top_panel.SetSizer(box1)


        box2 = wx.BoxSizer(wx.HORIZONTAL)
        mid_panel = wx.Panel(self, -1)
        self.graph_box = wx.StaticBitmap(mid_panel, -1)
        self.status_box = wx.StaticText(mid_panel, -1, 'text')
        box2.AddMany([self.graph_box, self.status_box])
        mid_panel.SetSizer(box2)


        box0.AddMany([top_panel, mid_panel])
        self.SetSizer(box0)


        """
        self.Z = []
        self.pause_at_generation = 0



        self.check_status_timer = wx.Timer(self, 1)
        self.Bind(wx.EVT_TIMER, self.OnCheckStatus, self.check_status_timer)
        self.check_status_timer.Start(100)

        self.pause_at_generation = 20
        self.making_generation = False
        self.made_generation = False
        self.testing_generation = False
        self.tested_generation = False

        #self.text = wx.StaticText(self, -1, '0', (40, 60))
        self.update_data_timer = wx.Timer(self, 2)
        self.Bind(wx.EVT_TIMER, self.OnUpdateData, self.update_data_timer)
        self.update_data_timer.Start(2000)

        self.Show(True)
        print 'havent built anything'

    def OnCheckStatus(self, event):
        # make sure current_individual is up-to-date
        self.status_box.SetLabel(str(self.genetic_controller.generation) + '\t' + str(self.genetic_controller.individual))
        if self.genetic_controller.generation < self.pause_at_generation:
            if not self.made_generation and not self.making_generation:
                self.making_generation = True
                self.gthread = threading.Thread(target=self.make_generation)
                self.gthread.start()
            elif not self.tested_generation and not self.testing_generation:
                self.testing_generation = True
                self.gthread = threading.Thread(target=self.test_generation)
                self.gthread.start()
            elif self.tested_generation:
                self.made_generation = False
                self.tested_generation = False
                self.OnUpdateData('asf')
        self.check_status_timer.Start(100)

    def make_generation(self):
        if self.genetic_controller.generation == 0:
            self.genetic_controller.build_initial_structures()
        else:
            self.genetic_controller.make_next_generation()
        self.making_generation = False
        self.made_generation = True

    def test_generation(self):
        self.genetic_controller.test_generation()
        self.testing_generation = False
        self.tested_generation = True

    def OnUpdateData(self, event):
        #plotting stuff

        # what if individual is None
        if self.genetic_controller.individual != None:
            hist, edges = np.histogram([round(self.genetic_controller.s(i,self.genetic_controller.generation)) for i in range(self.genetic_controller.individual)], bins = self.genetic_controller.bins, range=(0,self.genetic_controller.r_max))
        else:
            hist, edges = np.histogram([round(self.genetic_controller.s(i,self.genetic_controller.generation)) for i in range(self.genetic_controller.M)], bins = self.genetic_controller.bins, range=(0,self.genetic_controller.r_max))
        Y = []
        for i in range(len(hist)):
            Y.append( (edges[i]+edges[i+1])/2. )
        if len(self.Z)-1 < self.genetic_controller.generation:
            self.Z.append(list(hist))
        else:
            self.Z[-1] = list(hist)


        X, Y = np.meshgrid(range(0,self.genetic_controller.generation+1), Y)

        fig = plt.figure()
        #ax = fig.gca(projection='3d')
        ax = fig.add_subplot(121)
        ax.set_axis_bgcolor("#bdb76b")

        Z = np.array(self.Z)
        Z = Z.transpose()

        #surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet,
        #        linewidth=0, antialiased=False)
        #ax.set_zlim3d(-1.01, 1.01)
        ax.pcolormesh(X,Y,Z, shading='gouraud', figure=fig)
        

        #ax.w_zaxis.set_major_locator(LinearLocator(10))
        #ax.w_zaxis.set_major_formatter(FormatStrFormatter('%.03f'))

        #fig.colorbar(surf, shrink=0.5, aspect=5)
        #plt.colorbar()
        #plt.show()

        #except Exception:
        #    print 'need matplotlib version 1 or greater. you have version ' + matplotlib.__version__

        #t = range(0,len(self.average_fitness))

        #l_worst, = plt.plot(t, self.worst_fitness, 'g-o')
        #l_average, = plt.plot(t, self.average_fitness, 'b-D')
        #l_best, = plt.plot(t, self.best_fitness, 'r-s')

        #plt.legend( (l_worst, l_average, l_best), ('worst', 'average', 'best'), 'upper right', shadow=True)
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.title('Fitness Curves')
        #axis([0,len(self.average_fitness),0,])
        #plt.show()
        fig.savefig('graph.png')


        # should reload sooner
        if os.path.exists('graph.png'):
            self.graph_box.SetBitmap( wx.BitmapFromImage( wx.Image('graph.png', wx.BITMAP_TYPE_PNG) ) )


        self.update_data_timer.Start(2000)

    def OnQuit(self, event):
        self.gthread.stop()
    
    """
    def graph
        #st = time.time()
        time.sleep(1)
        t = range(0,len(self.average_fitness))

        l_worst, = plt.plot(t, self.worst_fitness, 'g-o', figure=fig)
        l_average, = plt.plot(t, self.average_fitness, 'b-D', figure=fig)
        l_best, = plt.plot(t, self.best_fitness, 'r-s', figure=fig)

        #plt.legend( (l_worst, l_average, l_best), ('worst', 'average', 'best'), 'upper right', shadow=True, figure=fig)
        
        
        fig
    """

"""
class GraphFrame(wx.Frame)


generation
    fitness, hits, time to test, average time per fitness case, depth
        number of individuals
    average (fitness, hits, time to test, average time per fitness case, depth)

3d graphs but at one generation or current generation

"""
