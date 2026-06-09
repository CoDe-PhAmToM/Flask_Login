from pathlib import Path
import img2pdf

order = [
    'D:/EXAMEN_TEC_EMERGENTES/LOGIN/screenshots/register.png',
    'D:/EXAMEN_TEC_EMERGENTES/LOGIN/screenshots/register-success.png',
    'D:/EXAMEN_TEC_EMERGENTES/LOGIN/screenshots/login.png',
    'D:/EXAMEN_TEC_EMERGENTES/LOGIN/screenshots/agenda-after-login.png',
    'D:/EXAMEN_TEC_EMERGENTES/LOGIN/screenshots/agendar.png',
    'D:/EXAMEN_TEC_EMERGENTES/LOGIN/screenshots/flask-migrate-output.png',
    'D:/EXAMEN_TEC_EMERGENTES/LOGIN/screenshots/migration-file.png',
    'D:/EXAMEN_TEC_EMERGENTES/LOGIN/screenshots/flask-bcrypt-output.png',
]
out = Path('D:/EXAMEN_TEC_EMERGENTES/LOGIN/screenshots/ClinicVet_auth_migrations_bcrypt.pdf')
with open(out, 'wb') as f:
    f.write(img2pdf.convert(order))
print('PDF creado en', out)
