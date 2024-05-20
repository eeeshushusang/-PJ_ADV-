from django.forms import widgets


class CompositeWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        _widgets = [  # 这里修改变量名以避免与导入的模块名widgets冲突
            widgets.NumberInput(attrs={'placeholder': '分数', 'step': '0.01', 'min': '0', 'max': '100'}),
            widgets.TextInput(attrs={'placeholder': '评价', 'maxlength': '20'}),
        ]
        super().__init__(_widgets, attrs)  # 这里使用了新的变量名_widgets

    def decompress(self, value):
        if value:
            return value.split(':')
        return [None, None]
