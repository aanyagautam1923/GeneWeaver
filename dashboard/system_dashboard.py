from app.core.performance_engine import system_metrics
import json
from pathlib import Path

def main():
    data = system_metrics()
    print("GENEWEAVER SYSTEM DASHBOARD")
    print("=" * 35)
    for key, value in data.items():
        print(f"{key}: {value}")
    Path("results").mkdir(exist_ok=True)
    Path("results/system_metrics.json").write_text(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
