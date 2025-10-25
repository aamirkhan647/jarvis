# tests/test_ranker.py
import unittest
from core.ranker import rank_jobs


class TestRanker(unittest.TestCase):
    def test_rank_simple(self):
        jobs = [
            {
                "id": "1",
                "title": "Python Developer",
                "description": "Python, REST, AWS",
            },
            {"id": "2", "title": "Java Developer", "description": "Java, Spring"},
        ]
        resume = "Experienced Python developer with AWS and REST APIs"
        ranked = rank_jobs(jobs, resume, top_k=2)
        self.assertEqual(ranked[0]["id"], "1")
        self.assertGreaterEqual(ranked[0]["score"], ranked[1]["score"])


if __name__ == "__main__":
    unittest.main()
