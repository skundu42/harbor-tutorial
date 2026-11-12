import json

EXPECTED = {"errors": 4, "top_ip": "10.0.0.4", "slowest_path": "/api/export"}

try:
    answer = json.load(open("/app/answer.json"))
except (OSError, ValueError):
    answer = {}

correct = 0
for key, expected in EXPECTED.items():
    got = answer.get(key)
    correct += got == expected
    print(f"{'PASS' if got == expected else 'FAIL'} {key}: got {got!r}, expected {expected!r}")

reward = round(correct / len(EXPECTED), 3)
json.dump({"reward": reward}, open("/logs/verifier/reward.json", "w"))
print("reward:", reward)
