from aiogram.dispatcher.filters.state import StatesGroup


class TestStatesGroup:
    @staticmethod
    def test_all_childs():
        class InnerState1(StatesGroup):
            pass

        class InnerState2(InnerState1):
            pass

        class Form(StatesGroup):
            inner1 = InnerState1
            inner2 = InnerState2

        form_childs = Form.all_childs
        if form_childs != (InnerState1, InnerState2):
            raise AssertionError
