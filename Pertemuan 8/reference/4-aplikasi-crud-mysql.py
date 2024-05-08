import flet 
from flet import *
import mysql.connector

# CONECTION TO DB
mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "",
	database = "mp_appcrudsql"
)
cursor = mydb.cursor()

def main(page:Page):
	# mengatur halaman
	page.title = "Aplikasi Flet"

	# CREATE ADD INPUT
	inputan_nama = TextField(label = "Nama")
	inputan_umur = TextField(label = "Umur")

	# CREATE EDIT INPUT
	edit_inputan_nama = TextField(label = "Ubah Nama")
	edit_inputan_umur = TextField(label = "Ubah Umur")
	edit_id = Text()

	data_mahasiswa = DataTable(
		columns = [
			DataColumn(Text("ID")),
			DataColumn(Text("Nama")),
			DataColumn(Text("Umur")),
			DataColumn(Text("Opsi")),
		],
		rows = []
	)

	# DELETE FUNCTION
	def hapus_data(e):
		print("you selected id is = ", e.control.data['id'])
		try:
			sql = "DELETE FROM mahasiswa WHERE id = %s"
			val = (e.control.data['id'],)
			cursor.execute(sql, val)
			mydb.commit()
			print("you deleted !!!")
			data_mahasiswa.rows.clear()
			tampil_data_mahasiswa()

			# AND SHOW SNACKBAR
			page.snack_bar = SnackBar(
				Text("Data success Deleted",size = 30),
				bgcolor = "red"
			)
			page.snack_bar.open = True
			page.update()
		except Exception as e:
			print(e)
			print("error you code for delete")

	def simpan_ubah_data(e):
		try:
			sql = "UPDATE mahasiswa SET age = %s , name = %s WHERE id = %s"
			val = (edit_inputan_umur.value, edit_inputan_nama.value, edit_id.value)
			cursor.execute(sql, val)
			mydb.commit()
			print("you succes edit data")
			dialog.open = False		
			page.update()

			# CLEAR EDIT TEXTFIELD
			edit_inputan_nama.value = ""
			edit_inputan_umur.value = ""
			edit_id.value = ""

			data_mahasiswa.rows.clear()
			tampil_data_mahasiswa()

			# AND SHOW SNACKBAR
			page.snack_bar = SnackBar(
				Text("Data success EDIT",size = 30),
				bgcolor = "green"
			)
			page.snack_bar.open = True
			page.update()
		except Exception as e:
			print(e)
			print("ERROR SAVE EDIT !!!")

	# CREATE DIALOG SHOW WHEN YOU CLICK EDIT BUTTON
	dialog = AlertDialog(
		title = Text("Edit data"),
		content = Column([
			edit_inputan_nama,
			edit_inputan_umur
		]),
		actions = [
			TextButton("Simpan Perubahan",
				on_click = simpan_ubah_data
			)
		]
	)

	# EDIT FUNCTION
	def tampil_ubah_data(e):
		edit_inputan_nama.value = e.control.data['name']
		edit_inputan_umur.value = e.control.data['age']
		edit_id.value = e.control.data['id']
		page.dialog = dialog
		dialog.open = True
		page.update()
			

	def tampil_data_mahasiswa():
		# GET ALL DATA FROM DATABASE AND PUSH TO DATATABLE
		cursor.execute("SELECT * FROM mahasiswa")
		result = cursor.fetchall()

		# AND PUSH DATA TO DICT
		columns = [column[0] for column in cursor.description]
		rows = [dict(zip(columns,row)) for row in result]

		# LOOP AND PUSH
		for row in rows:
			data_mahasiswa.rows.append(
				DataRow(
					cells = [
						DataCell(Text(row['id'])),
						DataCell(Text(row['name'])),
						DataCell(Text(row['age'])),
						DataCell(
							Row([
								IconButton("delete",icon_color = "red",
									data = row,
									on_click = hapus_data
								),
								IconButton("create",icon_color = "red",
									data = row,
									on_click = tampil_ubah_data
								),
							])
						),
					]
				)

			)
		page.update()

	# AND CALL FUNCTION WHEN YOU APP IS FIRST OPEN
	tampil_data_mahasiswa()

	def simpan_data_baru(e):
		try:
			sql = "INSERT INTO mahasiswa (name,age) VALUES(%s,%s)"
			val = (inputan_nama.value,inputan_umur.value)
			cursor.execute(sql,val)
			mydb.commit()
			print(cursor.rowcount,"YOU RECORD INSERT !!!")

			# AND CLEAR ROWS IN TABLE AND PUSH FROM DATABASE AGAIN
			data_mahasiswa.rows.clear()
			tampil_data_mahasiswa()

			# AND SHOW SNACKBAR
			page.snack_bar = SnackBar(
				Text("Data success add",size = 30),
				bgcolor="green"

			)
			page.snack_bar.open = True
			page.update()
		except Exception as e:
			print(e)
			print("error you CODE !!!!")

		# AND AFTER YOU SUCCESS INPUT TO DB THEN CLEAR TEXTINPUT
		inputan_nama.value = ""
		inputan_umur.value = ""
		page.update()

	page.add(
		Column([
			inputan_nama,
			inputan_umur,
			ElevatedButton("Simpan Data Baru",
				on_click = simpan_data_baru
			),
			data_mahasiswa
		])
	)

flet.app(target=main)