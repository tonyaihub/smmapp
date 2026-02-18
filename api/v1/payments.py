import stripe
from fastapi import APIRouter, Request, HTTPException
from ..models import User
from ..crud import update_user_subscription

stripe.api_key = "sk_test_..."

router = APIRouter()

@router.post("/create-checkout-session")
async def create_checkout(user = Depends(current_active_user)):
    try:
        session = stripe.checkout.Session.create(
            customer=user.stripe_customer_id or None,
            mode="subscription",
            payment_method_types=["card"],
            line_items=[{"price": "price_твой_pro_price_id", "quantity": 1}],
            success_url="https://твой-домен/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://твой-домен/cancel",
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, "твой_webhook_secret"
        )
    except ValueError:
        raise HTTPException(400)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # обнови user.subscription_tier = PRO
        # user.stripe_customer_id = session.customer
        # сохрани в БД
    return {"status": "success"}
