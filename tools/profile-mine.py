#!/usr/bin/env python
# Workstation-mining profile builder. Reads the operator's OWN data on their OWN
# machine -- Chrome's autofill database (everything typed in a field), the career
# campaign's prior applications (custom-question answers), the candidate profile,
# and resume/docs -- into one comprehensive local answers knowledge base that the
# form-filler consults to auto-answer ANY required field. Stays LOCAL (no upload,
# no commit; PII never leaves the workstation). Never extracts credentials.
#
#   python profile-mine.py > answers-db.json
import sqlite3, json, os, shutil, tempfile, re, sys, csv as _csv

def mine_chrome_autofill():
    """Copy Chrome's Web Data (locked while Chrome runs) and read the autofill
    table: field-name -> [typed values]. The most direct 'what has the operator
    actually entered before' source."""
    src = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Web Data")
    out = {}
    if not os.path.exists(src):
        return {"_note": "no default Web Data"}
    tmp = os.path.join(tempfile.gettempdir(), "nc_webdata_copy.sqlite")
    try:
        shutil.copy(src, tmp)
    except Exception as e:
        return {"_note": f"copy failed (chrome running?): {e}"}
    try:
        con = sqlite3.connect(tmp)
        # field-name -> typed values (most-used first)
        rows = con.execute("SELECT name, value, count FROM autofill ORDER BY count DESC").fetchall()
        by_field = {}
        for name, value, count in rows:
            n = (name or "").lower().strip()
            v = (value or "").strip()
            if n and v and len(v) < 80 and not re.search(r"(password|pwd|passwd|secret|token|cvv|cvc|cardnumber|accountno)", n + v):
                by_field.setdefault(n, []).append({"value": v, "count": count})
        con.close()
        # also the structured autofill profile tables (addresses/names/phones)
        try:
            con = sqlite3.connect(tmp)
            for tbl in ("autofill_profile_addresses", "autofill_profile_names", "autofill_profile_phones", "autofill_profile_emails"):
                try:
                    cols = [c[1] for c in con.execute(f"PRAGMA table_info({tbl})").fetchall()]
                    for r in con.execute(f"SELECT * FROM {tbl}").fetchall():
                        out.setdefault("_profiles", []).append(dict(zip(cols, r)))
                except Exception:
                    pass
            con.close()
        except Exception:
            pass
        return {"field_values": by_field, "field_count": len(by_field)}
    except Exception as e:
        return {"_note": f"sqlite read failed: {e}"}

def mine_candidate_profile():
    p = r"C:\Users\Zain\career-campaign\candidate-profile.json"
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception as e:
        return {"_note": str(e)}

def mine_applications_answers():
    """Scan the campaign's applications.csv for custom-question answer patterns
    buried in materials/notes -- prior apps already answered many fields."""
    p = r"C:\Users\Zain\career-campaign\applications.csv"
    out = {"track_counts": {}, "status_counts": {}, "notes_signals": {}}
    try:
        with open(p, encoding="utf-8") as f:
            for row in _csv.DictReader(f):
                out["track_counts"][row.get("track", "")] = out["track_counts"].get(row.get("track", ""), 0) + 1
                out["status_counts"][row.get("status", "")] = out["status_counts"].get(row.get("status", ""), 0) + 1
                # salary/comp signals
                for m in re.findall(r"(\$\s?\d{2,3}[,\d]{0,6}(?:/hr|k|\s*/\s*yr)?)", row.get("compensation", "") + " " + row.get("notes", "")):
                    out["notes_signals"].setdefault("comp_seen", []).append(m)
    except Exception as e:
        out["_note"] = str(e)
    out["track_count"] = len(out["track_counts"])
    return out

def mine_resume():
    for p in (r"C:\Users\Zain\HarperZ9-site\resume.md", r"C:\Users\Zain\HarperZ9-site\cv.md"):
        try:
            t = open(p, encoding="utf-8").read()
            # extract emails, phones, skills, education-ish lines
            emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", t)
            phones = re.findall(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}", t)
            return {"path": p, "emails": list(set(emails))[:4], "phones": list(set(phones))[:3], "chars": len(t)}
        except Exception:
            continue
    return {"_note": "no resume found"}

db = {
    "schema": "project-telos.operator-profile/v1",
    "scope": "operator's own workstation data; local-only; no credentials",
    "built_at": __import__("datetime").datetime.utcnow().isoformat(timespec="seconds") + "Z",
    "chrome_autofill": mine_chrome_autofill(),
    "candidate_profile": mine_candidate_profile(),
    "applications_signals": mine_applications_answers(),
    "resume": mine_resume(),
}
print(json.dumps(db, indent=2, default=str))
