from datetime import datetime
from math import cos, sin, pi
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import *
from kivy.graphics import Line, Color
from kivy.uix.widget import Widget
from kivy.utils import get_hex_from_color
from kivy.lang.builder import Builder
KV = """
<SettingLabel@Label>:
    size_hint_y: None
    height: '30dp'

<SettingSlider@Slider>:
    size_hint_y: None
    height: '40dp'

<SettingSpacer@Widget>:
    size_hint_y: None
    height: '30dp'

<SettingToggle@ToggleButton>:
    text: "Enabled" if self.state == 'down' else "Disabled"
    size_hint_y: None
    height: '40dp'

RelativeLayout:
    digital_x: 0.5
    digital_y: 0.2
    digital_size: 1
    FractalClock:
        id: fractalclock
    ClockIndicators:
        id: clockindicators
    Label:
        id: digitalclock
        pos: (root.digital_x * root.width) - (root.width/2), (root.digital_y * root.height) - (root.height/2)
        font_size: root.digital_size * root.height/10
        text: str(fractalclock.hour) + ':' + str(fractalclock.minute).zfill(2) + ':' + str(int(fractalclock.second)).zfill(2)
    BoxLayout:
        canvas.before:
            Color:
                rgba: 0.5, 0.5, 0.5, 0.4
            Rectangle:
                size: self.size
                pos: self.pos
        id: settingsarea
        hidden: True
        size_hint_x: 0.333
        pos: (root.width - self.width) if not self.hidden else root.width, 0
        orientation: 'vertical'
        ScrollView:
            scroll_type: ['bars', 'content']
            do_scroll_x: False
            do_scroll_y: True
            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                SettingLabel:
                    text: "Clock Scale: " + str(round(fractalclock.scale, 3))
                SettingSlider:
                    value: fractalclock.scale
                    on_value: fractalclock.scale = self.value
                    min: 0.1
                    max: 1
                SettingLabel:
                    text: "Clock Hand Width: " + str(round(fractalclock.overlay_width, 3))
                SettingSlider:
                    value: fractalclock.overlay_width
                    on_value: fractalclock.overlay_width = self.value
                    min: 0.5
                    max: 5
                SettingLabel:
                    text: "Clock Hand Color: "
                ColorWheel:
                    size_hint_y: None
                    height: self.width / 2
                    color: fractalclock.hand_color
                    on_color: fractalclock.hand_color = self.color[:3]

                SettingSpacer:

                SettingLabel:
                    text: "Angle offset: " + str(round(fractalclock.angle_offset, 3))
                SettingSlider:
                    value: fractalclock.angle_offset
                    on_value: fractalclock.angle_offset = self.value
                    min: 0
                    max: 1
                SettingLabel:
                    text: "Max Iterations: " + str(fractalclock.max_iteration)
                SettingSlider:
                    value: fractalclock.max_iteration
                    on_value: fractalclock.max_iteration = int(round(self.value))
                    min: 0
                    max: 10
                SettingLabel:
                    text: "Transparency Maximum: " + str(round(fractalclock.color_value, 3))
                SettingSlider:
                    value: fractalclock.color_value
                    on_value: fractalclock.color_value = self.value
                    min: 0
                    max: 1
                SettingLabel:
                    text: "Transparency Minimum: " + str(round(fractalclock.color_minimum, 3))
                SettingSlider:
                    value: fractalclock.color_minimum
                    on_value: fractalclock.color_minimum = self.value
                    min: 0
                    max: 1
                SettingLabel:
                    text: "Fractal Line Width: " + str(round(fractalclock.subhand_width, 3))
                SettingSlider:
                    value: fractalclock.subhand_width
                    on_value: fractalclock.subhand_width = self.value
                    min: 0.5
                    max: 5
                SettingLabel:
                    text: "Fractal Color: "
                ColorWheel:
                    size_hint_y: None
                    height: self.width / 2
                    color: fractalclock.fractal_color
                    on_color: fractalclock.fractal_color = self.color[:3]

                SettingSpacer:

                SettingLabel:
                    text: "Clock Indicators Opacity: "
                SettingSlider:
                    value: clockindicators.opacity
                    on_value: clockindicators.opacity = self.value
                    min: 0
                    max: 1
                SettingLabel:
                    text: "Clock Indicators Scale: "
                SettingSlider:
                    value: clockindicators.scale
                    on_value: clockindicators.scale = self.value
                    min: 0.1
                    max: 1
                SettingLabel:
                    text: "Clock Indicator Line Width: "
                SettingSlider:
                    value: clockindicators.line_width
                    on_value: clockindicators.line_width = self.value
                    min: 0.5
                    max: 5
                SettingLabel:
                    text: "Clock Indicator Line Length: "
                SettingSlider:
                    value: clockindicators.indicator_size
                    on_value: clockindicators.indicator_size = self.value
                    min: 0.5
                    max: 3
                SettingLabel:
                    text: "Anti-Screen Burn: "
                SettingToggle:
                    state: 'down' if clockindicators.anti_screen_burn else 'normal'
                    on_state: clockindicators.anti_screen_burn = True if self.state == 'down' else False
                SettingLabel:
                    text: "Clock Indicators Color: "
                ColorWheel:
                    size_hint_y: None
                    height: self.width / 2
                    color: clockindicators.indicators_color
                    on_color: clockindicators.indicators_color = self.color[:3]

                SettingSpacer:

                SettingLabel:
                    text: "Digital Clock Opacity: "
                SettingSlider:
                    value: digitalclock.opacity
                    on_value: digitalclock.opacity = self.value
                    min: 0
                    max: 1
                SettingLabel:
                    text: "Digital Clock X Position: "
                SettingSlider:
                    value: root.digital_x
                    on_value: root.digital_x = self.value
                    min: 0
                    max: 1
                SettingLabel:
                    text: "Digital Clock Y Position: "
                SettingSlider:
                    value: root.digital_y
                    on_value: root.digital_y = self.value
                    min: 0
                    max: 1
                SettingLabel:
                    text: "Digital Clock Size: "
                SettingSlider:
                    value: root.digital_size
                    on_value: root.digital_size = self.value
                    min: 0.01
                    max: 4
                SettingLabel:
                    text: "Digital Clock Color: "
                ColorWheel:
                    size_hint_y: None
                    height: self.width / 2
                    color: digitalclock.color
                    on_color: digitalclock.color = self.color[:3]

        BoxLayout:
            size_hint_y: None
            height: '40dp'
            orientation: 'horizontal'
            Button:
                text: 'Save'
                on_release: app.save_settings()
            Button:
                text: 'Reset'
                on_release: app.reset_settings()
    Button:
        opacity: 0
        pos: 0 if settingsarea.hidden else (0 - settingsarea.width), 0
        on_release: settingsarea.hidden = not settingsarea.hidden
"""

settings = {
    'angle_offset': 0.4,
    'max_iteration': 6,
    'color_value': 0.4,
    'color_minimum': 0,
    'scale': 0.5,
    'subhand_width': 1,
    'overlay_width': 1.5,
    'indicator_width': 1.5,
    'indicator_size': 1,
    'digital_opacity': 0,
    'circle_opacity': 0,
    'circle_scale': 1,
    'digital_x': 0.5,
    'digital_y': 0.1,
    'digital_size': 1,
    'anti_screen_burn': False,
    'digital_color': '#FFFFFF',
    'indicators_color': '#FFFFFF',
    'fractal_color': '#FFFFFF',
    'hand_color': '#FFFFFF'
}


class ClockIndicators(Widget):
    line_width = NumericProperty(1)
    scale = NumericProperty(1)
    center_pos = ListProperty([0, 0])
    radius = NumericProperty(1)
    indicator_size = NumericProperty(1)
    indicators_color = ColorProperty([1, 1, 1])
    anti_screen_burn = BooleanProperty(False)
    anti_screen_burn_amount = []
    anti_screen_burn_index = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(0, 100):
            self.anti_screen_burn_amount.append(i / 100)
        for i in range(100, 0, -1):
            self.anti_screen_burn_amount.append(i / 100)
        Clock.schedule_interval(self.update_anti_burn, 1)

    def update_anti_burn(self, *_):
        if self.anti_screen_burn:
            self.anti_screen_burn_index += 1
            if self.anti_screen_burn_index > 199:
                self.anti_screen_burn_index = 0
            self.redraw()

    def redraw(self):
        self.center_pos = [self.pos[0] + self.width / 2, self.pos[1] + self.height / 2]
        self.radius = min(self.center_pos[0], self.center_pos[1]) * self.scale
        mid_x = self.pos[0] + self.width / 2
        mid_y = self.pos[1] + self.height / 2
        self.canvas.clear()
        self.canvas.add(Color(*self.indicators_color[:3]))
        indicator_size = 0.025 * self.indicator_size
        if self.anti_screen_burn:
            indicator_offset = self.indicator_size * 0.1 * self.anti_screen_burn_amount[self.anti_screen_burn_index] - indicator_size - indicator_size
        else:
            indicator_offset = 0
        inner_radius = self.radius * self.scale * (1 - indicator_size + indicator_offset)
        outer_radius = self.radius * self.scale * (1 + indicator_size + indicator_offset)
        for index in range(0, 12):
            radians = index / 6 * pi
            start_x = mid_x + inner_radius * sin(radians)
            start_y = mid_y + inner_radius * cos(radians)
            end_x = mid_x + outer_radius * sin(radians)
            end_y = mid_y + outer_radius * cos(radians)
            self.canvas.add(Line(width=self.line_width, points=[start_x, start_y, end_x, end_y]))

    def on_anti_screen_burn(self, *_):
        self.redraw()

    def on_indicators_color(self, *_):
        self.redraw()

    def on_indicator_size(self, *_):
        self.redraw()

    def on_size(self, *_):
        self.redraw()

    def on_scale(self, *_):
        self.redraw()

    def on_line_width(self, *_):
        self.redraw()


class FractalLine(Line):
    twopi = 6.283185307179586
    angle_offset = 0.5
    color_value = 1
    color_subtract = 0.05
    color = [1, 1, 1]
    start_pos = [0, 0]
    angle_percent = 0
    length = 1
    iteration = 1
    max_iteration = 2
    canvas = None
    sub_minute = None
    sub_second = None

    def __init__(self, canvas, color=[1, 1, 1], color_subtract=0, angle_offset=0, iteration=1, max_iteration=0, color_value=1, **kwargs):
        self.color = color
        self.color_subtract = color_subtract
        self.angle_offset = angle_offset
        self.canvas = canvas
        self.iteration = iteration
        self.max_iteration = max_iteration
        self.color_value = color_value
        super().__init__(**kwargs)
        if self.iteration <= self.max_iteration:
            sub_color = self.color_value - self.color_subtract
            sub_iteration = self.iteration + 1
            self.sub_minute = FractalLine(width=self.width, color=self.color, color_subtract=self.color_subtract, angle_offset=self.angle_offset, canvas=self.canvas, iteration=sub_iteration, max_iteration=self.max_iteration, color_value=sub_color)
            self.sub_second = FractalLine(width=self.width, color=self.color, color_subtract=self.color_subtract, angle_offset=self.angle_offset, canvas=self.canvas, iteration=sub_iteration, max_iteration=self.max_iteration, color_value=sub_color)
            self.canvas.add(Color(*self.color[:3], sub_color))
            self.canvas.add(self.sub_minute)
            self.canvas.add(self.sub_second)

    def hand_loc(self, time, length):
        radians = time * self.twopi
        return length * sin(radians), length * cos(radians)

    def update(self, pos, angle, angles, length):
        self.start_pos = pos
        self.angle_percent = angle
        self.length = length
        offset = self.hand_loc(self.angle_percent, self.length)
        end_pos = (self.start_pos[0] + offset[0], self.start_pos[1] + offset[1])
        self.points = [self.start_pos[0], self.start_pos[1], end_pos[0], end_pos[1]]
        if self.sub_minute:
            angle = self.angle_percent + angles[1] + self.angle_offset
            self.sub_minute.update(end_pos, angle, angles, length)
        if self.sub_second:
            angle = self.angle_percent + angles[2] + self.angle_offset
            self.sub_second.update(end_pos, angle, angles, length)


class FractalClock(Widget):
    angle_offset = NumericProperty(0.4)  #Percent of offset for fractal sub-hands
    max_iteration = NumericProperty(6)  #Number of times to add sub-hands
    color_value = NumericProperty(0.4)  #Starting transparency level for sub-hands
    color_minimum = NumericProperty(0)  #Low cutoff value for sub-hand transparency
    scale = NumericProperty(.5)  #Multiplier for clock size
    subhand_width = NumericProperty(1)  #Line width for sub-hands
    overlay_width = NumericProperty(1.5)  #Line width for the overlay hands
    fractal_color = ColorProperty([1, 1, 1])
    hand_color = ColorProperty([1, 1, 1])
    hand_length = NumericProperty(1)
    center_pos = ListProperty([0, 0])
    hour = NumericProperty(0)
    minute = NumericProperty(0)
    second = NumericProperty(0)
    minute_line = None
    second_line = None
    hour_overlay = None
    minute_overlay = None
    second_overlay = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reset()
        Clock.schedule_interval(self.set_current_time, 0.03333)

    def on_subhand_width(self, *_):
        self.reset()

    def on_overlay_width(self, *_):
        self.reset()

    def on_angle_offset(self, *_):
        self.reset()

    def on_max_iteration(self, *_):
        self.reset()

    def on_fractal_color(self, *_):
        self.reset()

    def on_hand_color(self, *_):
        self.reset()

    def on_color_value(self, *_):
        self.reset()

    def on_color_minimum(self, *_):
        self.reset()

    def on_scale(self, *_):
        self.on_size()
        self.reset()

    def reset(self):
        self.canvas.clear()
        color_subtract = (self.color_value - self.color_minimum) / (self.max_iteration + 1)
        self.minute_line = FractalLine(width=self.subhand_width, color=self.fractal_color[:3], color_subtract=color_subtract, angle_offset=self.angle_offset, canvas=self.canvas, iteration=1, max_iteration=self.max_iteration, color_value=self.color_value)
        self.second_line = FractalLine(width=self.subhand_width, color=self.fractal_color[:3], color_subtract=color_subtract, angle_offset=self.angle_offset, canvas=self.canvas, iteration=1, max_iteration=self.max_iteration, color_value=self.color_value)
        self.canvas.add(Color(*self.fractal_color[:3], self.color_value))
        self.canvas.add(self.minute_line)
        self.canvas.add(self.second_line)
        self.canvas.add(Color(*self.hand_color))
        self.hour_overlay = FractalLine(width=self.overlay_width, canvas=self.canvas)
        self.minute_overlay = FractalLine(width=self.overlay_width, canvas=self.canvas)
        self.second_overlay = FractalLine(width=self.overlay_width, canvas=self.canvas)
        self.canvas.add(self.hour_overlay)
        self.canvas.add(self.minute_overlay)
        self.canvas.add(self.second_overlay)

    def on_size(self, *_):
        self.center_pos = [self.pos[0] + self.width / 2, self.pos[1] + self.height / 2]
        self.hand_length = min(self.center_pos[0], self.center_pos[1]) * self.scale

    def set_current_time(self, *_):
        now = datetime.now()
        if now.hour > 12:
            self.hour = now.hour - 12
        else:
            self.hour = now.hour
        self.minute = now.minute
        self.second = now.second + (now.microsecond / 1000000)
        self.redraw()

    def redraw(self, *_):
        second_per = self.second / 60
        minute_per = (self.minute + second_per) / 60
        hour_per = (self.hour + minute_per) / 12
        angles = (hour_per, minute_per, second_per)
        self.minute_line.update(self.center_pos, minute_per, angles, self.hand_length)
        self.second_line.update(self.center_pos, second_per, angles, self.hand_length)
        self.hour_overlay.update(self.center_pos, hour_per, angles, self.hand_length*.5)
        self.minute_overlay.update(self.center_pos, minute_per, angles, self.hand_length)
        self.second_overlay.update(self.center_pos, second_per, angles, self.hand_length)


class FractalClockApp(App):
    def apply_settings(self):
        fc = self.root.ids.fractalclock
        fc.angle_offset = self.config.getfloat("Settings", "angle_offset")
        fc.max_iteration = self.config.getint("Settings", "max_iteration")
        fc.color_value = self.config.getfloat("Settings", "color_value")
        fc.color_minimum = self.config.getfloat("Settings", "color_minimum")
        fc.scale = self.config.getfloat("Settings", "scale")
        fc.subhand_width = self.config.getfloat("Settings", "subhand_width")
        fc.overlay_width = self.config.getfloat("Settings", "overlay_width")
        self.root.ids.clockindicators.anti_screen_burn = self.config.getboolean("Settings", "anti_screen_burn")
        self.root.ids.clockindicators.indicator_size = self.config.getfloat("Settings", "indicator_size")
        self.root.ids.clockindicators.line_width = self.config.getfloat("Settings", "indicator_width")
        self.root.ids.clockindicators.opacity = self.config.getfloat("Settings", "circle_opacity")
        self.root.ids.clockindicators.scale = self.config.getfloat("Settings", "circle_scale")
        self.root.ids.digitalclock.opacity = self.config.getfloat("Settings", "digital_opacity")
        self.root.digital_x = self.config.getfloat("Settings", "digital_x")
        self.root.digital_y = self.config.getfloat("Settings", "digital_y")
        self.root.digital_size = self.config.getfloat("Settings", "digital_size")
        self.root.ids.clockindicators.indicators_color = self.config.get("Settings", "indicators_color")
        self.root.ids.digitalclock.color = self.config.get("Settings", "digital_color")
        fc.hand_color = self.config.get("Settings", "hand_color")
        fc.fractal_color = self.config.get("Settings", "fractal_color")

    def save_settings(self):
        fc = self.root.ids.fractalclock
        self.config.set("Settings", "angle_offset", fc.angle_offset)
        self.config.set("Settings", "max_iteration", fc.max_iteration)
        self.config.set("Settings", "color_value", fc.color_value)
        self.config.set("Settings", "color_minimum", fc.color_minimum)
        self.config.set("Settings", "scale", fc.scale)
        self.config.set("Settings", "subhand_width", fc.subhand_width)
        self.config.set("Settings", "overlay_width", fc.overlay_width)
        self.config.set("Settings", "anti_screen_burn", self.root.ids.clockindicators.anti_screen_burn)
        self.config.set("Settings", "indicator_size", self.root.ids.clockindicators.indicator_size)
        self.config.set("Settings", "indicator_width", self.root.ids.clockindicators.line_width)
        self.config.set("Settings", "circle_opacity", self.root.ids.clockindicators.opacity)
        self.config.set("Settings", "circle_scale", self.root.ids.clockindicators.scale)
        self.config.set("Settings", "digital_opacity", self.root.ids.digitalclock.opacity)
        self.config.set("Settings", "digital_x", self.root.digital_x)
        self.config.set("Settings", "digital_y", self.root.digital_y)
        self.config.set("Settings", "digital_size", self.root.digital_size)
        self.config.set("Settings", "digital_color", get_hex_from_color(self.root.ids.digitalclock.color[:3]))
        self.config.set("Settings", "indicators_color", get_hex_from_color(self.root.ids.clockindicators.indicators_color[:3]))
        self.config.set("Settings", "hand_color", get_hex_from_color(fc.hand_color[:3]))
        self.config.set("Settings", "fractal_color", get_hex_from_color(fc.fractal_color[:3]))
        self.config.write()

    def reset_settings(self):
        for setting in settings:
            self.config.set("Settings", setting, settings[setting])
        self.apply_settings()

    def build_config(self, config):
        config.setdefaults('Settings', settings)

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        self.apply_settings()


if __name__ == '__main__':
    FractalClockApp().run()