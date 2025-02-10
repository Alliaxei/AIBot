import os

import openai
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from apps.keyboards import keyboards as kb
from apps.states import DeepSeekState

router = Router()
load_dotenv('.env')
DEEPSEEK_KEY = os.getenv('DEEPSEEK_KEY')

@router.message(DeepSeekState.waiting_for_promt)
async def process_chatgpt_request(message: Message, state: FSMContext):
    user_input = message.text
    try:
        client = openai.OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model='deepseek-chat',
            messages=[
                {'role': 'user', 'content': user_input}
            ],
        )

        deepseek_response = response.choices[0].message.content
        await message.answer(deepseek_response, reply_markup=kb.main)
    except Exception as e:
        print(e)
        await message.answer(f'Ошибка при запросе к DeepSeek {str(e)}')

    await state.clear()

