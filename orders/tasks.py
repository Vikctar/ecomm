import africastalking
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from orders.models import Order


@shared_task
def send_order_sms(order_id):
    """Send SMS notification to customer"""
    try:
        order = Order.objects.get(id=order_id)

        # Initialize Africa's Talking
        africastalking.initialize(
            settings.AFRICASTALKING_USERNAME,
            settings.AFRICASTALKING_API_KEY
        )
        sms = africastalking.SMS

        message = f"Hi {order.customer.user.first_name}, your order #{order.id} has been placed successfully! Total: ${order.total_amount}"

        response = sms.send(message, [order.customer.phone_number])
        print(f"SMS sent: {response}")

    except Exception as e:
        print(f"SMS sending failed: {e}")


@shared_task
def send_order_email(order_id):
    """Send email notification to admin"""
    try:
        order = Order.objects.get(id=order_id)

        subject = f"New Order Placed - #{order.id}"
        message = f"""
        New order details:

        Order ID: #{order.id}
        Customer: {order.customer.user.get_full_name()} ({order.customer.user.email})
        Phone: {order.customer.phone_number}
        Total Amount: ${order.total_amount}
        Status: {order.status}
        Items:
        """

        for item in order.items.all():
            message += f"- {item.product.name} x{item.quantity} @ ${item.price} = ${item.subtotal}\n"

        message += f"\nOrder placed at: {order.created_at}"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],  # Send to admin
            fail_silently=False,
        )

    except Exception as e:
        print(f"Email sending failed: {e}")