from apps.carts.models import Cart



def create_cart(user):
    customer = user

    cart = Cart.objects.create(customer=customer)

    return cart