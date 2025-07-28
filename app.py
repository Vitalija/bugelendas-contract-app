from flask import Flask, render_template, request
from fpdf import FPDF
import dropbox
import os
from datetime import datetime

app = Flask(__name__)

DROPBOX_ACCESS_TOKEN = "sl.u.AF6gNDMm4w9UfUvN-DL2HpB1iRKq8LEDvQi6F1vo5w6pkg8rRRO7BhFfJPxNViHsSVvzhQV-oB6iFCtSYbuesz3eeN9ipNgCyuU68W63WLvbBnfE3n8z4a5RNrYxm416iHWpPlP2ZfQroYtiJbo1iuVFsC4wIv8lEGbOf-YOJbomJhiLv-GedntPd3BlG9Iod335lNHe0FSXURvrfTgmESVKZJCEqvC58kRrh3jQ_so8RiICLg2-VMr0qbjbBkrVQ94aBRF32UBwmAufj4xjv6mGhr6IuQAMeC58xoZp-OUvtMdNLStgdq4uAafNdVTJA7HZ4Hb3jmv5OTAbP2eu4UcXdaTXpCO11fZdxQL9-HCiBImH5yjl5FnX7-KpKPia_vlGwWg8XmplQ2huShIW6aw56H6Y9PJ5D2svF8E_DE6h5tNzPmwpltUPpm99Lo8nxqj9rPZ2pwC2Tav1d7Lz8XnCcVo4zg3MF8Xu1Ll-DqnRU9Ew9MLHVdiJnP721HK0J1_YzNdDCP17V8vt7YJqO7D2yf8ZWwFKOxXxIknbiQhnrxfz16nCk4rnSxUh_Gp4Nw0mKQZ16RvpxxtrJoVLI23FGqyZZqvsV5XZJ4uxdtCOA4zud_gydptx6l_aQ3V3BahGmbFd9eeDPhjZWOh0i7sUmY1FVLPyaTrqkJEXi005Hjps7Bvcvf_hcyq7LAu3phngQx6IcQ-Q9YHrXeOacOI6f8aSnylvHmBdlI5Y1Gp2YAUPVTgCJmDSUH_aEWSfhqLn3eEX4YlFWRiO9ZxrqZHaxskoqiOH6MSBkBD4mkzPxOF1eYFYPjHZsS02-iHK4GUDf-oaEFrZqbGFpYYbrzip1_Yj8qYhK8oUZ7tJ6umv1BJRotr_YjU-l8cKncdV-w9WcPTgwHJBR6Hk5o99q3rWujNA3Snj4MYiBWM8j7b3j2fnxSpiiuJZMdEV5pt3rjeyO3KIs-dBsAST49kVMMMKqWUi3I0DmObfr6_EBVWDh60uwTrG6j0a10r3VyeZaC9YYG-WoJD8P221u5nJ7uXRyMMDLm2cEww3OYbPKRqEcSe17K7eg9spXTO28AvSvErYpJof_amUg-SBOrSngvi0-Ws6UdFAMHpuEzTMXEQjNZVr6cQIC3Hum3Nh5klXfjCIF6V_ZTRP7QUv7lL_SZe7_FfBHkBgfk3E7to0juWcJh85zvc_HqY29auyEZyX-RpO56avVnYt-jxx9XxuExi-tJhm7JeRNjVlF_yKRUrWR5lV32ueewiaB3nHDIaEZBFW-2ebh-Z16PDFH6g5641_"

@app.route('/', methods=['GET', 'POST'])
def contract():
    if request.method == 'POST':
        # 1. Gaunami duomenys iš formos
        full_name = request.form['full_name']
        birth_date = request.form['birth_date']
        phone = request.form['phone']
        email = request.form['email']
        city = request.form['city']
        parent_name = request.form['parent_name']
        camp_session = request.form['camp_session']

        # 2. PDF sukūrimas
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.multi_cell(0, 10, txt=f""" 
BUGELENDAS STOVYKLOS SUTARTIS

1. Vaiko vardas ir pavardė: {full_name}
2. Gimimo data: {birth_date}
3. Miestas: {city}
4. Vienas iš tėvų/globėjų: {parent_name}
5. Kontaktinis telefonas: {phone}
6. El. paštas: {email}
7. Pasirinkta pamaina: {camp_session}

Pasirašydamas sutinku su visomis stovyklos taisyklėmis ir įsipareigoju sumokėti 290 EUR.
""")

        filename = f"bugelendas_sutartis_{full_name.replace(' ', '_')}.pdf"
        pdf.output(filename)

        # 3. Įkėlimas į Dropbox
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        with open(filename, "rb") as f:
            dbx.files_upload(f.read(), f"/bugelendas/{filename}", mode=dropbox.files.WriteMode("overwrite"))

        os.remove(filename)

        return "Sutartis sėkmingai pateikta!"

    return render_template('contract_form.html')

