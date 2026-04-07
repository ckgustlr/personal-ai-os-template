import yaml

def yaml_to_mermaid_advanced(yaml_str):
    data = yaml.safe_load(yaml_str)
    steps = data.get("steps", [])

    lines = ["graph TD"]

    for step in steps:
        name = step["name"]
        step_type = step.get("type", "")

        label = f"{name}[{step_type}]"
        lines.append(f"    {name}{label}")

    for i in range(len(steps) - 1):
        lines.append(f"    {steps[i]['name']} --> {steps[i+1]['name']}")

    return "\n".join(lines)


# 사용 예
yaml_input = """
recipe_name: revenue_calc
steps:
  - name: load_sales
    type: load
  - name: calc_margin
    type: formula
  - name: filter_positive
    type: filter
"""

print(yaml_to_mermaid_advanced(yaml_input))