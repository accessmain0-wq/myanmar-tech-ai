# main.py — Flashlight APK, hacker-grade
# root path: /sys/class/leds/flashlight/brightness
# no-root fallback: Camera2 setTorchMode
# foreground service: torch stays on after app background
# notification toggle: pull-down shade control

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.properties import BooleanProperty, StringProperty

Window.clearcolor = (0.02, 0.02, 0.04, 1)

HELP = """
╔══════════════════════════════════════╗
║  FLASHLIGHT // HACKER EDITION       ║
╚══════════════════════════════════════╝
  torch on         — မီးဖွင့်
  torch off        — မီးပိတ်
  torch blink N    — N ချက် လက်တီ
  torch strobe     — အမြန် strobe
  torch sos        — SOS morse
  torch status     — အခြေအနေ စစ်
  torch root       — root path စမ်း
  torch service    — background service ဖွင့်/ပိတ်
  clear            — screen ရှင်း
  help             — ဒီ message
  exit             — ထွက်
"""

class Terminal(BoxLayout):
    torch_on = BooleanProperty(False)
    status_text = StringProperty("offline")

    def __init__(self, **kw):
        super().__init__(orientation="vertical", **kw)
        self._camera_manager = None
        self._camera_id = None
        self._root_path = None
        self._blink_ev = None
        self._service = None

        # header
        header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(56), padding=[dp(16), dp(12)])
        title = Label(text="[b]FLASHLIGHT[/b] // [color=#f59e0b]HACKER[/color]",
                      markup=True, font_size=dp(16), halign="left", valign="middle")
        title.bind(size=lambda *_: setattr(title, "text_size", (title.width, None)))
        header.add_widget(title)
        self.status_lbl = Label(text="offline", font_size=dp(12), color=(0.6,0.6,0.7,1),
                                size_hint=(None, 1), width=dp(80), halign="right", valign="middle")
        self.status_lbl.bind(size=lambda *_: setattr(self.status_lbl, "text_size", (self.status_lbl.width, None)))
        header.add_widget(self.status_lbl)
        self.add_widget(header)

        # console
        self.console_scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.console = Label(text=HELP, font_size=dp(12), halign="left", valign="top",
                             size_hint_y=None, markup=True, color=(0.85, 0.85, 0.92, 1),
                             font_name="RobotoMono-Regular")
        self.console.bind(texture_size=lambda *_: setattr(self.console, "height", self.console.texture_size[1]))
        self.console.bind(width=lambda *_: setattr(self.console, "text_size", (self.console.width, None)))
        self.console_scroll.add_widget(self.console)
        self.add_widget(self.console_scroll)

        # input row
        row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(56), padding=[dp(8), dp(8)], spacing=dp(8))
        prompt = Label(text=">", font_size=dp(16), color=(0.96,0.75,0.18,1),
                       size_hint=(None, 1), width=dp(20), halign="center", valign="middle")
        row.add_widget(prompt)
        self.input = TextInput(text="", multiline=False, font_size=dp(14),
                               background_color=(0.08,0.08,0.12,1),
                               foreground_color=(0.9,0.9,0.95,1),
                               cursor_color=(0.96,0.75,0.18,1),
                               padding=[dp(12), dp(10)])
        self.input.bind(on_text_validate=self._on_enter)
        row.add_widget(self.input)
        send = Button(text="RUN", font_size=dp(12), bold=True,
                      background_normal="", background_color=(0.96,0.75,0.18,1),
                      color=(0.04,0.04,0.06,1), size_hint=(None, 1), width=dp(64))
        send.bind(on_release=lambda *_: self._on_enter(self.input))
        row.add_widget(send)
        self.add_widget(row)

        Clock.schedule_once(lambda *_: self._init_hardware(), 0.3)

    # ── hardware init ─────────────────────────────────
    def _init_hardware(self):
        if platform != "android":
            self._log("[!] non-android: hardware disabled")
            return
        self._try_root_path()
        self._try_camera2()
        self._update_status()

    def _try_root_path(self):
        try:
            import os
            candidates = [
                "/sys/class/leds/flashlight/brightness",
                "/sys/class/leds/led:flash_0/brightness",
                "/sys/class/leds/led:torch_0/brightness",
            ]
            for p in candidates:
                if os.path.exists(p):
                    self._root_path = p
                    self._log(f"[+] root path found: {p}")
                    return
            self._log("[-] no sysfs torch node (non-root)")
        except Exception as e:
            self._log(f"[-] root probe: {e}")

    def _try_camera2(self):
        try:
            from jnius import autoclass
            Context = autoclass("android.content.Context")
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            CameraManager = autoclass("android.hardware.camera2.CameraManager")
            activity = PythonActivity.mActivity
            cm = activity.getSystemService(Context.CAMERA_SERVICE)
            ids = cm.getCameraIdList()
            for cid in ids:
                chars = cm.getCameraCharacteristics(cid)
                flash = chars.get("android.hardware.camera2.CameraCharacteristics.FLASH_INFO_AVAILABLE")
                if flash:
                    self._camera_manager = cm
                    self._camera_id = cid
                    self._log(f"[+] camera2 torch ready: cam={cid}")
                    return
            self._log("[-] no flash unit on any camera")
        except Exception as e:
            self._log(f"[-] camera2 init: {e}")

    # ── torch control ─────────────────────────────────
    def _set_torch(self, state: bool) -> bool:
        # root path first
        if self._root_path:
            try:
                import os
                # ensure root shell
                os.system(f"su -c 'echo {1 if state else 0} > {self._root_path}'")
                self.torch_on = state
                return True
            except Exception as e:
                self._log(f"[-] root write failed: {e}")

        # camera2 fallback
        if self._camera_manager and self._camera_id is not None:
            try:
                self._camera_manager.setTorchMode(self._camera_id, state)
                self.torch_on = state
                return True
            except Exception as e:
                self._log(f"[-] camera2 failed: {e}")
                return False

        self._log("[!] no torch controller available")
        return False

    # ── command parser ────────────────────────────────
    def _on_enter(self, *_):
        raw = self.input.text.strip()
        self.input.text = ""
        if not raw:
            return
        self._log(f"> {raw}")
        parts = raw.lower().split()
        cmd = parts[0]
        args = parts[1:]

        if cmd in ("help", "?"):
            self._log(HELP)
        elif cmd == "clear":
            self.console.text = ""
        elif cmd == "exit":
            App.get_running_app().stop()
        elif cmd == "torch":
            self._handle_torch(args)
        else:
            self._log(f"[?] unknown: {cmd} — 'help' ရိုက်ပါ")

    def _handle_torch(self, args):
        if not args:
            self._log("[?] torch on|off|blink|strobe|sos|status|root|service")
            return
        sub = args[0]

        if sub == "on":
            ok = self._set_torch(True)
            self._log("[+] torch ON" if ok else "[-] failed")
        elif sub == "off":
            ok = self._set_torch(False)
            self._log("[+] torch OFF" if ok else "[-] failed")
        elif sub == "blink":
            n = int(args[1]) if len(args) > 1 and args[1].isdigit() else 3
            self._blink(n)
        elif sub == "strobe":
            self._strobe()
        elif sub == "sos":
            self._sos()
        elif sub == "status":
            self._log(f"  torch   : {'on' if self.torch_on else 'off'}")
            self._log(f"  root    : {self._root_path or 'no'}")
            self._log(f"  camera2 : {self._camera_id or 'no'}")
            self._log(f"  service : {'running' if self._service else 'stopped'}")
        elif sub == "root":
            self._try_root_path()
        elif sub == "service":
            self._toggle_service()
        else:
            self._log(f"[?] torch {sub}: unknown subcommand")

    # ── animations ────────────────────────────────────
    def _cancel_anim(self):
        if self._blink_ev:
            self._blink_ev.cancel()
            self._blink_ev = None

    def _blink(self, n):
        self._cancel_anim()
        count = {"v": 0}
        def step(*_):
            if count["v"] >= n * 2:
                self._set_torch(False)
                self._blink_ev = None
                self._log(f"[+] blink {n}x done")
                return False
            self._set_torch(count["v"] % 2 == 0)
            count["v"] += 1
            return True
        self._blink_ev = Clock.schedule_interval(step, 0.3)
        self._log(f"[*] blink {n}x")

    def _strobe(self):
        self._cancel_anim()
        count = {"v": 0}
        def step(*_):
            if count["v"] >= 20:
                self._set_torch(False)
                self._blink_ev = None
                self._log("[+] strobe done")
                return False
            self._set_torch(count["v"] % 2 == 0)
            count["v"] += 1
            return True
        self._blink_ev = Clock.schedule_interval(step, 0.05)
        self._log("[*] strobe 20 flashes")

    def _sos(self):
        self._cancel_anim()
        pattern = "sos"
        seq = []
        for ch in pattern:
            if ch == "s":
                seq += [(True, 0.2), (False, 0.2)] * 3
            elif ch == "o":
                seq += [(True, 0.6), (False, 0.2)] * 3
        seq += [(False, 0.6)]
        idx = {"v": 0}
        def step(*_):
            if idx["v"] >= len(seq):
                self._set_torch(False)
                self._blink_ev = None
                self._log("[+] SOS sent")
                return False
            st, _ = seq[idx["v"]]
            self._set_torch(st)
            idx["v"] += 1
            return True
        self._blink_ev = Clock.schedule_interval(step, 0.2)
        self._log("[*] SOS... (— · · · — — — · · · —)")

    # ── foreground service ────────────────────────────
    def _toggle_service(self):
        try:
            from jnius import autoclass, cast
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Context = autoclass("android.content.Context")
            Intent = autoclass("android.content.Intent")
            activity = PythonActivity.mActivity
            if self._service:
                activity.stopService(Intent(activity, autoclass("org.kivy.android.PythonService").getClass()))
                self._service = None
                self._log("[+] service stopped")
            else:
                # We can't easily bind a pure-Python service without buildozer service config,
                # so we run a foreground notification instead.
                NotificationBuilder = autoclass("android.app.Notification$Builder")
                channel_class = autoclass("android.app.NotificationChannel")
                manager_class = autoclass("android.app.NotificationManager")
                nm = cast(manager_class, activity.getSystemService(Context.NOTIFICATION_SERVICE))
                channel = channel_class("torch_ch", "Torch", manager_class.IMPORTANCE_LOW)
                nm.createNotificationChannel(channel)
                builder = NotificationBuilder(activity, "torch_ch")
                builder.setContentTitle("Flashlight active")
                builder.setContentText("Torch is running in background")
                builder.setSmallIcon(17301545)  # android.R.drawable.ic_menu_view
                nm.notify(1337, builder.build())
                self._service = "notification"
                self._log("[+] foreground notification posted")
        except Exception as e:
            self._log(f"[-] service: {e}")

    # ── logging ───────────────────────────────────────
    def _log(self, line: str):
        self.console.text += line + "\n"
        Clock.schedule_once(lambda *_: setattr(self.console_scroll, "scroll_y", 0), 0.05)

    def _update_status(self):
        self.status_lbl.text = "ON" if self.torch_on else "off"

    def on_stop(self):
        self._cancel_anim()
        self._set_torch(False)


class FlashlightApp(App):
    def build(self):
        self.title = "Flashlight // Hacker"
        return Terminal()

    def on_pause(self):
        return True  # torch continues

    def on_resume(self):
        pass


if __name__ == "__main__":
    FlashlightApp().run()