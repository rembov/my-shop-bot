import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import sqlite3 as sq
import config
from kbd import db as db
from dotenv import load_dotenv
from kbd import keyboards
from config import token, admin
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import LabeledPrice, PreCheckoutQuery

storage = MemoryStorage()
load_dotenv()
# Объект бота
bot = Bot(token)
# Диспетчер
dp = Dispatcher()


class NewOrder(StatesGroup):
    name = State()
    desc = State()
    price = State()
    photo = State()


class New1(StatesGroup):
    name = State()


class NewOrder1(StatesGroup):
    t = State()
    t2 = State()
    mail = State()


class Cata(StatesGroup):
    cata = State()
    cata2 = State()


class kor(StatesGroup):
    kor = State()


class Kor1(StatesGroup):
    kor1 = State()


class Mail(StatesGroup):
    mail = State()


class Mou(StatesGroup):
    ud = State()
    money = State()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)
    if message.from_user.id != admin:
        await message.answer(f"{message.from_user.first_name},Привет!\nДобро пожаловать в магазин печенья 🍪🍪🍪!",
                             reply_markup=keyboards.keyboard)
    if message.from_user.id == admin:
        await message.answer(f"{message.from_user.first_name},Привет!\nВы авторизировались как админ",
                             reply_markup=keyboards.keyboard)


@dp.message(Command("id"))
async def cmd_id(message: types.Message):
    await message.answer(f"{message.from_user.id}")


@dp.message(F.text.lower() == "каталог 📕")
async def with_puree(message: types.Message, state: FSMContext):
    db = sq.connect('tg1.db')
    cur = db.cursor()
    cur.execute('''SELECT * FROM category''')
    data = cur.fetchall()
    print(data)
    await state.set_state(Kor1.kor1)
    await message.answer("Каталог товаров 🍪🍪🍪 :", reply_markup=keyboards.genmarkup(data).as_markup())


@dp.message(F.text.lower() == "сделать рассылку 📫")
async def mail(message: types.Message, state: FSMContext):
    await message.answer(
        ' Отправьте сообщение для рассылки:'
    )
    await state.set_state(Mail.mail)


@dp.message(Mail.mail)
async def add_item(message: types.Message, state: FSMContext):
    print('1')
    await state.update_data(mail=message.text)
    print(message.text)
    data1 = await state.get_data()
    d = data1['mail']
    db = sq.connect('tg1.db')
    cur = db.cursor()
    cur.execute('''SELECT * FROM accounts WHERE tg_id ''')
    data = cur.fetchall()
    print(data)
    for i in data:
        if message.from_user.id == i[1]:
            print(i[1])
            await message.answer(f"{d}")
    await state.clear()
    if message.from_user.id == admin:
        await message.answer("рассылка сделана!", reply_markup=keyboards.keyadm1)


@dp.callback_query(Kor1.kor1)
async def callback_query_delete(callback_query: types.CallbackQuery, state: FSMContext):
    print('1')

    if int(callback_query.data) > 0:
        await state.set_state(Cata.cata)

        db1 = sq.connect('tg1.db')
        cur1 = db1.cursor()
        cur1.execute('''SELECT * FROM category''')
        db = sq.connect('tg1.db')
        cur = db.cursor()
        cur.execute('''SELECT * FROM items''')
        data = cur.fetchall()
        data2 = cur1.fetchall()
        w = int(callback_query.data)
        w = w - 1

        print(w)

        await state.update_data(cata=data2[w][1] + f'w{data[w][2]}')

        await callback_query.message.answer_photo(data[w][3],
                                                  f'Описание: {data[w][1]}\nЦена: {data[w][2]}\n',
                                                  reply_markup=keyboards.dob().as_markup())


@dp.callback_query(lambda call: call.data == "dob", Cata.cata)
async def callback_query_d(callback_query: types.CallbackQuery, state: FSMContext):
    w = callback_query.from_user.id
    data = await state.get_data()
    data1 = data['cata']
    data1 = data1.split('w')

    print(data1)

    db.add_kor(w, data1[0], data1[1])
    await callback_query.message.answer("Товар добавлен в корзину!")


@dp.message(Command("adm"))
async def with_puree(message: types.Message):
    if message.from_user.id != admin:
        await message.answer(f"{message.from_user.first_name},я тебя не понимаю!",
                             reply_markup=keyboards.keyboard)
    if message.from_user.id == admin:
        await message.answer(f"{message.from_user.first_name},Привет!\nВы вошли Админ-панель",
                             reply_markup=keyboards.keyadm1)


@dp.message(F.text.lower() == "удалить товар 📤")
async def add_item(message: types.Message, state: FSMContext):
    if message.from_user.id != admin:
        await message.answer(f"{message.from_user.first_name},я тебя не понимаю!",
                             reply_markup=keyboards.keyboard)
    if message.from_user.id == admin:
        await state.set_state(NewOrder1.t2)
        db = sq.connect('tg1.db')
        cur = db.cursor()
        cur.execute('''SELECT * FROM category''')
        data = cur.fetchall()
        print(data)
        await message.answer(f'Выберите тип товара', reply_markup=keyboards.genmarkup(data).as_markup())


@dp.callback_query(NewOrder1.t2)
async def callback_query_delete(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.from_user.id == admin:
        if int(callback_query.data) > 0:
            w = int(callback_query.data)
            db.delete_item1(w)

            await callback_query.message.answer(f'товар {w} удален', reply_markup=keyboards.keyadm1)

    await state.clear()


@dp.message(F.text.lower() == "удалить описание 📤")
async def add_item(message: types.Message, state: FSMContext):
    if message.from_user.id != admin:
        await message.answer(f"{message.from_user.first_name},я тебя не понимаю!",
                             reply_markup=keyboards.keyboard)
    if message.from_user.id == admin:
        await state.set_state(NewOrder1.t)
        db = sq.connect('tg1.db')
        cur = db.cursor()
        cur.execute('''SELECT * FROM items''')
        data = cur.fetchall()
        print(data)
        await message.answer(f'Выберите тип товара', reply_markup=keyboards.genmarkup(data).as_markup())


@dp.callback_query(NewOrder1.t)
async def callback_query_delete(callback_query: types.CallbackQuery, state: FSMContext):
    if int(callback_query.data) > 0:
        w = int(callback_query.data)
        db.delete_item(w)
        await callback_query.message.answer(f'описание {w} удалено', reply_markup=keyboards.keyadm1)

    await state.clear()


@dp.message(F.text.lower() == "добавить описание 📥")
async def add_item(message: types.Message, state: FSMContext):
    if message.from_user.id != admin:
        await message.answer(f"{message.from_user.first_name},я тебя не понимаю!",
                             reply_markup=keyboards.keyboard)
    if message.from_user.id == admin:
        await state.set_state(NewOrder.name)
        db = sq.connect('tg1.db')
        cur = db.cursor()
        cur.execute('''SELECT * FROM category''')
        data = cur.fetchall()
        print(data)
        await message.answer(f'Выберите тип товара', reply_markup=keyboards.genmarkup(data).as_markup())


@dp.message(F.text.lower() == "добавить товар 📥")
async def add_item_type11(message: types.Message, state: FSMContext):
    if message.from_user.id != admin:
        await message.answer(f"{message.from_user.first_name},я тебя не понимаю!",
                             reply_markup=keyboards.keyboard)
    if message.from_user.id == admin:
        await state.set_state(New1.name)
        await message.answer(f'Напишите название товара')


@dp.message(New1.name)
async def add_item_type11(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    print(message.text)
    data1 = await state.get_data()
    data = data1['name']
    db.add_item1(data)
    await state.clear()

    await message.answer('Товар создан!', reply_markup=keyboards.keyadm1)


@dp.callback_query(NewOrder.name)
async def add_item_type(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(NewOrder.desc)
    await call.message.answer(f'Напишите описание товара')


@dp.message(NewOrder.desc)
async def add_item_type(message: types.Message, state: FSMContext):
    await state.set_state(NewOrder.desc)
    await state.update_data(desc=message.text)
    await state.set_state(NewOrder.price)
    await message.answer(f'Напишите цену товара')


@dp.message(NewOrder.price)
async def add_item_type(message: types.Message, state: FSMContext):
    await state.set_state(NewOrder.price)
    if int(message.text) > 0:
        await state.update_data(price=message.text)
    else:
        await message.answer(f'Это не цена')
    await state.set_state(NewOrder.photo)
    await message.answer(f'Отправьте фото товара')


@dp.message(NewOrder.photo, F.photo)
async def add_item_type(message: types.Message, state: FSMContext):
    await state.set_state(NewOrder.photo)
    await state.update_data(photo=message.photo[-1].file_id)

    data = await state.get_data()

    db.add_item(**data)
    await state.clear()

    await message.answer('Описание создано!', reply_markup=keyboards.keyadm1)


@dp.message(F.text.lower() == "корзина 🗑")
async def with_puree(message: types.Message, state: FSMContext):
    await message.answer('Отличный выбор!\nНазвания добавленных товаров:')
    db = sq.connect('tg1.db')
    cur = db.cursor()
    cur.execute('''SELECT * FROM korzina''')
    data = cur.fetchall()
    mmm = int(message.from_user.id)
    await state.update_data(ud=mmm)
    for i in data:
        if int(i[0]) != 0 and int(i[0]) == mmm:
            await bot.send_message(message.chat.id, f'{i[1]}\nЦена: {i[2]}', reply_markup=keyboards.udal)


@dp.message(F.text.lower() == "удалить из корзины ❌")
async def callback_query_d1112(message: types.Message):
    print("ud")

    w = message.from_user.id
    db.ud_kor(w)
    if w == admin:
        await message.answer("Товары удалены из корзины!", reply_markup=keyboards.keyadm1)
    else:
        await message.answer("Товары удалены из корзины!", reply_markup=keyboards.keyboard)


@dp.message(F.text.lower() == "оплатить 💵")
async def callback_query_d1112(message: types.Message):
    await message.answer("Оплата!", reply_markup=keyboards.keyboard)
    db = sq.connect('tg1.db')
    cur = db.cursor()
    cur.execute('''SELECT * FROM korzina''')
    data = cur.fetchall()
    k = -1
    s = 0
    for i in data:
        if data != '':
            k += 1
    while k >= 0:
        s += int(data[k][2])
        k -= 1

    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Покупка товаров',
        description='Покупка товаров',
        payload='hm',
        provider_token=config.pay,
        currency='rub',
        prices=[
            LabeledPrice(label='Цена за ваши покупки', amount=s * 100)
        ], start_parameter='bot',
        provider_data=None,
        photo_url=None,
        need_name=True,
        need_email=False,
        need_phone_number=False,
        need_shipping_address=False,
        send_email_to_provider=False,
        send_phone_number_to_provider=False,
        is_flexible=False,
        disable_notification=True,
        protect_content=True,
        reply_to_message_id=None,
        reply_markup=None,
        request_timeout=15
    )
    s = 0


@dp.pre_checkout_query(lambda x: True)
async def prech(pre: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre.id, ok=True)
    m = pre.from_user.id
    db.ud_kor(m)


@dp.message(F.text.lower() == "возврат 🔄")
async def callback_query_d1112(message: types.Message):
    w = message.from_user.id
    if w == admin:
        await message.answer("Вы вышли из корзины!", reply_markup=keyboards.keyadm1)
    else:
        await message.answer("Вы вышли из корзины!", reply_markup=keyboards.keyboard)


@dp.message(F.text.lower() == "контакты 📞")
async def with_puree(message: types.Message):
    await message.reply(config.support)


# Запуск процесса поллинга новых апдейтов
async def main():
    await db.db_start()
    await dp.start_polling(bot, storage=storage)


if __name__ == "__main__":
    asyncio.run(main())
    print("База данных успешно подключена")
