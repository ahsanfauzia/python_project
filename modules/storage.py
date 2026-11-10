import json
from modules.auth import connect

def save_analysis(user_id, role, company, resume_name, score, profile, result, jd):
    with connect() as c:
        cur = c.execute("""INSERT INTO analyses(user_id,role_title,company,resume_name,score,profile_json,result_json,job_description)
            VALUES(?,?,?,?,?,?,?,?)""", (user_id,role,company,resume_name,score,json.dumps(profile),json.dumps(result),jd))
        return cur.lastrowid

def list_analyses(user_id):
    with connect() as c:
        rows = c.execute("SELECT id,role_title,company,score,created_at FROM analyses WHERE user_id=? ORDER BY id DESC",(user_id,)).fetchall()
    return [dict(r) for r in rows]

def delete_analysis(user_id, analysis_id):
    with connect() as c:
        c.execute("DELETE FROM analyses WHERE user_id=? AND id=?", (user_id,analysis_id))
