import datetime
from collections import OrderedDict

import kivy
kivy.require('1.0.9')

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup

import confwriter


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Controller(FloatLayout):
    switch1 = ObjectProperty(None)
    switch2 = ObjectProperty(None)
    loadfile = ObjectProperty(None)
    tabbedpanel = ObjectProperty(None)
    path = None
    filename = None

    def do_cancel(self):
        self.app.stop()

    def do_ok(self):
        values = []

        # Global values
        update_keys = ['update', 'update_fw']
        for key in update_keys:
            values.append(self.apply_fix(key, self.get_value(self.ids[key])))

        # Switchs values
        for key, value in self.switch1.ids.items() + self.switch2.ids.items():
            values.append(self.apply_fix(key, self.get_value(value)))
        # Global values
        global_keys = ['fps', 'camera_name', 'dcf_prefix']
        for key in global_keys:
            values.append(self.apply_fix(key, self.get_value(self.ids[key])))

        # Insert date
        date = self.get_date()
        values.insert(-1, date)
        # return path
        # return model(tab name)
        confwriter.confmaker(self.path, self.tabbedpanel.current_tab.text, values)

    def get_value(self, obj):
        if isinstance(obj, Switch):
            return obj.active
        if isinstance(obj, Spinner):
            return obj.text
        if isinstance(obj, Slider):
            return obj.value

    def apply_fix(self, key, value):
        if key in ['update', 'update_fw']:
            return ['NO', 'YES'][value]
        if value in [True, False]:
            return int(value)
        if value is None:
            return ''
        if key in ['res', 'br', 'ae', 'awb', 'fps'] and value is not '':
            return getattr(self.app, key + '_values')[value]

        return value

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.path = path
        # self.filename = len(filename) and filename[0]
        self.dismiss_popup()

    def get_date(self):
        date = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        return date


class ControllerApp(App):
    res_values = OrderedDict((
        ('(A)1920x1080 30fps (NTSC)/25fps (PAL)', 'A'),
        ('(B)1280x960  30fps (NTSC)/25fps (PAL)', 'B'),
        ('(C)1280x720  30fps (NTSC)/25fps (PAL)', 'C'),
        ('(D)1280x720  60fps (NTSC)/50fps (PAL)', 'D'),
        ('(E)848x480  30fps (NTSC)/25fps (PAL)', 'E'),
        ('(F)848x480  60fps (NTSC)/50fps (PAL)', 'F'),
        ('(G)848x480  120fps (NTSC)/100fps (PAL)', 'G'),
        ('(P/1)5Mp at intervals of 1 picture per second', 'P/1'),
        ('(P/3)5Mp at intervals of 3 pictures per second', 'P/3'),
        ('(P/5)5Mp at intervals of 5 pictures per second', 'P/5'),
        ('(P/10)5Mp at intervals of 10 pictures per second', 'P/10'),
        ('(P/15)5Mp at intervals of 15 pictures per second', 'P/15'),
        ('(P/20)5Mp at intervals of 20 pictures per second', 'P/20'),
        ('(P/30)5Mp at intervals of 30 pictures per second', 'P/30'),
        ('(P/45)5Mp at intervals of 45 pictures per second', 'P/45'),
        ('(P/60)5Mp at intervals of 60 pictures per second', 'P/60'),
    ))

    br_values = OrderedDict(
        (('(H)High', 'H'),
         ('(M)Medium', 'M'),
         ('(L)Low', 'L')
    ))

    ae_values = OrderedDict(
        (('(C)Center', 'C'),
         ('(A)Average', 'A'),
         ('(S)Spot', 'S')
    ))

    awb_values = OrderedDict(
        (('(0)AUTO', '0'),
         ('(1)2800K_Incandescent', '1'),
         ('(2)4000K_Fluorescent', '2'),
         ('(3)5000K_DaylightD50', '3'),
         ('(4)6500K_DaylightD65', '4'),
         ('(5)7500k_Cloudy', '5'),
         ('(6)9000k_Shade', '6'),
         ('(7)10000k_XenonHID', '7')
    ))

    fps_values = OrderedDict(
        (('(50)25/50/100fps', '50'),
         ('(60)30/60/120fps', '60')
    ))

    def build(self):
        root = Controller()
        root.app = self
        return root


if __name__ == '__main__':
    ControllerApp().run()
