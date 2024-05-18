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
        pos_hint: {'x': app.anti_burn_offset, 'y': app.anti_burn_offset}
    ClockIndicators:
        id: clockindicators
        pos_hint: {'x': app.anti_burn_offset, 'y': app.anti_burn_offset}
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
        hidden: not app.show_settings
        size_hint_x: 0.333
        pos: (root.width - self.width) if not self.hidden else root.width, 0
        orientation: 'vertical'
        ScrollView:
            scroll_type: ['bars', 'content']
            do_scroll_x: False
            do_scroll_y: True
            on_scroll_move: app.start_close_settings()
            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                SettingLabel:
                    text: "Clock Scale: "
                SettingSlider:
                    value: fractalclock.scale
                    on_value: fractalclock.scale = round(self.value, 2)
                    min: 0.1
                    max: 1
                SettingLabel:
                    text: "Clock Hand Width: " + str(int(fractalclock.overlay_width))
                SettingSlider:
                    value: fractalclock.overlay_width
                    on_value: fractalclock.overlay_width = round(self.value, 0)
                    min: 1
                    max: 10
                SettingLabel:
                    text: "Clock Hand Overlay Scale: " + str(fractalclock.hand_overscale)
                SettingSlider:
                    value: fractalclock.hand_overscale
                    on_value: fractalclock.hand_overscale = round(self.value, 1)
                    min: 0.5
                    max: 4
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
                    text: "Transparency Maximum: " + str(fractalclock.color_value)
                SettingSlider:
                    value: fractalclock.color_value
                    on_value: fractalclock.color_value = round(self.value, 2)
                    min: 0
                    max: 1
                SettingLabel:
                    text: "Transparency Minimum: " + str(fractalclock.color_minimum)
                SettingSlider:
                    value: fractalclock.color_minimum
                    on_value: fractalclock.color_minimum = round(self.value, 2)
                    min: 0
                    max: 1
                SettingLabel:
                    text: "Fractal Line Width: " + str(int(fractalclock.subhand_width))
                SettingSlider:
                    value: fractalclock.subhand_width
                    on_value: fractalclock.subhand_width = round(self.value, 0)
                    min: 1
                    max: 10
                SettingLabel:
                    text: "Fractal Color: "
                ColorWheel:
                    size_hint_y: None
                    height: self.width / 2
                    color: fractalclock.fractal_color
                    on_color: fractalclock.fractal_color = self.color[:3]

                SettingSpacer:

                SettingLabel:
                    text: "Clock Indicators Transparency: "
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
                    text: "Clock Indicator Line Width: " + str(int(clockindicators.line_width))
                SettingSlider:
                    value: clockindicators.line_width
                    on_value: clockindicators.line_width = round(self.value, 0)
                    min: 1
                    max: 10
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
                    state: 'down' if app.anti_screen_burn else 'normal'
                    on_state: app.anti_screen_burn = True if self.state == 'down' else False
                SettingLabel:
                    text: "Clock Indicators Color: "
                ColorWheel:
                    size_hint_y: None
                    height: self.width / 2
                    color: clockindicators.indicators_color
                    on_color: clockindicators.indicators_color = self.color[:3]

                SettingSpacer:

                SettingLabel:
                    text: "Digital Clock Transparency: "
                SettingSlider:
                    value: digitalclock.opacity
                    on_value: digitalclock.opacity = self.value
                    min: 0
                    max: 1
                SettingLabel:
                    text: "Digital Clock X Position: " + str(root.digital_x)
                SettingSlider:
                    value: root.digital_x
                    on_value: root.digital_x = round(self.value, 2)
                    min: 0
                    max: 1
                SettingLabel:
                    text: "Digital Clock Y Position: " + str(root.digital_y)
                SettingSlider:
                    value: root.digital_y
                    on_value: root.digital_y = round(self.value, 2)
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
                text: 'Quit'
                on_release: app.stop()
    Button:
        opacity: 0
        pos: 0 if settingsarea.hidden else (0 - settingsarea.width), 0
        on_release: app.toggle_settings()
"""

settings = {
    'angle_offset': 0.4,
    'max_iteration': 6,
    'color_value': 0.4,
    'color_minimum': 0,
    'scale': 0.5,
    'subhand_width': 1,
    'overlay_width': 1.5,
    'hand_overscale': 1,
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def redraw(self):
        self.center_pos = [self.pos[0] + self.width / 2, self.pos[1] + self.height / 2]
        self.radius = min(self.center_pos[0], self.center_pos[1]) * self.scale
        mid_x = self.pos[0] + self.width / 2
        mid_y = self.pos[1] + self.height / 2
        self.canvas.clear()
        self.canvas.add(Color(*self.indicators_color[:3]))
        indicator_size = 0.025 * self.indicator_size
        inner_radius = self.radius * self.scale * (1 - indicator_size)
        outer_radius = self.radius * self.scale * (1 + indicator_size)
        for index in range(0, 12):
            radians = index / 6 * pi
            start_x = mid_x + inner_radius * sin(radians)
            start_y = mid_y + inner_radius * cos(radians)
            end_x = mid_x + outer_radius * sin(radians)
            end_y = mid_y + outer_radius * cos(radians)
            self.canvas.add(Line(width=self.line_width, points=[start_x, start_y, end_x, end_y]))

    def on_indicators_color(self, *_):
        self.redraw()

    def on_indicator_size(self, *_):
        self.redraw()

    def on_pos(self, *_):
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
    hand_overscale = NumericProperty(1)
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
        app = App.get_running_app()
        app.start_close_settings()
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

    def on_pos(self, *_):
        self.center_pos = [self.pos[0] + self.width / 2, self.pos[1] + self.height / 2]

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
        self.hour_overlay.update(self.center_pos, hour_per, angles, self.hand_length*.5*self.hand_overscale)
        self.minute_overlay.update(self.center_pos, minute_per, angles, self.hand_length*self.hand_overscale)
        self.second_overlay.update(self.center_pos, second_per, angles, self.hand_length*self.hand_overscale)


class FractalClockApp(App):
    close_settings_timer = ObjectProperty(allownone=True)
    anti_screen_burn = BooleanProperty(False)
    anti_screen_burn_amount = []
    anti_screen_burn_index = 0
    anti_burn_offset = NumericProperty(0)
    show_settings = BooleanProperty(False)

    def toggle_settings(self):
        if self.show_settings:
            self.close_settings_area()
        else:
            self.show_settings_area()

    def start_close_settings(self):
        self.stop_close_settings()
        self.close_settings_timer = Clock.schedule_once(self.close_settings_area, 60)

    def stop_close_settings(self):
        if self.close_settings_timer:
            self.close_settings_timer.cancel()
            self.close_settings_timer = None

    def show_settings_area(self):
        self.start_close_settings()
        self.show_settings = True

    def close_settings_area(self, *_):
        self.stop_close_settings()
        self.show_settings = False

    def update_anti_burn(self, *_):
        if self.anti_screen_burn:
            self.anti_screen_burn_index += 1
            if self.anti_screen_burn_index > 199:
                self.anti_screen_burn_index = 0
            self.anti_burn_offset = self.anti_screen_burn_amount[self.anti_screen_burn_index]
        else:
            self.anti_burn_offset = 0

    def apply_settings(self):
        fc = self.root.ids.fractalclock
        fc.angle_offset = self.config.getfloat("Settings", "angle_offset")
        fc.max_iteration = self.config.getint("Settings", "max_iteration")
        fc.color_value = self.config.getfloat("Settings", "color_value")
        fc.color_minimum = self.config.getfloat("Settings", "color_minimum")
        fc.scale = self.config.getfloat("Settings", "scale")
        fc.subhand_width = self.config.getfloat("Settings", "subhand_width")
        fc.overlay_width = self.config.getfloat("Settings", "overlay_width")
        fc.hand_overscale = self.config.getfloat("Settings", "hand_overscale")
        self.anti_screen_burn = self.config.getboolean("Settings", "anti_screen_burn")
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
        self.config.set("Settings", "hand_overscale", fc.hand_overscale)
        self.config.set("Settings", "anti_screen_burn", self.anti_screen_burn)
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
        for i in range(0, 100):
            self.anti_screen_burn_amount.append((i - 50) / 10000)
        for i in range(100, 0, -1):
            self.anti_screen_burn_amount.append((i - 50) / 10000)
        Clock.schedule_interval(self.update_anti_burn, 1)


if __name__ == '__main__':
    FractalClockApp().run()
