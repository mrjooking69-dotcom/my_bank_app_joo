from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.toast import toast
from kivy.utils import platform
import os

# تحديد مسار الحفظ ليعمل على أندرويد والكمبيوتر
if platform == 'android':
    from android.storage import app_storage_details
    data_dir = app_storage_details().filesDir
    store_path = os.path.join(data_dir, "data.json")
else:
    store_path = "data.json"

store = JsonStore(store_path)

KV = '''
MDScreen:
    MDBottomNavigation:
        panel_color: .9, .9, .9, 1
        
        MDBottomNavigationItem:
            name: "home"
            text: "الرئيسية"
            icon: "home"
            MDBoxLayout:
                orientation: "vertical"
                padding: 20
                spacing: 20
                MDLabel:
                    text: "MR/ABOJOO"
                    halign: "center"
                    font_style: "H4"
                    theme_text_color: "Primary"
                MDLabel:
                    id: total_money
                    text: "إجمالي الفلوس: 0 جنيه"
                    halign: "center"
                    font_style: "H5"

        MDBottomNavigationItem:
            name: "members"
            text: "الأعضاء"
            icon: "account-group"
            MDBoxLayout:
                orientation: "vertical"
                ScrollView:
                    MDList:
                        id: members_list
                MDFloatingActionButton:
                    icon: "plus"
                    pos_hint: {"center_x": .5}
                    on_release: app.add_member_dialog()
                    md_bg_color: app.theme_cls.primary_color

        MDBottomNavigationItem:
            name: "payment"
            text: "الدفع"
            icon: "cash-multiple"
            ScrollView:
                MDList:
                    id: payment_list

        MDBottomNavigationItem:
            name: "collect"
            text: "القبض"
            icon: "wallet-giftcard"
            MDBoxLayout:
                orientation: "vertical"
                padding: 20
                spacing: 20
                MDLabel:
                    id: collect_label
                    text: ""
                    halign: "center"
                    font_style: "H5"
                MDRaisedButton:
                    text: "الدور التالي"
                    pos_hint: {"center_x": .5}
                    on_release: app.next_turn()
'''

class App(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    def on_start(self):
        if not store.exists("members"):
            store.put("members", data=[], turn=0)
        self.refresh_all()

    def refresh_all(self):
        self.refresh_members()
        self.refresh_payments()
        self.update_collect()
        self.update_total()

    def add_member_dialog(self):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.button import MDRaisedButton

        self.name_input = MDTextField(hint_text="اسم العضو الجديد")
        self.dialog = MDDialog(
            title="إضافة عضو",
            type="custom",
            content_cls=self.name_input,
            buttons=[
                MDRaisedButton(text="إلغاء", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="حفظ", on_release=self.save_member)
            ]
        )
        self.dialog.open()

    def save_member(self, obj):
        name = self.name_input.text.strip()
        if name:
            data = store.get("members")
            members = data["data"]
            members.append({"name": name, "paid": 0, "missed": 0})
            store.put("members", data=members, turn=data["turn"])
            toast(f"تم إضافة {name}")
            self.dialog.dismiss()
            self.refresh_all()

    def refresh_members(self):
        container = self.root.ids.members_list
        container.clear_widgets()
        members = store.get("members")["data"]
        for i, m in enumerate(members):
            text = f'{m["name"]} | 💰 {m["paid"]} | ❌ {m["missed"]}'
            item = OneLineListItem(text=text, on_release=lambda x, i=i: self.mark_missed(i))
            container.add_widget(item)

    def refresh_payments(self):
        container = self.root.ids.payment_list
        container.clear_widgets()
        members = store.get("members")["data"]
        for i, m in enumerate(members):
            item = OneLineListItem(
                text=f'{m["name"]} (دفع: {m["paid"]} جنيه)',
                on_release=lambda x, i=i: self.pay(i)
            )
            container.add_widget(item)

    def pay(self, index):
        data = store.get("members")
        members = data["data"]
        members[index]["paid"] += 5
        store.put("members", data=members, turn=data["turn"])
        toast("تم تسجيل الدفع")
        self.refresh_all()

    def mark_missed(self, index):
        data = store.get("members")
        members = data["data"]
        members[index]["missed"] += 1
        store.put("members", data=members, turn=data["turn"])
        toast("تم تسجيل غياب")
        self.refresh_all()

    def update_collect(self):
        data = store.get("members")
        members = data["data"]
        turn = data["turn"]
        if members:
            amount = len(members) * 5 * 10 # مثال للحساب
            name = members[turn % len(members)]["name"]
            self.root.ids.collect_label.text = f"الدور على: {name}\nالمبلغ: {amount} جنيه"

    def next_turn(self):
        data = store.get("members")
        members = data["data"]
        if members:
            new_turn = (data["turn"] + 1) % len(members)
            store.put("members", data=members, turn=new_turn)
            self.update_collect()
            toast("تم الانتقال للعضو التالي")

    def update_total(self):
        members = store.get("members")["data"]
        total = sum([m["paid"] for m in members])
        self.root.ids.total_money.text = f"إجمالي الفلوس: {total} جنيه"

if __name__ == "__main__":
    App().run()