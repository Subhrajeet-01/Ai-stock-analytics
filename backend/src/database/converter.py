class cleaner:
    @staticmethod
    def clean_number(s: str):
        if s is None:
            return None
        s = s.strip()
        if s == "" or s == "-":
            return None
        # remove thousands separators and surrounding quotes
        s = s.replace('"', "").replace("'", "")
        s = s.replace(",", "")
        try:
            return float(s)
        except Exception:
            return None

    @staticmethod
    def clean_int(s: str):
        f = cleaner.clean_number(s)
        if f is None:
            return None
        try:
            return int(f)
        except Exception:
            return None

clean_number = cleaner.clean_number
clean_int = cleaner.clean_int
