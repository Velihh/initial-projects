@router.message(Text(text=['Добавить район']))
async def district1(message: Message, state: FSMContext):
	await state.set_state(AdminStates.name_dis)
	await message.answer(
		'Введи название района')

@router.message(AdminStates.name_dis)
async def district2(message: Message, state: FSMContext):
	await state.update_data(name=message.text)
	await state.set_state(AdminStates.geo)
	await message.answer('Перешли координаты центра района, использовав вложения и выбрав нужную геолокацию'
						' или перешли их текстом')

@router.message(AdminStates.geo)
async def district2(message: Message, state: FSMContext):
	text = 'Выбери или введи радиус района в метрах'
	await state.set_state(AdminStates.radius)
	try:
		await state.update_data(lat=message.location.latitude, lon=message.location.longitude)
		await message.answer(text, reply_markup=adminMenu.pn_size)
	except(AttributeError):
		try:
			lat = re.findall(r'(\d+\.\d+),', message.text)[0]
			lon = re.findall(r', (\d+\.\d+)', message.text)[0]
			await state.update_data(lat=lat, lon=lon)
			await message.answer(text, reply_markup=adminMenu.pn_size)
		except(IndexError):
			await message.answer('Неверно введеные координаты, перешлите координаты координаты либо текстом'
								' в формате: двух дробных чисел через запятую с пробелом, либо через вложения')
			return

@router.message(AdminStates.radius)
async def geo10(message: Message, state: FSMContext):

	try:
		rad = int(message.text)
		await state.update_data(rad = rad)
		await state.set_state(AdminStates.add_dis)
		data = await state.get_data()
		await message.answer_location(latitude=data['lat'], longitude=data['lon'])
		await message.answer('Итого:\n'
							f'Район: {str(data["name"])}\n'
							   f'Размер зоны {rad}\n'
							f'Все верно?'
							, reply_markup=get_yes_no_dec('toch'))
	except:
		await message.answer('Введи положительное число')

@router.callback_query(yes_no_dec.filter(F.v=='toch'))
async def req3(query: CallbackQuery, state: FSMContext, callback_data: yes_no_dec):
	await query.message.edit_text(text=f'{query.message.text}')
	if callback_data.a == 'Yes':
		data = await state.get_data()
		await Config.db.add_dis(data["name"], data['lat'], data['lon'], data['rad'])
		await query.message.answer(f'Отлично район: {data["name"]} добавлен', reply_markup=adminMenu.district)
	else:
		await query.message.answer('Тогда попробуйте заново.', reply_markup=adminMenu.district)
	await state.clear()
