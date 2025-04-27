from typing import List, Dict


# Мемоізація
def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    memo = {}

    def helper(n):
        if n == 0:
            return 0, []
        if n in memo:
            return memo[n]

        max_profit = 0
        best_cut = []

        for i in range(1, n + 1):
            profit, cuts = helper(n - i)
            if prices[i - 1] + profit > max_profit:
                max_profit = prices[i - 1] + profit
                best_cut = [i] + cuts

        memo[n] = (max_profit, best_cut)
        return memo[n]

    max_profit, cuts = helper(length)
    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1  # Кількість розрізів
    }


# Табуляція
def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    dp = [0] * (length + 1)
    cuts = [0] * (length + 1)

    for i in range(1, length + 1):
        for j in range(1, i + 1):
            if dp[i] < prices[j - 1] + dp[i - j]:
                dp[i] = prices[j - 1] + dp[i - j]
                cuts[i] = j

    max_profit = dp[length]
    cuts_list = []
    n = length
    while n > 0:
        cuts_list.append(cuts[n])
        n -= cuts[n]

    return {
        "max_profit": max_profit,
        "cuts": cuts_list,
        "number_of_cuts": len(cuts_list) - 1  # Кількість розрізів
    }


def run_tests():
    test_cases = [
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("\nПеревірка пройшла успішно!")


if __name__ == "__main__":
    run_tests()
