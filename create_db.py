from cafeteria import db
from models import User

if __name__ == '__main__':
    print("creating database...")
    db.create_all()
    print("creating admin account...")
    # creamos un usario admin y uno cajero
    admin = User(username='admin', email='admin@admin.com', cedula='0', type_user='admin')
    admin.set_password('nimda')
    # admin.save()
    cajero = User(username='cajero', email='cajero@cajero.com', cedula='1', type_user='cajero')
    cajero.set_password('orejac')
    # cajero.save()
    db.session.add(admin)
    db.session.add(cajero)
    db.session.commit()
    print("success!!!!!")
