# Database initial data
INITIAL_DATA = {
      'users': [
            {
                  'username': 'superuser',
                  'email': 'mitkomtoshev@gmail.com',
                  'hashed_password': 'Test1234_abkjsdjfak',
                  'is_active': True
            },
      ],
      'products': [
            {'name': 'Computer', 'is_active': True, 'price': 1500.00},
            {'name': 'Monitor', 'is_active': True, 'price': 500.00},
      ]
}


def seed_table(target, connection, **kw):
    table_name = str(target)
    if table_name in INITIAL_DATA and len(INITIAL_DATA[table_name]) > 0:
        connection.execute(target.insert(), INITIAL_DATA[table_name])
