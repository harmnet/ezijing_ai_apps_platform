from app import create_app

app = create_app()

print("所有注册的路由:")
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint:50s} -> {rule.rule}") 