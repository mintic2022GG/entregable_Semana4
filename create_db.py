from cafeteria import db
from models import User

if __name__ == '__main__':
    print("creating database...")
    db.create_all()
    print("creating admin account...")
    # creamos un usario admin y uno cajero
    admin = User(username='admin', email='admin@admin.com', cedula='0', type_user='admin', password='nimda')
    admin.save()
    cajero = User(username='cajero', email='cajero@cajero.com', cedula='1', type_user='cajero', password='orejac')
    cajero.save()
    print("success!!!!!")
