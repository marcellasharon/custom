{
    'name': 'Coba3',  #nama modul yg dibaca user di UI
    'version': '1.0.0',
    'author': 'Marcella',
    'summary': 'Melihat Transaksi Coba3', #deskripsi singkat dari modul
    'description': 'Modul Coba3', #bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    #di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['base', 'sales_team'],  # list of dependencies, conditioning startup order
    'data': [
        'security/ir.model.access.csv',
        'views/novel_views.xml',
        'views/ResPartner_views.xml',
    ],
    'qweb':[],  #untuk memberi tahu static file, misal CSS
    'demo': [], #demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
}