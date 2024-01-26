from django.http import HttpResponse
from django.shortcuts import render, redirect

from utils.filehandler import handle_file_upload

from .forms import *
from .models import *
import pandas as pd

# Create your views here.


def getTotalIncome():
    allInvoice = Invoice.objects.all()
    totalIncome = 0
    for curr in allInvoice:
        totalIncome += curr.total
    return totalIncome


def base(request):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()
    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
    }

    return render(request, "invoice/base/base.html", context)


def download_all(request):
    # Download all invoice to excel file
    # Download all product to excel file
    # Download all customer to excel file

    allInvoiceDetails = InvoiceDetail.objects.all()
    invoiceAndProduct = {
        "invoice_id": [],
        "invoice_date": [],
        "invoice_customer": [],
        "invoice_contact": [],
        "invoice_email": [],
        "invoice_comments": [],
        "product_name": [],
        "product_price": [],
        "product_unit": [],
        "product_amount": [],
        "invoice_total": [],

    }
    for curr in allInvoiceDetails:
        invoice = Invoice.objects.get(id=curr.invoice_id)
        product = Product.objects.get(id=curr.product_id)
        invoiceAndProduct["invoice_id"].append(invoice.id)
        invoiceAndProduct["invoice_date"].append(invoice.date)
        invoiceAndProduct["invoice_customer"].append(invoice.customer)
        invoiceAndProduct["invoice_contact"].append(invoice.contact)
        invoiceAndProduct["invoice_email"].append(invoice.email)
        invoiceAndProduct["invoice_comments"].append(invoice.comments)
        invoiceAndProduct["product_name"].append(product.product_name)
        invoiceAndProduct["product_price"].append(product.product_price)
        invoiceAndProduct["product_unit"].append(product.product_unit)
        invoiceAndProduct["product_amount"].append(curr.amount)
        invoiceAndProduct["invoice_total"].append(invoice.total)

    df = pd.DataFrame(invoiceAndProduct)
    df.to_excel("static/excel/allInvoices.xlsx", index=False)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="allInvoices.xlsx"'
    with open("static/excel/allInvoices.xlsx", "rb") as f:
        response.write(f.read())
    return response


def delete_all_invoice(request):
    # Delete all invoice
    Invoice.objects.all().delete()
    return redirect("view_invoice")


def upload_product_from_excel(request):
    # Upload excel file to static folder "excel"
    # add all product to database
    # save product to database
    # redirect to view_product
    excelForm = excelUploadForm(request.POST or None, request.FILES or None)
    print("Reached HERE!")
    if request.method == "POST":
        print("Reached HERE2222!")

        handle_file_upload(request.FILES["excel_file"])
        excel_file = "static/excel/masterfile.xlsx"
        df = pd.read_excel(excel_file)
        Product.objects.all().delete()
        for index, row in df.iterrows():
            product = Product(
                product_name=row["product_name"],
                product_price=row["product_price"],
                product_unit=row["product_unit"],
            )
            print(product)
            product.save()
        return redirect("view_product")
    return render(request, "invoice/upload_products.html", {"excelForm": excelForm})

    # Product view


def create_product(request):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()

    product = ProductForm()

    if request.method == "POST":
        product = ProductForm(request.POST)
        if product.is_valid():
            product.save()
            return redirect("create_product")

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        "product": product,
    }

    return render(request, "invoice/create_product.html", context)


def view_product(request):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()

    product = Product.objects.filter(product_is_delete=False)
    print(product)
    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        "product": product,
    }

    return render(request, "invoice/view_product.html", context)


# Customer view
def create_customer(request):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()

    customer = CustomerForm()

    if request.method == "POST":
        customer = CustomerForm(request.POST)
        if customer.is_valid():
            customer.save()
            return redirect("create_customer")

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "customer": customer,
    }

    return render(request, "invoice/create_customer.html", context)


def view_customer(request):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()

    customer = Customer.objects.all()

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "customer": customer,
    }

    return render(request, "invoice/view_customer.html", context)


# Invoice view
def create_invoice(request):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()

    form = InvoiceForm()
    formset = InvoiceDetailFormSet()
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        formset = InvoiceDetailFormSet(request.POST)
        if form.is_valid():
            invoice = Invoice.objects.create(
                customer=form.cleaned_data.get("customer"),
                contact=form.cleaned_data.get("contact"),
                email=form.cleaned_data.get("email"),
                date=form.cleaned_data.get("date"),
            )
        if formset.is_valid():
            total = 0
            for form in formset:
                product = form.cleaned_data.get("product")
                amount = form.cleaned_data.get("amount")
                if product and amount:
                    # Sum each row
                    sum = float(product.product_price) * float(amount)
                    # Sum of total invoice
                    total += sum
                    InvoiceDetail(
                        invoice=invoice, product=product, amount=amount
                    ).save()
            # Pointing the customer
            # points = 0
            # if total > 1000:
            #     points += total / 1000
            # # invoice.customer.customer_points = round(points)
            # # Save the points to Customer table
            # invoice.customer.save()

            # Save the invoice
            invoice.total = total
            invoice.save()
            return redirect("view_invoice")

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        "form": form,
        "formset": formset,
    }

    return render(request, "invoice/create_invoice.html", context)


def view_invoice(request):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()

    invoice = Invoice.objects.all()

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        "invoice": invoice,
    }

    return render(request, "invoice/view_invoice.html", context)


# Detail view of invoices
def view_invoice_detail(request, pk):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()

    invoice = Invoice.objects.get(id=pk)
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        # 'invoice': invoice,
        "invoice_detail": invoice_detail,
    }

    return render(request, "invoice/view_invoice_detail.html", context)


# Delete invoice
def delete_invoice(request, pk):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()

    invoice = Invoice.objects.get(id=pk)
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)
    if request.method == "POST":
        invoice_detail.delete()
        invoice.delete()
        return redirect("view_invoice")

    context = {
        "total_product": total_product,
        "total_customer": total_customer,##
        "total_invoice": total_invoice,
        "total_income": total_income,
        "invoice": invoice,
        "invoice_detail": invoice_detail,
    }

    return render(request, "invoice/delete_invoice.html", context)


# # Edit customer
def edit_customer(request, pk):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()

    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        customer = CustomerForm(request.POST, instance=customer)
        if customer.is_valid():
            customer.save()
            return redirect("view_customer")

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "customer": form,
    }

    return render(request, "invoice/create_customer.html", context)


# Delete customer
def delete_customer(request, pk):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()

    customer = Customer.objects.get(id=pk)

    if request.method == "POST":
        customer.delete()
        return redirect("view_customer")

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "customer": customer,
    }

    return render(request, "invoice/delete_customer.html", context)


# Edit product
def edit_product(request, pk):
    total_product = Product.objects.count()
    # total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()

    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == "POST":
        # customer = CustomerForm(request.POST, instance=product)

        product.save()
        return redirect("view_product")

    context = {
        "total_product": total_product,
        # "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        "product": form,
    }

    return render(request, "invoice/create_product.html", context)


# Delete product
def delete_product(request, pk):
    total_product = Product.objects.count()
    # total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()

    product = Product.objects.get(id=pk)

    if request.method == "POST":
        product.product_is_delete = True
        product.save()
        return redirect("view_product")

    context = {
        "total_product": total_product,
        # "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        "product": product,
    }

    return render(request, "invoice/delete_product.html", context)

#
#
#
#


# Importa los modelos y formularios necesarios
# from django.http import HttpResponse
# from django.shortcuts import render, redirect

# from .forms import CompraForm, DetalleCompraFormSet, ExcelUploadForm, ProductoForm
# from .models import Producto, Proveedor, Compra, Detallecompra

# import pandas as pd

# Resto del código

# def getTotalIncome():
#     allCompras = Compra.objects.all()
#     totalIncome = 0
#     for compra in allCompras:
#         totalIncome += compra.total
#     return totalIncome

# # Resto del código

# def base(request):
#     total_producto = Producto.objects.count()
#     total_compra = Compra.objects.count()
#     total_income = getTotalIncome()
#     context = {
#         "total_producto": total_producto,
#         "total_compra": total_compra,
#         "total_income": total_income,
#     }

#     return render(request, "invoice/base/base.html", context)

# # Resto del código

# def download_all(request):
#     # Descargar todas las compras a un archivo Excel

#     allDetalleCompras = Detallecompra.objects.all()
#     compraAndDetalle = {
#         "compra_id": [],
#         "date": [],
#         "contact": [],
#         "email": [],
#         "comments": [],
#         "nombre": [],
#         "precio": [],
#         "unidad": [],
#         "cantidad": [],
#         "total": [],
#     }

#     for detalleCompra in allDetalleCompras:
#         if detalleCompra.compra is not None:
#             compra = detalleCompra.compra
#             producto = detalleCompra.producto
#             compraAndDetalle["compra_id"].append(compra.id)
#             compraAndDetalle["date"].append(compra.fecha_compra)
#             compraAndDetalle["contacto"].append(compra.contact)
#             compraAndDetalle["email"].append(compra.email)
#             compraAndDetalle["comments"].append(compra.comments)
#             compraAndDetalle["nombre"].append(producto.nombre)
#             compraAndDetalle["precio"].append(producto.precio)
#             compraAndDetalle["unidad"].append(producto.stock)
#             compraAndDetalle["cantidad"].append(detalleCompra.cantidad)
#             compraAndDetalle["total"].append(detalleCompra.get_total_bill)
# # <a class="collapse-item" href="{% url 'download_all_compra' %}">Descagar</a> 
# #  <a class="collapse-item" href="{% url 'delete_all_compra' %}">Eliminar</a>

#     df = pd.DataFrame(compraAndDetalle)
#     df.to_excel("static/excel/allCompras.xlsx", index=False)
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="allCompras.xlsx"'
#     with open("static/excel/allCompras.xlsx", "rb") as f:
#         response.write(f.read())
#     return response

# def delete_all_compra(request):
#     # Delete all invoice
#     Invoice.objects.all().delete()
#     return redirect("view_compra")

# # Resto del código

# def create_compra(request):
#     total_product = Producto.objects.count()
#     total_compra = Compra.objects.count()
#     total_income = getTotalIncome()

#     form = CompraForm()
#     formset = DetalleCompraFormSet()
#     if request.method == "POST":
#         form = CompraForm(request.POST)
#         formset = DetalleCompraFormSet(request.POST)
#         if form.is_valid():
#             compra = form.save(commit=False)
#             compra.total = 0  # inicializar el total
#             compra.save()
#         if formset.is_valid():
#             total = 0
#             for form in formset:
#                 detalleCompra = form.save(commit=False)
#                 detalleCompra.compra = compra
#                 detalleCompra.subtotal = detalleCompra.get_total_bill
#                 detalleCompra.save()
#                 total += detalleCompra.subtotal
#             compra.total = total
#             compra.save()
#             return redirect("view_compra")

#     context = {
#         "total_product": total_product,
#         "total_compra": total_compra,
#         "total_income": total_income,
#         "form": form,
#         "formset": formset,
#     }

#     return render(request, "invoice/create_compra.html", context)

# # Resto del código

# def view_compra(request):
#     total_producto = Producto.objects.count()
#     total_compra = Compra.objects.count()
#     total_income = getTotalIncome()

#     compras = Compra.objects.all()

#     context = {
#         "total_producto": total_producto,
#         "total_compra": total_compra,
#         "total_income": total_income,
#         "compras": compras,
#     }

#     return render(request, "invoice/view_compra.html", context)

# # Resto del código

# def view_compra_detail(request, pk):
#     total_producto = Producto.objects.count()
#     total_compra = Compra.objects.count()
#     total_income = getTotalIncome()

#     compra = Compra.objects.get(id=pk)
#     detalleCompras = Detallecompra.objects.filter(compra=compra)

#     context = {
#         "total_producto": total_producto,
#         "total_compra": total_compra,
#         "total_income": total_income,
#         "compra": compra,
#         "detalleCompras": detalleCompras,
#     }

#     return render(request, "invoice/view_compra_detail.html", context)

# # Resto del código

# def delete_compra(request, pk):
#     total_producto = Producto.objects.count()
#     total_compra = Compra.objects.count()
#     total_income = getTotalIncome()

#     compra = Compra.objects.get(id=pk)
#     detalleCompras = Detallecompra.objects.filter(compra=compra)
#     if request.method == "POST":
#         detalleCompras.delete()
#         compra.delete()
#         return redirect("view_compra")

#     context = {
#         "total_producto": total_producto,
#         "total_compra": total_compra,
#         "total_income": total_income,
#         "compra": compra,
#         "detalleCompras": detalleCompras,
#     }

#     return render(request, "invoice/delete_compra.html", context)


# def view_producto(request):
#     total_producto = Producto.objects.count()
#     total_compra = Compra.objects.count()
#     total_income = getTotalIncome()

#     productos = Producto.objects.filter(estado=1)  # Filtra los productos activos
#     context = {
#         "total_producto": total_producto,
#         "total_compra": total_compra,
#         "total_income": total_income,
#         "productos": productos,
#     }

#     return render(request, "invoice/view_producto.html", context)

# def create_producto(request):
#     total_producto = Producto.objects.count()
#     total_compra = Compra.objects.count()
#     total_income = getTotalIncome()

#     form = ProductForm()

#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("view_producto")

#     context = {
#         "total_producto": total_producto,
#         "total_compra": total_compra,
#         "total_income": total_income,
#         "form": form,
#     }

#     return render(request, "invoice/create_producto.html", context)


# def edit_producto(request, pk):
#     total_producto = Producto.objects.count()
#     total_compra = Compra.objects.count()
#     total_income = getTotalIncome()

#     producto = Producto.objects.get(id=pk)
#     form = ProductoForm(instance=producto)

#     if request.method == "POST":
#         form = ProductoForm(request.POST, instance=producto)
#         if form.is_valid():
#             form.save()
#             return redirect("view_producto")

#     context = {
#         "total_producto": total_producto,
#         "total_compra": total_compra,
#         "total_income": total_income,
#         "producto": form,
#     }

#     return render(request, "invoice/create_producto.html", context)

# # Resto del código

# def delete_producto(request, pk):
#     total_producto = Producto.objects.count()
#     total_compra = Compra.objects.count()
#     total_income = getTotalIncome()

#     producto = Producto.objects.get(id=pk)

#     if request.method == "POST":
#         producto.estado = 0  # establecer estado a inactivo
#         producto.save()
#         return redirect("view_producto")

#     context = {
#         "total_producto": total_producto,
#         "total_compra": total_compra,
#         "total_income": total_income,
#         "producto": producto,
#     }

#     return render(request, "invoice/delete_producto.html", context)


# def create_proveedor(request):
#     total_producto = Producto.objects.count()
#     total_compra = Compra.objects.count()
#     total_income = getTotalIncome()

#     form = ProveedorForm()
#     if request.method == "POST":
#         form = ProveedorForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("view_proveedor")

#     context = {
#         "total_producto": total_producto,
#         "total_compra": total_compra,
#         "total_income": total_income,
#         "form": form,
#     }

#     return render(request, "invoice/create_proveedor.html", context)



# def view_proveedor(request):
#     total_producto = Producto.objects.count()
#     total_compra = Compra.objects.count()
#     total_income = getTotalIncome()

#     proveedores = Proveedor.objects.all()

#     context = {
#         "total_producto": total_producto,
#         "total_compra": total_compra,
#         "total_income": total_income,
#         "proveedores": proveedores,
#     }

#     return render(request, "invoice/view_proveedor.html", context)



# def delete_proveedor(request, pk):
#     total_producto = Producto.objects.count()
#     total_compra = Compra.objects.count()
#     total_income = getTotalIncome()

#     proveedor = Proveedor.objects.get(id=pk)

#     if request.method == "POST":
#         proveedor.delete()
#         return redirect("view_proveedor")

#     context = {
#         "total_producto": total_producto,
#         "total_compra": total_compra,
#         "total_income": total_income,
#         "proveedor": proveedor,
#     }

#     return render(request, "invoice/delete_proveedor.html", context)



# def edit_proveedor(request, pk):
#     total_producto = Producto.objects.count()
#     total_compra = Compra.objects.count()
#     total_income = getTotalIncome()

#     proveedor = Proveedor.objects.get(id=pk)
#     form = ProveedorForm(instance=proveedor)

#     if request.method == "POST":
#         form = ProveedorForm(request.POST, instance=proveedor)
#         if form.is_valid():
#             form.save()
#             return redirect("view_proveedor")

#     context = {
#         "total_producto": total_producto,
#         "total_compra": total_compra,
#         "total_income": total_income,
#         "proveedor": form,
#     }

#     return render(request, "invoice/edit_proveedor.html", context)
# # 
# # 
# # 
# # 
# def getTotalIncome():
#     allInvoice = Invoice.objects.all()
#     totalIncome = 0
#     for curr in allInvoice:
#         totalIncome += curr.total
#     return totalIncome


# def base(request):
#     total_product = Product.objects.count()
#     total_customer = Customer.objects.count()
#     total_invoice = Invoice.objects.count()
#     total_income = getTotalIncome()
#     context = {
#         "total_product": total_product,
#         "total_customer": total_customer,
#         "total_invoice": total_invoice,
#         "total_income": total_income,
#     }

#     return render(request, "invoice/base/base.html", context)
def getTotalcomprado():
    allCompra = Compra.objects.all()
    totalCompra = 0
    for curr in allCompra:
        totalCompra += curr.total
    return totalCompra


def base1(request):
    total_producto = Producto.objects.count()
    total_proveedor = Proveedor.objects.count()
    total_compra = Compra.objects.count()
    total_comprado = getTotalcomprado()
    context = {
        "total_producto": total_producto,
        "total_proveedor": total_proveedor,
        "total_compra": total_compra,
        "total_comprado": total_comprado,
    }

    return render(request, "invoice/base/base1.html", context)

def download_all(request):
    # Download all invoice to excel file
    # Download all product to excel file
    # Download all customer to excel file

    allDetalleCompras = Detallecompra.objects.all()
    compraAndProducto = {
        "compra_id": [],
        "date": [],
        "proveedor": [],
        "cod_factura": [],
        "compra_contacto": [],
        # "invoice_comments": [],
        "nombre": [],
        "precio": [],
        "stock": [],
        "cantidad": [],
        "total": [],

    }
# <!-- <a class="collapse-item" href="{% url 'download_all' %}">Descagar</a> 
#                         <a class="collapse-item" href="{% url 'delete_all_compra' %}">Eliminar</a> -->
    
    for curr in allDetalleCompras:
        compra = Compra.objects.get(id=curr.compra_id)
        producto = Producto.objects.get(id=curr.producto_id)
        compraAndProducto["compra_id"].append(compra.id)
        compraAndProducto["compra_fecha_compra"].append(compra.date)
        compraAndProducto["compra_proveedor"].append(compra.proveedor)
        compraAndProducto["cod_factura"].append(compra.cod_factura)
        compraAndProducto["compra_contacto"].append(compra.contacto)
        # compraAndProducto["invoice_comments"].append(compra.comments)
        compraAndProducto["nomber"].append(producto.nombre)
        compraAndProducto["precio"].append(producto.precio)
        compraAndProducto["stock"].append(producto.stock)
        compraAndProducto["cantidad"].append(curr.cantidad)
        compraAndProducto["total"].append(compra.total)
        
  
    df = pd.DataFrame(compraAndProducto)
    df.to_excel("static/excel/allCompras.xlsx", index=False)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="allCompras.xlsx"'
    with open("static/excel/allCompras.xlsx", "rb") as f:
        response.write(f.read())
    return response

def delete_all_compra(request):
    # Delete all invoice
    Compra.objects.all().delete()
    return redirect("view_compra")



def subir_producto_from_excel(request):
    # Upload excel file to static folder "excel"
    # add all product to database
    # save product to database
    # redirect to view_product
    excelForm = excelSubirForm(request.POST or None, request.FILES or None)
    print("Reached HERE!")
    if request.method == "POST":
        print("Reached HERE2222!")

        handle_file_upload(request.FILES["excel_file"])
        excel_file = "static/excel/masterfile.xlsx"
        df = pd.read_excel(excel_file)
        Producto.objects.all().delete()
        for index, row in df.iterrows():
            producto = Producto(
                nombre=row["nombre"],
                precio=row["precio"],
                stock=row["stock"],
            )
            print(producto)
            producto.save()
        return redirect("view_producto")
    return render(request, "invoice/upload_productos.html", {"excelForm": excelForm})

    # Product view


def create_producto(request):
    total_producto = Producto.objects.count()
    total_proveedor = Proveedor.objects.count()
    total_compra = Compra.objects.count()
    total_vendido = getTotalcomprado()

    producto = ProductoForm()

    if request.method == "POST":
        producto = ProductForm(request.POST)
        if producto.is_valid():
            producto.save()
            return redirect("create_product")

    context = {
        "total_producto": total_producto,
        "total_proveedor": total_proveedor,
        "total_compre": total_compra,
        "total_vendido": total_vendido,
        "producto": producto,
    }

    return render(request, "invoice/create_producto.html", context)


def view_producto(request):
    total_producto = Producto.objects.count()
    total_proveedor = Proveedor.objects.count()
    total_compra = Compra.objects.count()
    total_vendido = getTotalcomprado()

    producto = Producto.objects.filter(estado=False)
    print(producto)
    context = {
        "total_producto": total_producto,
        "total_proveedor": total_proveedor,
        "total_compre": total_compra,
        "total_vendido": total_vendido,
        "producto": producto,
    }

    return render(request, "invoice/view_producto.html", context)


# Customer view
def create_proveedor(request):
    total_producto = Producto.objects.count()
    total_proveedor = Proveedor.objects.count()
    total_compra = Compra.objects.count()
    

    proveedor = ProveedorForm()

    if request.method == "POST":
        proveedor = ProveedorForm(request.POST)
        if proveedor.is_valid():
            proveedor.save()
            return redirect("create_proveedor")

    context = {
        "total_producto": total_producto,
        "total_proveedor": total_proveedor,
        "total_compre": total_compra,
        "proveedor": proveedor,
    }

    return render(request, "invoice/create_proveedor.html", context)


def view_proveedor(request):
    total_producto = Producto.objects.count()
    total_proveedor = Proveedor.objects.count()
    total_compra = Compra.objects.count()

    proveedor = Proveedor.objects.all()

    context = {
        "total_producto": total_producto,
        "total_proveedor": total_proveedor,
        "total_compre": total_compra,
        "proveedor": proveedor,
    }

    return render(request, "invoice/view_proveedor.html", context)


# Invoice view
def create_compra(request):
    total_producto = Producto.objects.count()
    total_proveedor = Proveedor.objects.count()
    total_compra = Compra.objects.count()
    total_vendido = getTotalcomprado()

    form = CompraForm()
    formset = DetalleCompraFormSet()
    if request.method == "POST":
        form = CompraForm(request.POST)
        formset = DetalleCompraFormSet(request.POST)
        if form.is_valid():
                compra = Compra.objects.create(
                proveedor=form.cleaned_data.get("proveedor"),
                contacto=form.cleaned_data.get("contacto"),
                cod_factura=form.cleaned_data.get("cod_factura"),
                date=form.cleaned_data.get("date"),
            )
                
        if formset.is_valid():
            total = 0
            for form in formset:
                producto = form.cleaned_data.get("producto")
                cantidad = form.cleaned_data.get("cantidad")
                if producto and cantidad:
                    # Sum each row
                    sum = float(producto.precio) * float(cantidad)
                    # Sum of total invoice
                    total += sum
                    Detallecompra(
                        compra=compra, product=producto, cantidad=cantidad
                    ).save()
            # Pointing the customer
            # points = 0
            # if total > 1000:
            #     points += total / 1000
            # # invoice.customer.customer_points = round(points)
            # # Save the points to Customer table
            # invoice.customer.save()

            # Save the invoice
            compra.total = total
            compra.save()
            return redirect("view_compra")

    context = {
        "total_producto": total_producto,
        "total_proveedor": total_proveedor,
        "total_compra": total_compra,
        "total_vendido": total_vendido,
        "form": form,
        "formset": formset,
    }

    return render(request, "invoice/create_compra.html", context)


def view_compra(request):
    total_producto = Producto.objects.count()
    total_proveedor = Proveedor.objects.count()
    total_compra = Compra.objects.count()
    total_comprado = getTotalcomprado()

    compra = Compra.objects.all()

    context = {
        "total_produco": total_producto,
        "total_proveedor": total_proveedor,
        "total_compra": total_compra,
        "total_comprado": total_comprado,
        "compra": compra,
    }

    return render(request, "invoice/view_compra.html", context)


# Detail view of invoices
def view_compra_detail(request, pk):
    total_producto = Producto.objects.count()
    total_proveedor = Proveedor.objects.count()
    total_compra = Compra.objects.count()
    total_comprado = getTotalcomprado()

    compra = Compra.objects.get(id=pk)
    detallecompra = Detallecompra.objects.filter(compra=compra)

    context = {
        "total_producto": total_producto,
        " total_proveedor":  total_proveedor,
        "total_compra": total_compra,
        "total_comprado": total_comprado,
        # 'invoice': invoice,
        "invoice_detail": detallecompra,
    }

    return render(request, "invoice/view_compra_detail.html", context)


# Delete invoice
def delete_compra(request, pk):
    total_producto = Producto.objects.count()
    total_proveedor = Proveedor.objects.count()
    total_compra = Compra.objects.count()
    total_comprado = getTotalcomprado()

    compra = Compra.objects.get(id=pk)
    detallecompra = Detallecompra.objects.filter(compra=compra)
    if request.method == "POST":
        detallecompra.delete()
        compra.delete()
        return redirect("view_compra")

    context = {
        "total_producto": total_producto,
        "total_proveedor":  total_proveedor,
        "total_compra": total_compra,
        "total_comprado": total_comprado,
        # 'compra': compra,
        "invoice_detail": detallecompra,
    }

    return render(request, "invoice/delete_compra.html", context)


# # Edit customer
def edit_proveedor(request, pk):
    total_producto = Producto.objects.count()
    total_proveedor = Proveedor.objects.count()
    total_compra = Compra.objects.count()

    proveedor = Proveedor.objects.get(id=pk)
    form = ProveedorForm(instance=proveedor)

    if request.method == "POST":
        proveedor = ProveedorForm(request.POST, instance=proveedor)
        if proveedor.is_valid():
            proveedor.save()
            return redirect("view_proveedor")

    context = {
        "total_producto": total_producto,
        "total_proveedor":  total_proveedor,
        "total_compra": total_compra,
        "proveedor": form,
    }

    return render(request, "invoice/create_proveedor.html", context)


# Delete customer
def delete_proveedor(request, pk):
    total_producto = Producto.objects.count()
    total_proveedor = Proveedor.objects.count()
    total_compra = Compra.objects.count()

    proveedor = Proveedor.objects.get(id=pk)

    if request.method == "POST":
        proveedor.delete()
        return redirect("view_prveedor")

    context = {
        "total_producto": total_producto,
        "total_proveedor":  total_proveedor,
        "total_compra": total_compra,
        "proveedor": proveedor,
    }

    return render(request, "invoice/delete_proveedor.html", context)


# Edit product
def edit_producto(request, pk):
    total_producto = Producto.objects.count()
    total_proveedor = Proveedor.objects.count()
    total_compra = Compra.objects.count()
    total_comprado = getTotalcomprado()

    producto = Producto.objects.get(id=pk)
    form = ProductoForm(instance=producto)

    if request.method == "POST":
        # customer = CustomerForm(request.POST, instance=product)

        producto.save()
        return redirect("view_producto")

    context = {
        "total_producto": total_producto,
        "total_proveedor": total_proveedor,
        "total_compra": total_compra,
        "total_comprado": total_comprado,
        "producto": form,
    }

    return render(request, "invoice/create_producto.html", context)


# Delete product
def delete_producto(request, pk):
    total_producto = Producto.objects.count()
    total_proveedor = Proveedor.objects.count()
    total_compra = Compra.objects.count()
    total_comprado = getTotalcomprado()

    producto = Producto.objects.get(id=pk)

    if request.method == "POST":
        producto.estado = True
        producto.save()
        return redirect("view_producto")

    context = {
        "total_producto": total_producto,
        "total_proveedor": total_proveedor,
        "total_compra": total_compra,
        "total_comprado": total_comprado,
        "producto": producto,
    }

    return render(request, "invoice/delete_product.html", context)



