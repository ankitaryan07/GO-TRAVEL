

import os

# ── SendGrid config ──────────────────────────────────────────────
SENDGRID_API_KEY    = os.getenv("SENDGRID_API_KEY", "")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "")
SENDGRID_FROM_NAME  = os.getenv("SENDGRID_FROM_NAME", "GO-TRAVEL")

# ── SMTP Gmail config (fallback) ─────────────────────────────────
SMTP_HOST     = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT     = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER     = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")


def _send_via_sendgrid(to_email: str, subject: str, html_body: str) -> bool:
    """SendGrid API se email bhejo — sabse reliable."""
    if not SENDGRID_API_KEY or not SENDGRID_FROM_EMAIL:
        return False
    try:
        import sendgrid
        from sendgrid.helpers.mail import Mail, Email, To, Content
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        mail = Mail(
            from_email=Email(SENDGRID_FROM_EMAIL, SENDGRID_FROM_NAME),
            to_emails=To(to_email),
            subject=subject,
            html_content=Content("text/html", html_body)
        )
        response = sg.client.mail.send.post(request_body=mail.get())
        success = response.status_code in (200, 201, 202)
        if success:
            print(f"[SENDGRID] Email sent to {to_email}")
        else:
            print(f"[SENDGRID] Failed: {response.status_code}")
        return success
    except Exception as e:
        print(f"[SENDGRID ERROR] {e}")
        return False


def _send_via_smtp(to_email: str, subject: str, html_body: str) -> bool:
    """Gmail SMTP se email bhejo — fallback."""
    if not SMTP_USER or not SMTP_PASSWORD:
        return False
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"GO-TRAVEL <{SMTP_USER}>"
        msg["To"]      = to_email
        msg.attach(MIMEText(html_body, "html"))
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to_email, msg.as_string())
        print(f"[SMTP] Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"[SMTP ERROR] {e}")
        return False


def _send(to_email: str, subject: str, html_body: str) -> bool:
    """
    Email bhejo — SendGrid → SMTP → Test Mode order mein try karo.
    Har user ke APNE email pe jaata hai.
    """
    # 1. SendGrid try karo
    if _send_via_sendgrid(to_email, subject, html_body):
        return True
    # 2. SMTP try karo
    if _send_via_smtp(to_email, subject, html_body):
        return True
    # 3. Test mode otp
    print(f"[EMAIL TEST MODE] No email service configured. OTP shown on screen.")
    return False




def _base_template(title: str, content: str) -> str:
    return f"""
    <div style="font-family:'Segoe UI',Arial,sans-serif;max-width:600px;margin:0 auto;background:#f8fafc;">
        <!-- Header -->
        <div style="background:linear-gradient(135deg,#0F1F47,#1a4480);padding:28px 32px;text-align:center;">
            <div style="display:inline-flex;align-items:center;gap:10px;">
                <div style="width:40px;height:40px;background:linear-gradient(135deg,#E8771E,#f59e0b);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:22px;">✈</div>
                <span style="color:#fff;font-size:24px;font-weight:800;">GO<span style="color:#E8771E;">-TRAVEL</span></span>
            </div>
            <p style="color:rgba(255,255,255,0.65);margin:6px 0 0;font-size:14px;">{title}</p>
        </div>
        <!-- Body -->
        <div style="background:#fff;padding:32px;">
            {content}
        </div>
        <!-- Footer -->
        <div style="background:#f1f5f9;padding:16px 32px;text-align:center;border-top:1px solid #e2e8f0;">
            <p style="color:#94a3b8;font-size:12px;margin:0;">
                © 2026 GO-TRAVEL · CIMAGE College, Patna · Built by Ankit Aryan
            </p>
        </div>
    </div>"""


def send_otp_email(to_email: str, name: str, code: str) -> bool:
    """Password reset OTP — user ke apne email pe jaata hai."""
    content = f"""
        <p style="color:#1e293b;font-size:16px;">Hi <strong>{name}</strong>,</p>
        <p style="color:#475569;font-size:14px;line-height:1.6;">
            You requested to reset your GO-TRAVEL password. Use the OTP below:
        </p>
        <div style="background:linear-gradient(135deg,#0F1F47,#1a4480);border-radius:14px;
                    padding:28px;text-align:center;margin:24px 0;">
            <p style="color:rgba(255,255,255,0.6);font-size:11px;text-transform:uppercase;
                      letter-spacing:2px;margin:0 0 10px;">Your OTP</p>
            <span style="font-size:42px;font-weight:900;letter-spacing:12px;
                         color:#E8771E;font-family:monospace;">{code}</span>
            <p style="color:rgba(255,255,255,0.5);font-size:12px;margin:10px 0 0;">
                ⏱ Valid for 10 minutes only
            </p>
        </div>
        <p style="color:#64748b;font-size:13px;background:#fef9f0;border-left:4px solid #E8771E;
                  padding:10px 14px;border-radius:0 8px 8px 0;">
            🔒 If you did not request this, please ignore this email. Your password will not change.
        </p>"""
    return _send(to_email,
                 "🔐 GO-TRAVEL — Your Password Reset OTP",
                 _base_template("Password Reset", content))


def send_verification_email(to_email: str, code: str) -> bool:
    """Signup email verification — user ke apne email pe jaata hai."""
    content = f"""
        <p style="color:#1e293b;font-size:16px;">Welcome to <strong>GO-TRAVEL!</strong> 🎉</p>
        <p style="color:#475569;font-size:14px;line-height:1.6;">
            Please verify your email address to complete your registration.
        </p>
        <div style="background:linear-gradient(135deg,#065f46,#047857);border-radius:14px;
                    padding:28px;text-align:center;margin:24px 0;">
            <p style="color:rgba(255,255,255,0.6);font-size:11px;text-transform:uppercase;
                      letter-spacing:2px;margin:0 0 10px;">Verification Code</p>
            <span style="font-size:42px;font-weight:900;letter-spacing:12px;
                         color:#fff;font-family:monospace;">{code}</span>
            <p style="color:rgba(255,255,255,0.5);font-size:12px;margin:10px 0 0;">
                ⏱ Valid for 10 minutes only
            </p>
        </div>
        <p style="color:#64748b;font-size:13px;background:#f0fdf4;border-left:4px solid #10b981;
                  padding:10px 14px;border-radius:0 8px 8px 0;">
            Enter this code on the signup page to verify your email.
        </p>"""
    return _send(to_email,
                 "GO-TRAVEL — Verify Your Email",
                 _base_template("Email Verification", content))


def send_itinerary_email(to_email: str, name: str, destination: str, plan: dict) -> bool:
    days_html = ""
    for day in plan.get("days", []):
        days_html += f"""
            <div style="border-left:4px solid #E8771E;padding:12px 16px;margin:10px 0;
                        background:#fef9f0;border-radius:0 8px 8px 0;">
                <strong style="color:#0F1F47;">📅 Day {day.get('day_number')}</strong>
                <p style="margin:6px 0;color:#475569;">{day.get('activities','')}</p>
                <span style="background:#E8771E;color:#fff;padding:2px 10px;border-radius:20px;
                             font-size:11px;font-weight:700;">
                    💰 Est. ₹{day.get('estimated_cost',0)}
                </span>
            </div>"""
    content = f"""
        <p style="color:#1e293b;font-size:16px;">Hi <strong>{name}</strong>,</p>
        <p style="color:#475569;font-size:14px;">Here is your AI-generated itinerary for
            <strong style="color:#0F1F47;">{destination}</strong>:
        </p>
        {f'<p style="background:#f0f4ff;padding:12px;border-radius:8px;color:#4338ca;font-size:13px;">{plan.get("summary","")}</p>' if plan.get("summary") else ""}
        {days_html}
        <p style="margin-top:20px;color:#94a3b8;font-size:13px;">Happy travels! ✈<br>Team GO-TRAVEL</p>"""
    return _send(to_email,
                 f"✈ Your GO-TRAVEL Itinerary — {destination}",
                 _base_template("Your AI Itinerary", content))


def send_booking_confirmation(to_email: str, name: str, hotel_name: str,
                               check_in: str, check_out: str, amount: float) -> bool:
    content = f"""
        <p style="color:#1e293b;font-size:16px;">Hi <strong>{name}</strong>,</p>
        <p style="color:#475569;font-size:14px;">Your hotel booking is confirmed! 🎉</p>
        <div style="background:#f8fafc;border-radius:12px;padding:20px;margin:20px 0;
                    border:1px solid #e2e8f0;">
            <table style="width:100%;border-collapse:collapse;">
                <tr><td style="padding:10px;border-bottom:1px solid #e2e8f0;color:#64748b;font-size:13px;">🏨 Hotel</td>
                    <td style="padding:10px;border-bottom:1px solid #e2e8f0;font-weight:700;color:#0F1F47;">{hotel_name}</td></tr>
                <tr><td style="padding:10px;border-bottom:1px solid #e2e8f0;color:#64748b;font-size:13px;">📅 Check-in</td>
                    <td style="padding:10px;border-bottom:1px solid #e2e8f0;color:#1e293b;">{check_in}</td></tr>
                <tr><td style="padding:10px;border-bottom:1px solid #e2e8f0;color:#64748b;font-size:13px;">📅 Check-out</td>
                    <td style="padding:10px;border-bottom:1px solid #e2e8f0;color:#1e293b;">{check_out}</td></tr>
                <tr><td style="padding:10px;color:#64748b;font-size:13px;">💰 Amount</td>
                    <td style="padding:10px;color:#E8771E;font-weight:800;font-size:18px;">₹{amount}</td></tr>
            </table>
        </div>
        <p style="color:#94a3b8;font-size:13px;">Thank you for booking with GO-TRAVEL! ✈<br>Team GO-TRAVEL</p>"""
    return _send(to_email,
                 f" Booking Confirmed — {hotel_name}",
                 _base_template("Booking Confirmed ", content))
