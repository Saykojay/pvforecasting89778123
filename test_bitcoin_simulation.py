import unittest
import numpy as np
import pandas as pd
from bitcoin_simulation import simulate_bitcoin_prices

class TestBitcoinSimulation(unittest.TestCase):
    def test_simulate_bitcoin_prices_length(self):
        days = 60
        prices = simulate_bitcoin_prices(days=days)
        self.assertEqual(len(prices), days)

    def test_simulate_bitcoin_prices_values(self):
        initial_price = 50000
        prices = simulate_bitcoin_prices(days=10, initial_price=initial_price)
        self.assertEqual(prices[0], initial_price)
        # First price might be int, others float
        self.assertTrue(all(isinstance(p, (int, float, np.float64)) for p in prices))
        self.assertTrue(all(p > 0 for p in prices)) # Prices should be positive

    def test_simulate_bitcoin_prices_reproducibility(self):
        prices1 = simulate_bitcoin_prices(days=10, seed=42)
        prices2 = simulate_bitcoin_prices(days=10, seed=42)
        self.assertEqual(prices1, prices2)

        prices3 = simulate_bitcoin_prices(days=10, seed=43)
        self.assertNotEqual(prices1, prices3)

if __name__ == '__main__':
    unittest.main()
