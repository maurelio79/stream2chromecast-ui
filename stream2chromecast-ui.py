#!/usr/bin/env python
   
import pygtk
pygtk.require('2.0')
import gtk, gobject, vte
import os

		
def display_error(data):
	dialogError = gtk.MessageDialog(None, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
	dialogError.set_markup(data)
	dialogError.run()
	dialogError.destroy()

class Stream2Chromecast:

  def delete_event(self, widget, data):
    print "Exiting..."
    gtk.main_quit()
    return False

  def set_vol(obj, widget):
    vol = obj.slider.get_value()
    video = obj.buttonFile.get_filename()
    if not video:
      pass
    else:
      os.system('/opt/stream2chromecast/stream2chromecast.py -setvol %s' % (vol))

  def pause_event(obj, widget):
    os.system('/opt/stream2chromecast/stream2chromecast.py -pause')

  def continue_event (obj, widget):
    os.system('/opt/stream2chromecast/stream2chromecast.py -continue')

  def stop_event(obj, widget):
    v = obj.term
    os.system('/opt/stream2chromecast/stream2chromecast.py -stop ')
    v.feed_child('clear \n')

  def start_event(obj, widget):
    video = obj.buttonFile.get_filename()
    if not video:
      display_error("Select a video File")
      return 1
    v = obj.term
    v.show()
    if (obj.checkButton.get_active() == True):
      v.feed_child('/opt/stream2chromecast/stream2chromecast.py -transcode %s \n' % (video))
    else:
      v.feed_child('/opt/stream2chromecast/stream2chromecast.py %s \n' % (video))


    

  def __init__(self):
    
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_title("Stream2Chromcast UI")
    self.window.set_border_width(25)
    #self.window.set_resizable(False)
    self.window.set_default_size(600, -1)

    self.window.connect("delete_event", self.delete_event)

    self.boxContainer = gtk.VBox(False, 15)
    self.window.add(self.boxContainer)
    self.boxContainer.show()

    self.descriptionLabel = gtk.Label("Simple UI to use stream2chromecast application\n")
    self.boxContainer.pack_start(self.descriptionLabel)
    self.descriptionLabel.show()

    # Box with button file and checkbutton
    self.box1 = gtk.HBox(False, 5)
    self.boxContainer.pack_start(self.box1)
    self.box1.show()

    self.fileLabel = gtk.Label("Select a video to stream to your chromecast")
    self.box1.pack_start(self.fileLabel)
    self.fileLabel.show()

    self.buttonFile = gtk.FileChooserButton("Title")
    self.box1.pack_start(self.buttonFile, True)
    self.buttonFile.set_width_chars(50)
    self.buttonFile.show()

    self.volumeLabel = gtk.Label("Volume: ")
    self.boxContainer.pack_start(self.volumeLabel)
    self.volumeLabel.show()

    self.adj1 = gtk.Adjustment(0.5, 0, 1.0, 0.1, 0, 0)

    self.sliderBox = gtk.HBox(False, 5)
    self.boxContainer.pack_start(self.sliderBox)
    self.sliderBox.show()
    
    self.slider = gtk.HScale(self.adj1)
    self.sliderBox.pack_start(self.slider)
    self.slider.show()

    self.bottomBox = gtk.HBox(False, 5)
    self.boxContainer.pack_start(self.bottomBox)
    self.bottomBox.show()

    self.submitButton = gtk.Button("Play")
    self.bottomBox.pack_start(self.submitButton)
    self.submitButton.show()

    self.pauseButton = gtk.Button("Pause")
    self.bottomBox.pack_start(self.pauseButton)
    self.pauseButton.show()

    self.continueButton = gtk.Button("Continue")
    self.bottomBox.pack_start(self.continueButton)
    self.continueButton.show()

    self.stopButton = gtk.Button("Stop")
    self.bottomBox.pack_start(self.stopButton)
    self.stopButton.show()

    self.checkButton = gtk.CheckButton()
    self.checkButton.set_label("Transcode")
    self.boxContainer.pack_start(self.checkButton, False)
    self.checkButton.show()
    
    self.termBox = gtk.HBox(False, 5)
    self.boxContainer.pack_start(self.termBox)
    self.termBox.show()

    self.term = vte.Terminal()
    self.term.connect("child-exited", lambda w: gtk.main_quit())
    self.pid = self.term.fork_command()
    self.term.set_emulation('xterm')
    self.termBox.pack_start(self.term)

    # Here every handler
    self.submitButton.connect("clicked", self.start_event)
    self.pauseButton.connect("clicked", self.pause_event)
    self.stopButton.connect("clicked", self.stop_event)
    self.continueButton.connect("clicked", self.continue_event)
    self.slider.connect("value-changed", self.set_vol)

    self.window.show()
		
  def main(self):
      gtk.main()
		
if __name__ == "__main__":
  stream2chromecast = Stream2Chromecast()
  stream2chromecast.main()
