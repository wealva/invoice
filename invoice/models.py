from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    usuario_creacion = models.CharField(max_length=20)
    usuario_modificacion = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(default=1)

    class Meta:
        db_table = 'Categorias'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['fecha_creacion']

# class Product(models.Model):
#     product_name = models.CharField(max_length=255)  #product_name
#     descripcion = models.TextField()
#     product_price = models.FloatField(default=0)  #product_price
#     product_unit = models.CharField(max_length=255) #product_unit
#     usuario_creacion = models.CharField(max_length=20)
#     usuario_modificacion = models.CharField(max_length=20)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     fecha_modificacion = models.DateTimeField(auto_now=True)
#     product_is_delete = models.BooleanField(default=False)   #product_is_delete
#     categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)   

#     class Meta:
#         db_table = 'Productos'
#         verbose_name = 'Producto'
#         verbose_name_plural = 'Productos'
#         ordering = ['fecha_creacion']
#     def __str__(self):
#         return str(self.product_name)
    
# class Customer(models.Model):
#     GENDER_CHOICES = (
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#         ('Others', 'Others'),
#     )
#     customer_name = models.CharField(max_length=255)  #customer_name
#     customer_gender = models.CharField(max_length=50, choices=GENDER_CHOICES) #customer_gender
#     customer_dob = models.DateField()
#     contacto = models.CharField(max_length=255)
#     telefono = models.CharField(max_length=15)
#     direccion = models.TextField()
#     usuario_creacion = models.CharField(max_length=20)
#     usuario_modificacion = models.CharField(max_length=20)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     fecha_modificacion = models.DateTimeField(auto_now=True)
#     estado = models.IntegerField(default=1)

#     class Meta:
#         db_table = 'Clientes'
#         verbose_name = 'Cliente'
#         verbose_name_plural = 'Clientes'
#         ordering = ['fecha_creacion']



# class Invoice(models.Model):
#     total = models.FloatField(default=0)  # total
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)   #customer
#     cod_factura = models.CharField(max_length=20)   #contact
#     n_factura = models.CharField(max_length=20)    #email
#     date = models.DateField(auto_now_add=True)   #date
#     contact = models.CharField(max_length=255, default='', blank=True, null=True)
#     email = models.EmailField(default='', blank=True, null=True)
#     comments = models.TextField(default='', blank=True, null=True)
#     usuario_creacion = models.CharField(max_length=20)
#     usuario_modificacion = models.CharField(max_length=20)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     fecha_modificacion = models.DateTimeField(auto_now=True)
#     estado = models.IntegerField(default=1)

#     class Meta:
#         db_table = 'Cabecera de Factura'
#         ordering = ['fecha_creacion']

#     def __str__(self):
#         return str(self.id)

# class InvoiceDetail(models.Model):
#     invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, blank=True, null=True)
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
#     amount = models.IntegerField(default=1)   #amount
#     pvp = models.DecimalField(max_digits=10, decimal_places=1)
#     subtotal = models.DecimalField(max_digits=12,decimal_places=1)
#     usuario_creacion = models.CharField(max_length=20)
#     usuario_modificacion = models.CharField(max_length=20)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     fecha_modificacion = models.DateTimeField(auto_now=True)
#     estado = models.IntegerField(default=1)

#     class Meta:
#         db_table = 'Detalle de Factura'
#         ordering = ['fecha_creacion']

#     @property
#     def get_total_bill(self):
#         total = float(self.product.product_price) * float(self.amount)
#         return total
    

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_price = models.FloatField(default=0)
    product_unit = models.CharField(max_length=255)
    product_is_delete = models.BooleanField(default=False)
    usuario_creacion = models.CharField(max_length=20)
    usuario_modificacion = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    # categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product_name)


class Customer(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    customer_name = models.CharField(max_length=255)
    customer_gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    customer_dob = models.DateField()
    customer_points = models.IntegerField(default=0)
    usuario_creacion = models.CharField(max_length=20)
    usuario_modificacion = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(default=1)

    def __str__(self):
        return str(self.customer_name)


class Invoice(models.Model):
    date = models.DateField(auto_now_add=True)
    customer = models.TextField(default='')
    contact = models.CharField(
        max_length=255, default='', blank=True, null=True)
    email = models.EmailField(default='', blank=True, null=True)
    comments = models.TextField(default='', blank=True, null=True)
    total = models.FloatField(default=0)
    usuario_creacion = models.CharField(max_length=20)
    usuario_modificacion = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)


class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField(default=1)
    usuario_creacion = models.CharField(max_length=20)
    usuario_modificacion = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(default=1)

    @property
    def get_total_bill(self):
        total = float(self.product.product_price) * float(self.amount)
        return total


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    usuario_creacion = models.CharField(max_length=20)
    usuario_modificacion = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(default=1)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['fecha_creacion']
    def __str__(self):
        return str(self.nombre)


class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    contacto = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    usuario_creacion = models.CharField(max_length=20)
    usuario_modificacion = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(default=1)

    class Meta:
        db_table = 'Proveedores'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['fecha_creacion']

    def __str__(self):
        return str(self.nombre)

class Compra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    total = models.FloatField(default=0)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    cod_factura = models.CharField(max_length=20)   #contact
    n_factura = models.CharField(max_length=20)    #email
    date= models.DateField()   #date
    contacto = models.CharField(max_length=255, default='', blank=True, null=True)
    email = models.EmailField(default='', blank=True, null=True)
    comments = models.TextField(default='', blank=True, null=True)
    usuario_creacion = models.CharField(max_length=20)
    usuario_modificacion = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(default=1)

    class Meta:
        db_table = 'Compra'
        ordering = ['fecha_creacion']

    def __str__(self):
        return str(self.id)

class Detallecompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.SET_NULL, blank=True, null=True)   #invoice
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, blank=True, null=True) #product
    cantidad = models.IntegerField(default=1)   #amount
    pvp = models.DecimalField(max_digits=10, decimal_places=1)
    subtotal = models.DecimalField(max_digits=12,decimal_places=1)
    usuario_creacion = models.CharField(max_length=20)
    usuario_modificacion = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(default=1)

    class Meta:
        db_table = 'Detalle de compra'
        ordering = ['fecha_creacion']

    @property
    def get_total_bill(self):
        total = float(self.producto.precio) * float(self.cantidad)
        return total


    

    # Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process  ./activate
    # django-admin startproject proyecto .
    # django-admin startapp app
    # python manage.py makemigrations
    # python manage.py migrate
    # python manage.py createsuperuser  administrador   951753
    # python manage.py runserver




# black==21.8b0
# click==8.0.1
# colorama==0.4.4
# mypy-extensions==0.4.3
# pathspec==0.9.0
# platformdirs==2.3.0
# regex==2021.8.28
# tomli==1.2.1
# six==1.16.0
# pandas==1.5.2
# openpyxl==3.0.10