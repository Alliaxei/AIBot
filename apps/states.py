from aiogram.fsm.state import StatesGroup, State

class DeepSeekState(StatesGroup):
    waiting_for_promt = State()

class VideoState(StatesGroup):
    waiting_for_promt = State()


