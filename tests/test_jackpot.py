import unittest
from app.jackpot import spin_jackpot

class TestJackpot(unittest.TestCase):

    # 1. 기본 구조 테스트
    def test_spin_length(self):
        result, jackpot = spin_jackpot()
        self.assertEqual(len(result), 3)

    # 2. 타입 테스트
    def test_spin_type(self):
        result, jackpot = spin_jackpot()
        self.assertEqual(type(result), list)
        self.assertEqual(type(jackpot), bool)

    # 3. 값이 symbols 안에 있는지 확인 (블랙박스 테스트)
    def test_valid_symbols(self):
        result, _ = spin_jackpot()
        symbols = ["🍒", "🍋", "⭐", "💎", "7️⃣"]

        for s in result:
            self.assertIn(s, symbols)

    # 4. jackpot 조건 테스트 (화이트박스 테스트 느낌)
    def test_jackpot_true_case(self):
        # 직접 강제 데이터 넣어서 테스트
        result = ["🍒", "🍒", "🍒"]
        jackpot = (result[0] == result[1] == result[2])

        self.assertTrue(jackpot)

    def test_jackpot_false_case(self):
        result = ["🍒", "🍋", "⭐"]
        jackpot = (result[0] == result[1] == result[2])

        self.assertFalse(jackpot)

    # 5. 반복 테스트 (확률 기반 함수 안정성)
    def test_multiple_runs(self):
        for _ in range(100):
            result, jackpot = spin_jackpot()
            self.assertEqual(len(result), 3)

    # 6. 예외 상황 없는지 (퍼징 느낌 테스트)
    def test_no_error(self):
        try:
            for _ in range(100):
                spin_jackpot()
        except Exception as e:
            self.fail(f"에러 발생: {e}")


if __name__ == "__main__":
    unittest.main()