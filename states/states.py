from aiogram.fsm.state import State, StatesGroup

# Create a class inherited from StatesGroup for the management group of our FSM
class FSMRegistration(StatesGroup):
    fill_name = State()        # Waiting for name entry state
    fill_age = State()         # Waiting for age input state
    fill_gender = State()      # Waiting state for gender selection
    fill_description = State()         # Waiting for description input state
    upload_photo = State()     # Waiting state for photo loading