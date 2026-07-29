"""
Ta'allim Mind Map Generator
Visual concept mapping for English grammar topics

Usage:
    from mindmap_generator import MindMapGenerator

    gen = MindMapGenerator()
    mindmap = gen.generate(topic="past_simple")
    gen.save_html(mindmap, "past_simple_map.html")
"""

import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class MindMapNode:
    id: str
    label: str
    parent_id: Optional[str] = None
    color: str = "#4A90D9"
    icon: str = ""
    notes: str = ""
    children: List[str] = field(default_factory=list)


class MindMapGenerator:
    def __init__(self):
        self.topic_structures = self._build_structures()

    def _build_structures(self) -> Dict:
        return {
            "past_simple": {
                "root": "Past Simple Tense",
                "branches": [
                    {
                        "label": "Formation",
                        "color": "#4A90D9",
                        "children": [
                            {"label": "Regular: V + ed", "color": "#5DADE2"},
                            {"label": "Irregular: go/went, eat/ate", "color": "#5DADE2"},
                            {"label": "Be: was/were", "color": "#5DADE2"}
                        ]
                    },
                    {
                        "label": "Usage",
                        "color": "#27AE60",
                        "children": [
                            {"label": "Completed actions", "color": "#52BE80"},
                            {"label": "Past habits", "color": "#52BE80"},
                            {"label": "Past states", "color": "#52BE80"},
                            {"label": "Sequence of events", "color": "#52BE80"}
                        ]
                    },
                    {
                        "label": "Signal Words",
                        "color": "#E74C3C",
                        "children": [
                            {"label": "yesterday", "color": "#EC7063"},
                            {"label": "last week/month/year", "color": "#EC7063"},
                            {"label": "ago", "color": "#EC7063"},
                            {"label": "in 2020", "color": "#EC7063"}
                        ]
                    },
                    {
                        "label": "Negative",
                        "color": "#F39C12",
                        "children": [
                            {"label": "Subject + did not + V", "color": "#F5B041"},
                            {"label": "didn't + base verb", "color": "#F5B041"}
                        ]
                    },
                    {
                        "label": "Questions",
                        "color": "#9B59B6",
                        "children": [
                            {"label": "Did + subject + V?", "color": "#AF7AC5"},
                            {"label": "Wh- + did + S + V?", "color": "#AF7AC5"}
                        ]
                    },
                    {
                        "label": "Common Errors",
                        "color": "#E74C3C",
                        "children": [
                            {"label": "She goed (wrong)", "color": "#EC7063"},
                            {"label": "I didn't went (wrong)", "color": "#EC7063"},
                            {"label": "Did she went? (wrong)", "color": "#EC7063"}
                        ]
                    }
                ]
            },
            "present_perfect": {
                "root": "Present Perfect Tense",
                "branches": [
                    {
                        "label": "Formation",
                        "color": "#4A90D9",
                        "children": [
                            {"label": "have/has + V3", "color": "#5DADE2"},
                            {"label": "Irregular: go/gone, eat/eaten", "color": "#5DADE2"},
                            {"label": "Regular: +ed", "color": "#5DADE2"}
                        ]
                    },
                    {
                        "label": "Usage",
                        "color": "#27AE60",
                        "children": [
                            {"label": "Life experience", "color": "#52BE80"},
                            {"label": "Unfinished actions", "color": "#52BE80"},
                            {"label": "Past to present", "color": "#52BE80"},
                            {"label": "Recent events", "color": "#52BE80"}
                        ]
                    },
                    {
                        "label": "Signal Words",
                        "color": "#E74C3C",
                        "children": [
                            {"label": "already", "color": "#EC7063"},
                            {"label": "yet", "color": "#EC7063"},
                            {"label": "just", "color": "#EC7063"},
                            {"label": "since / for", "color": "#EC7063"}
                        ]
                    },
                    {
                        "label": "since vs for",
                        "color": "#F39C12",
                        "children": [
                            {"label": "since + point in time", "color": "#F5B041"},
                            {"label": "for + duration", "color": "#F5B041"}
                        ]
                    },
                    {
                        "label": "Common Errors",
                        "color": "#E74C3C",
                        "children": [
                            {"label": "She has went (wrong)", "color": "#EC7063"},
                            {"label": "I have eat (wrong)", "color": "#EC7063"}
                        ]
                    }
                ]
            },
            "conditionals": {
                "root": "Conditionals",
                "branches": [
                    {
                        "label": "Zero Conditional",
                        "color": "#4A90D9",
                        "children": [
                            {"label": "If + present, present", "color": "#5DADE2"},
                            {"label": "General truths", "color": "#5DADE2"},
                            {"label": "Example: If you heat water, it boils", "color": "#5DADE2"}
                        ]
                    },
                    {
                        "label": "First Conditional",
                        "color": "#27AE60",
                        "children": [
                            {"label": "If + present, will + V", "color": "#52BE80"},
                            {"label": "Real future possibility", "color": "#52BE80"},
                            {"label": "Example: If it rains, I will stay home", "color": "#52BE80"}
                        ]
                    },
                    {
                        "label": "Second Conditional",
                        "color": "#F39C12",
                        "children": [
                            {"label": "If + past, would + V", "color": "#F5B041"},
                            {"label": "Unreal present", "color": "#F5B041"},
                            {"label": "Example: If I were rich, I would travel", "color": "#F5B041"}
                        ]
                    },
                    {
                        "label": "Third Conditional",
                        "color": "#E74C3C",
                        "children": [
                            {"label": "If + past perfect, would have + V3", "color": "#EC7063"},
                            {"label": "Unreal past", "color": "#EC7063"},
                            {"label": "Example: If I had studied, I would have passed", "color": "#EC7063"}
                        ]
                    }
                ]
            },
            "passive_voice": {
                "root": "Passive Voice",
                "branches": [
                    {
                        "label": "Formation",
                        "color": "#4A90D9",
                        "children": [
                            {"label": "be + V3 (+ by agent)", "color": "#5DADE2"},
                            {"label": "Object becomes subject", "color": "#5DADE2"}
                        ]
                    },
                    {
                        "label": "Tenses",
                        "color": "#27AE60",
                        "children": [
                            {"label": "Present: is/are + V3", "color": "#52BE80"},
                            {"label": "Past: was/were + V3", "color": "#52BE80"},
                            {"label": "Future: will be + V3", "color": "#52BE80"},
                            {"label": "Perfect: have been + V3", "color": "#52BE80"}
                        ]
                    },
                    {
                        "label": "Usage",
                        "color": "#F39C12",
                        "children": [
                            {"label": "Unknown agent", "color": "#F5B041"},
                            {"label": "Unimportant agent", "color": "#F5B041"},
                            {"label": "Formal writing", "color": "#F5B041"}
                        ]
                    }
                ]
            },
            "reported_speech": {
                "root": "Reported Speech",
                "branches": [
                    {
                        "label": "Statements",
                        "color": "#4A90D9",
                        "children": [
                            {"label": "S + said (that) + clause", "color": "#5DADE2"},
                            {"label": "Tense shift back", "color": "#5DADE2"}
                        ]
                    },
                    {
                        "label": "Questions",
                        "color": "#27AE60",
                        "children": [
                            {"label": "Yes/No: if/whether + clause", "color": "#52BE80"},
                            {"label": "Wh-: wh- word + clause", "color": "#52BE80"}
                        ]
                    },
                    {
                        "label": "Commands",
                        "color": "#F39C12",
                        "children": [
                            {"label": "told + to + V", "color": "#F5B041"},
                            {"label": "told + not to + V", "color": "#F5B041"}
                        ]
                    },
                    {
                        "label": "Changes",
                        "color": "#E74C3C",
                        "children": [
                            {"label": "Tense: present->past", "color": "#EC7063"},
                            {"label": "Pronoun: I->he/she", "color": "#EC7063"},
                            {"label": "Time: now->then", "color": "#EC7063"}
                        ]
                    }
                ]
            }
        }

    def generate(self, topic: str, custom_branches: List[Dict] = None) -> Dict:
        structure = self.topic_structures.get(topic)
        if not structure:
            return {"error": f"Topic '{topic}' not found. Available: {list(self.topic_structures.keys())}"}

        nodes = []
        node_id = 0

        root = MindMapNode(
            id=str(node_id),
            label=structure["root"],
            color="#2C3E50",
            icon="root"
        )
        nodes.append(root)
        node_id += 1

        branches = custom_branches or structure["branches"]
        for branch in branches:
            branch_node = MindMapNode(
                id=str(node_id),
                label=branch["label"],
                parent_id="0",
                color=branch.get("color", "#4A90D9"),
                icon="branch"
            )
            nodes.append(branch_node)
            root.children.append(branch_node.id)
            branch_id = node_id
            node_id += 1

            for child in branch.get("children", []):
                child_node = MindMapNode(
                    id=str(node_id),
                    label=child["label"],
                    parent_id=branch_id,
                    color=child.get("color", "#5DADE2"),
                    icon="leaf"
                )
                nodes.append(child_node)
                branch_node.children.append(child_node.id)
                node_id += 1

        return {
            "topic": topic,
            "root_label": structure["root"],
            "nodes": [asdict(n) for n in nodes],
            "node_count": len(nodes),
            "branch_count": len(branches)
        }

    def save_json(self, mindmap: Dict, filepath: str):
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(mindmap, f, ensure_ascii=False, indent=2)

    def save_html(self, mindmap: Dict, filepath: str):
        nodes = mindmap.get("nodes", [])
        root_label = mindmap.get("root_label", "Mind Map")

        nodes_json = json.dumps(nodes, ensure_ascii=False)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{root_label} - Ta'allim Mind Map</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: #f0f2f5; }}
        .header {{
            background: linear-gradient(135deg, #2C3E50, #3498DB);
            color: white; padding: 20px; text-align: center;
        }}
        .header h1 {{ font-size: 24px; }}
        .header p {{ opacity: 0.8; margin-top: 5px; }}
        .container {{ max-width: 1200px; margin: 20px auto; padding: 0 20px; }}
        .mindmap {{
            background: white; border-radius: 12px; padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .root-node {{
            text-align: center; margin-bottom: 30px;
        }}
        .root-node span {{
            background: #2C3E50; color: white; padding: 15px 30px;
            border-radius: 25px; font-size: 20px; font-weight: bold;
            display: inline-block;
        }}
        .branches {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }}
        .branch {{
            border-radius: 10px; overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .branch-header {{
            padding: 12px 16px; color: white; font-weight: bold; font-size: 16px;
        }}
        .branch-content {{ padding: 12px; background: white; }}
        .leaf {{
            padding: 8px 12px; margin: 4px 0; border-radius: 6px;
            font-size: 14px; background: #f8f9fa; border-left: 3px solid;
        }}
        .legend {{
            margin-top: 20px; padding: 15px; background: #f8f9fa;
            border-radius: 8px; font-size: 12px; color: #666;
        }}
        .legend strong {{ color: #333; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{root_label}</h1>
        <p>Ta'allim Visual Learning Tool</p>
    </div>
    <div class="container">
        <div class="mindmap">
            <div class="root-node">
                <span>{root_label}</span>
            </div>
            <div class="branches" id="branches"></div>
            <div class="legend">
                <strong>How to use:</strong> This mind map shows the key concepts for {root_label}.
                Review each branch to understand the rules, usage, and common errors.
                Use this as a study guide before doing exercises.
            </div>
        </div>
    </div>
    <script>
        const nodes = {nodes_json};
        const branches = {{}};
        nodes.forEach(n => {{
            if (n.parent_id === '0') {{
                branches[n.id] = {{ ...n, children_nodes: [] }};
            }} else if (n.parent_id && branches[n.parent_id]) {{
                branches[n.parent_id].children_nodes.push(n);
            }}
        }});
        const container = document.getElementById('branches');
        Object.values(branches).forEach(branch => {{
            const div = document.createElement('div');
            div.className = 'branch';
            let leaves = branch.children_nodes.map(c =>
                `<div class="leaf" style="border-color: ${{c.color}}">${{c.label}}</div>`
            ).join('');
            div.innerHTML = `
                <div class="branch-header" style="background: ${{branch.color}}">${{branch.label}}</div>
                <div class="branch-content">${{leaves}}</div>
            `;
            container.appendChild(div);
        }});
    </script>
</body>
</html>"""

        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
