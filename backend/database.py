
import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "alee.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with get_connection() as connection:

        # Store each learner's initial level estimate
        connection.execute("""
            CREATE TABLE IF NOT EXISTS initial_estimates (
                learner_id INTEGER PRIMARY KEY,
                estimated_level TEXT NOT NULL,
                confidence INTEGER NOT NULL,
                evidence TEXT NOT NULL
            )
        """)

        # Store external diagnostic results
        connection.execute("""
            CREATE TABLE IF NOT EXISTS diagnostic_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                learner_id INTEGER NOT NULL,
                diagnostic_name TEXT NOT NULL,
                overall_level TEXT NOT NULL,
                overall_score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                correct_answers INTEGER NOT NULL,
                incorrect_answers INTEGER NOT NULL,
                result_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Index diagnostic results by learner
        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_diagnostic_learner
            ON diagnostic_results (learner_id, id)
        """)

        # Store vocabulary learning experiment results
        connection.execute("""
            CREATE TABLE IF NOT EXISTS learning_experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                learner_id INTEGER NOT NULL,
                method TEXT NOT NULL,
                vocabulary_set_id TEXT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Index experiment results by learner
        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_experiments_learner
            ON learning_experiments (learner_id, id)
        """)


        connection.execute("""
            CREATE TABLE IF NOT EXISTS learner_learning_stages (
                learner_id INTEGER PRIMARY KEY,
                current_stage TEXT NOT NULL,
                current_method TEXT,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
