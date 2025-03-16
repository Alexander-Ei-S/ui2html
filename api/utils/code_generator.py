def generate_html_css(element_type: str) -> str:
    templates = {
        "button": (
            '<button class="neu-button">Click</button>\n'
            '<style>.neu-button { padding: 12px 24px; border: none; border-radius: 8px; background: #f0f0f3; box-shadow: 5px 5px 10px #d3d3d6, -5px -5px 10px #ffffff; }</style>'
        ),
        "input": (
            '<input type="text" class="neu-input" placeholder="Enter text">\n'
            '<style>.neu-input { padding: 12px; border: none; border-radius: 6px; background: #f0f0f3; box-shadow: inset 3px 3px 6px #d3d3d6, inset -3px -3px 6px #ffffff; }</style>'
        ),
        "card": (
            '<div class="neu-card">\n  <h3>Card Title</h3>\n  <p>Card content</p>\n</div>\n'
            '<style>.neu-card { padding: 20px; border-radius: 12px; background: #f0f0f3; box-shadow: 10px 10px 20px #d3d3d6, -10px -10px 20px #ffffff; }</style>'
        )
    }
    return templates.get(element_type, "<!-- Element not supported -->")