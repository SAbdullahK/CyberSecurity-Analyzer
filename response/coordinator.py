import smtplib

class  ResponseCordinator:
    def __init__(self, stakeholders=None):
        self.stakeholders = stakeholders or ["security_team@example.com"]


    def coordinate_response(self, anomaly, severity):
        if severity >= 7:
            self.send_email_alert(anomaly, severity)
        else:
            self.log_event(anomaly, severity)
    
    def send_email_alert(self, anomaly, severity):
        msg = f"High severity({severity}) anomaly dectected: \n{anomaly}"
        try:
            with smtplib.SMTP("localhost") as server:
                server.sendmail("analyzer@system", self.stakeholders, msg)
        except Exception:
            print("[!] Email sending skipped (no SMTP configured).")

    def log_event(self, anomaly, severity):
        with open("alerts.log", "a") as f:
            f.write(f"[SEVERITY {severity}] {anomaly}\n")
            
        