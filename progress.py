from flask import Flask, render_template, jsonify
from database import DatabaseManager

app = Flask(__name__)
db_manager = DatabaseManager()


def get_progress_data():
    """Fetch progress statistics from all task-related tables."""
    query = """
        SELECT 'task' AS category, COUNT(task_id) AS total, 
               COALESCE(SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END), 0) AS completed
        FROM tasks
        UNION ALL
        SELECT 'subject' AS category, COUNT(s_id) AS total, 
               COALESCE(SUM(CASE WHEN sstatus = 'completed' THEN 1 ELSE 0 END), 0) AS completed
        FROM subject
        UNION ALL
        SELECT 'revision' AS category, COUNT(r_id) AS total, 
               COALESCE(SUM(CASE WHEN rstatus = 'completed' THEN 1 ELSE 0 END), 0) AS completed
        FROM revision
        UNION ALL
        SELECT 'practical' AS category, COUNT(p_id) AS total, 
               COALESCE(SUM(CASE WHEN p_status = 'completed' THEN 1 ELSE 0 END), 0) AS completed
        FROM practical
        UNION ALL
        SELECT 'exam' AS category, COUNT(e_id) AS total, 
               COALESCE(SUM(CASE WHEN estatus = 'completed' THEN 1 ELSE 0 END), 0) AS completed
        FROM exam
        UNION ALL
        SELECT 'discussion' AS category, COUNT(d_id) AS total, 
               COALESCE(SUM(CASE WHEN dstatus = 'completed' THEN 1 ELSE 0 END), 0) AS completed
        FROM discussion;
    """

    progress_data = db_manager.fetch_all(query)
    return {item["category"]: [item["completed"], item["total"] - item["completed"]] for item in progress_data}





