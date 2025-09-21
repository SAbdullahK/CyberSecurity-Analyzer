


class PatternMatcher:
    def check(self, log_entry):
        suspicious_keywords = ["failed login", "unauthorized", "malware", "error"]
        return any(word in log_entry.lower() for word in suspicious_keywords)
    