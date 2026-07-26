

import os
import time


RAZORPAY_KEY_ID     = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")


try:
    import razorpay
    RAZORPAY_AVAILABLE = True
except ImportError:
    RAZORPAY_AVAILABLE = False


def is_razorpay_ready():
    """
    Razorpay use karne ke liye 3 cheezein chahiye:
    - Library install ho
    - KEY_ID .env mein ho
    - KEY_SECRET .env mein ho
    """
    return (
        RAZORPAY_AVAILABLE
        and bool(RAZORPAY_KEY_ID)
        and bool(RAZORPAY_KEY_SECRET)
        and not RAZORPAY_KEY_ID.startswith("rzp_test_xxx")  
    )


def is_saved_card_payment(razorpay_payment_id: str) -> bool:
    """
    Saved card / UPI se payment hua hai ya nahi check karo.
    Saved card payments mein payment_id 'savedcard_' se shuru hota hai.
    In payments mein OTP already verify ho chuka hota hai isliye
    Razorpay signature check ki zaroorat nahi hai.
    """
    return (
        razorpay_payment_id.startswith("savedcard_")
        or razorpay_payment_id.startswith("upi_")
        or razorpay_payment_id.startswith("mock_pay_")
    )


def create_order(amount_inr: float, receipt: str) -> dict:
    """
    Booking ke liye payment order banao.

    Razorpay ready hai to real order banao.
    Nahi to mock order banao (testing ke liye).
    """
    if is_razorpay_ready():
        # Real Razorpay order
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        rzp_order = client.order.create({
            "amount":          int(amount_inr * 100),  # Razorpay paise mein leta hai
            "currency":        "INR",
            "receipt":         receipt,
            "payment_capture": 1,
        })
        return {
            "order_id": rzp_order["id"],
            "amount":   amount_inr,
            "key_id":   RAZORPAY_KEY_ID,
            "mock":     False,
        }

    
    return {
        "order_id": f"mock_order_{int(time.time())}",
        "amount":   amount_inr,
        "key_id":   "mock_key",
        "mock":     True,
    }


def verify_payment(order_id: str, payment_id: str, signature: str) -> bool:
    """
    Payment sach mein hua ya nahi verify karo.

    3 cases hain:
    1. Saved card / UPI payment - OTP se verify hua tha, directly True
    2. Razorpay nahi hai - mock payment, directly True
    3. Razorpay hai - Razorpay se signature verify karo
    """

    # Case 1: Saved card or UPI payment 
    if is_saved_card_payment(payment_id):
        return True

    # Case 2: Razorpay check
    if not is_razorpay_ready():
        return True

    # Case 3: Real Razorpay payment
    try:
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        client.utility.verify_payment_signature({
            "razorpay_order_id":   order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature":  signature,
        })
        return True
    except Exception as e:
        print(f"[PAYMENT] Razorpay signature verify failed: {e}")
        return False
