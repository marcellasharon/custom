{
    'name': 'Restaurant',  #nama modul yg dibaca user di UI
    'version': '1.0.0',
    'author': 'Marcella',
    'summary': 'Melihat Transaksi Restoran', #deskripsi singkat dari modul
    'description': 'Modul Restoran', #bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    #di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['base', 'sales_team'],  # list of dependencies, conditioning startup order
    'data': [
        'security/ir.model.access.csv',
        'views/customer_views.xml',
        'views/delivery_views.xml',
        'views/employee_views.xml',
        'views/bukumenu_views.xml',
        'views/orders_views.xml',
        'views/payment_views.xml',
        'views/kelas_views.xml',
        'wizard/wiz_restaurant_kelas_views.xml',
    ],
    'qweb':[],  #untuk memberi tahu static file, misal CSS
    'demo': [], #demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
}